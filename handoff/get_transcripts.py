"""Pull raw, timestamped YouTube captions for IdleOn creators (Griffy, Pulse, Nocturne).
Run on your own PC. Output: idleon_transcripts/sources/creators/<creator>/{transcripts/*.txt, index.csv}
plus idleon_transcripts.zip. Safe to stop and re-run: finished videos are skipped.

Setup (Windows, once):  py -m pip install -U yt-dlp youtube-transcript-api
Run:                    py get_transcripts.py
Optional: py get_transcripts.py griffybit   (one creator only)
"""
import csv, os, random, re, shutil, sys, time
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

CREATORS = {
    'griffybit': 'https://www.youtube.com/channel/UCt5WC8O9Jrb-UeNcI5T9BoQ',
    'pulseidle': 'https://www.youtube.com/@PulseIdle',
    'nocturne': 'https://www.youtube.com/@NocturneGamingOfficial',
}
ROOT = os.path.join('idleon_transcripts', 'sources', 'creators')
MIN_SECONDS = 120          # skip shorts
PAUSE = (3, 7)             # seconds between videos, be polite to YouTube
IDLEON = re.compile(r'idle\s?on|legends of idleon', re.I)
YDL = {'quiet': True, 'no_warnings': True, 'skip_download': True}

def list_tab(url):
    with yt_dlp.YoutubeDL({**YDL, 'extract_flat': True}) as y:
        info = y.extract_info(url, download=False) or {}
    return [e for e in (info.get('entries') or []) if e and e.get('id')]

def video_info(vid):
    with yt_dlp.YoutubeDL(YDL) as y:
        return y.extract_info(f'https://www.youtube.com/watch?v={vid}', download=False)

def kind(title, from_streams, was_live):
    t = title.lower()
    if re.search(r'review|roast|bingo', t): return 'review'
    if from_streams or was_live: return 'stream'
    if re.search(r'\bep\.?\s?\d|episode|f2p guide|playthrough|next chapter', t): return 'playthrough'
    return 'guide'

def ts(sec):
    s = int(sec); return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'

def fetch_api(vid):
    api = YouTubeTranscriptApi()
    t = api.fetch(vid, languages=['en', 'en-US', 'en-GB'])
    snippets = list(t)
    return [(s.start, s.text) for s in snippets], ('auto' if getattr(t, 'is_generated', True) else 'manual')

def fetch_ytdlp(vid):
    tmp = os.path.join('idleon_transcripts', '_tmp'); os.makedirs(tmp, exist_ok=True)
    opts = {**YDL, 'writesubtitles': True, 'writeautomaticsub': True, 'subtitleslangs': ['en.*', 'en'],
            'subtitlesformat': 'vtt', 'outtmpl': os.path.join(tmp, '%(id)s')}
    with yt_dlp.YoutubeDL(opts) as y:
        y.download([f'https://www.youtube.com/watch?v={vid}'])
    files = [f for f in os.listdir(tmp) if f.startswith(vid) and f.endswith('.vtt')]
    if not files: raise RuntimeError('no subtitles')
    lines, last = [], None
    for block in open(os.path.join(tmp, files[0]), encoding='utf-8').read().split('\n\n'):
        m = re.search(r'(\d+):(\d+):(\d+)\.\d+ -->', block)
        if not m: continue
        start = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        text = re.sub(r'<[^>]+>', '', ' '.join(block.split('\n')[1:])).strip()
        if text and text != last:
            lines.append((start, text)); last = text
    for f in files: os.remove(os.path.join(tmp, f))
    return lines, 'auto'

def coverage(lines, duration):
    if not lines or not duration: return 0.0, 0
    starts = [s for s, _ in lines]
    gaps = [b - a for a, b in zip(starts, starts[1:])] + [duration - starts[-1], starts[0]]
    return min(1.0, starts[-1] / duration), int(max(gaps))

def run(name, url):
    base = os.path.join(ROOT, name); tdir = os.path.join(base, 'transcripts'); os.makedirs(tdir, exist_ok=True)
    idx_path = os.path.join(base, 'index.csv')
    done = set()
    if os.path.exists(idx_path):
        with open(idx_path, encoding='utf-8') as f:
            done = {r['video_id'] for r in csv.DictReader(f) if r['status'] in ('ok', 'partial', 'skipped')}
    entries = [(e, False) for e in list_tab(url + '/videos')] + [(e, True) for e in list_tab(url + '/streams')]
    print(f'{name}: {len(entries)} videos/streams listed, {len(done)} already done')
    new = not os.path.exists(idx_path)
    with open(idx_path, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if new: w.writerow(['video_id', 'date', 'title', 'duration_min', 'type', 'captions', 'words', 'coverage', 'max_gap_s', 'status'])
        for i, (e, from_streams) in enumerate(entries, 1):
            vid = e['id']
            if vid in done: continue
            try:
                info = video_info(vid)
            except Exception as ex:
                print(f'  [{i}] {vid} info failed: {ex}'); continue
            title = info.get('title') or ''
            dur = int(info.get('duration') or 0)
            date = info.get('upload_date') or ''
            date = f'{date[:4]}-{date[4:6]}-{date[6:]}' if len(date) == 8 else ''
            text = ' '.join([title, info.get('description') or '', ' '.join(info.get('tags') or [])])
            if dur < MIN_SECONDS or not IDLEON.search(text):
                w.writerow([vid, date, title, round(dur / 60, 1), '', '', 0, '', '', 'skipped']); f.flush(); continue
            typ = kind(title, from_streams, info.get('was_live'))
            lines, caps, err = None, '', ''
            for attempt in range(3):
                try:
                    lines, caps = fetch_api(vid); break
                except Exception as ex:
                    err = str(ex)[:120]
                    try:
                        lines, caps = fetch_ytdlp(vid); break
                    except Exception as ex2:
                        err = f'{err} | {str(ex2)[:120]}'; time.sleep(20 * (attempt + 1))
            if not lines:
                print(f'  [{i}] {vid} FAILED: {err}')
                w.writerow([vid, date, title, round(dur / 60, 1), typ, '', 0, '', '', 'failed']); f.flush()
                continue
            cov, gap = coverage(lines, dur)
            status = 'ok' if cov >= 0.9 and gap <= 600 else 'partial'
            words = sum(len(t.split()) for _, t in lines)
            fn = os.path.join(tdir, f'{date or "nodate"}_{vid}.txt')
            with open(fn, 'w', encoding='utf-8') as out:
                out.write(f'title: {title}\nurl: https://www.youtube.com/watch?v={vid}\ndate: {date}\n'
                          f'duration_min: {round(dur / 60, 1)}\ntype: {typ}\ncaptions: {caps}\n---\n')
                out.write('\n'.join(f'[{ts(s)}] {t}' for s, t in lines))
            w.writerow([vid, date, title, round(dur / 60, 1), typ, caps, words, round(cov, 2), gap, status]); f.flush()
            print(f'  [{i}/{len(entries)}] {status} {date} {title[:60]} ({words} words)')
            time.sleep(random.uniform(*PAUSE))

if __name__ == '__main__':
    pick = sys.argv[1:] or list(CREATORS)
    for name in pick:
        run(name, CREATORS[name])
    shutil.make_archive('idleon_transcripts', 'zip', 'idleon_transcripts')
    print('Done. Upload idleon_transcripts.zip to ChatGPT.')
