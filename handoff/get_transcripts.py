"""Pull raw, timestamped YouTube captions for IdleOn creators (Griffy, Pulse, Nocturne).
Run on your own PC. Output: idleon_transcripts/sources/creators/<creator>/{transcripts/*.txt, index.csv}
plus idleon_transcripts.zip. Safe to stop and re-run: finished videos are skipped, failures retried.

Faster version:
- ONE request per video: yt-dlp gets the details and the captions together.
- Optional: put a cookies.txt (YouTube cookies exported from your browser) next to this script and it
  uses your login so YouTube throttles less. Without it, runs logged out.
- Priority order across all three creators: account reviews first, then guides, then playthroughs, then streams.

Setup (Windows, once):  py -m pip install -U yt-dlp youtube-transcript-api
Run:                    py get_transcripts.py
"""
import csv, os, random, re, shutil, sys, time
import yt_dlp

CREATORS = {
    'griffybit': 'https://www.youtube.com/channel/UCt5WC8O9Jrb-UeNcI5T9BoQ',
    'pulseidle': 'https://www.youtube.com/@PulseIdle',
    'nocturne': 'https://www.youtube.com/@NocturneGamingOfficial',
}
COOKIEFILE = 'cookies.txt'  # optional: YouTube cookies exported from your browser, next to this script
ROOT = os.path.join('idleon_transcripts', 'sources', 'creators')
TMP = os.path.join('idleon_transcripts', '_tmp')
MIN_SECONDS = 120
PAUSE = (6, 12)
COOLDOWN = 600
SKIP_IDS = {'N2EFqfVHNMM'}  # 21-hour Remastered Movie (excluded by Zack)
IDLEON = re.compile(r'idle\s?on|legends of idleon', re.I)
ORDER = {'review': 0, 'guide': 1, 'playthrough': 2, 'stream': 3}
COOKIES = os.path.exists(COOKIEFILE)

def base_opts():
    o = {'quiet': True, 'no_warnings': True, 'skip_download': True}
    if COOKIES:
        o['cookiefile'] = COOKIEFILE
    return o

def kind(title, from_streams=False, was_live=False):
    t = (title or '').lower()
    if re.search(r'review|roast|bingo', t): return 'review'
    if from_streams or was_live: return 'stream'
    if re.search(r'\bep\.?\s?\d|episode|f2p guide|playthrough|next chapter', t): return 'playthrough'
    return 'guide'

def list_tab(url):
    global COOKIES
    try:
        with yt_dlp.YoutubeDL({**base_opts(), 'extract_flat': True}) as y:
            info = y.extract_info(url, download=False) or {}
    except Exception as ex:
        if 'does not have a' in str(ex):
            return []  # channel has no such tab (e.g. no Streams)
        if COOKIES:
            print(f'  cookies.txt not usable ({str(ex)[:100]}); continuing without.')
            COOKIES = False
            return list_tab(url)
        raise
    return [e for e in (info.get('entries') or []) if e and e.get('id')]

def ts(sec):
    s = int(sec); return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'

def parse_vtt(path):
    lines, last = [], None
    for block in open(path, encoding='utf-8').read().split('\n\n'):
        m = re.search(r'(\d+):(\d+):(\d+)\.\d+ -->', block)
        if not m: continue
        start = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        text = re.sub(r'<[^>]+>', '', ' '.join(block.split('\n')[1:])).strip()
        if text and text != last:
            lines.append((start, text)); last = text
    return lines

def fetch(vid):
    """One yt-dlp call: details + captions. Returns (info, lines, caption_kind)."""
    os.makedirs(TMP, exist_ok=True)
    opts = {**base_opts(), 'writesubtitles': True, 'writeautomaticsub': True,
            'subtitleslangs': ['en', 'en-US', 'en-GB', 'en-orig'], 'subtitlesformat': 'vtt',
            'outtmpl': os.path.join(TMP, '%(id)s')}
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(f'https://www.youtube.com/watch?v={vid}', download=True)
    files = sorted(f for f in os.listdir(TMP) if f.startswith(vid) and f.endswith('.vtt'))
    lines, caps = [], ''
    if files:
        subs = info.get('subtitles') or {}
        manual = [f for f in files if any(f'.{k}.' in f for k in subs)]
        pick = manual[0] if manual else files[0]
        lines, caps = parse_vtt(os.path.join(TMP, pick)), ('manual' if manual else 'auto')
    for f in files: os.remove(os.path.join(TMP, f))
    return info, lines, caps

def fetch_api(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    t = YouTubeTranscriptApi().fetch(vid, languages=['en', 'en-US', 'en-GB'])
    return [(s.start, s.text) for s in t], ('auto' if getattr(t, 'is_generated', True) else 'manual')

def coverage(lines, duration):
    if not lines or not duration: return 0.0, 0
    starts = [s for s, _ in lines]
    gaps = [b - a for a, b in zip(starts, starts[1:])] + [duration - starts[-1], starts[0]]
    return min(1.0, starts[-1] / duration), int(max(gaps))

def load_done(name):
    p = os.path.join(ROOT, name, 'index.csv')
    if not os.path.exists(p): return set()
    with open(p, encoding='utf-8') as f:
        return {r['video_id'] for r in csv.DictReader(f) if r['status'] in ('ok', 'partial', 'skipped')}

def writer(name):
    base = os.path.join(ROOT, name); os.makedirs(os.path.join(base, 'transcripts'), exist_ok=True)
    p = os.path.join(base, 'index.csv'); new = not os.path.exists(p)
    f = open(p, 'a', newline='', encoding='utf-8'); w = csv.writer(f)
    if new: w.writerow(['video_id', 'date', 'title', 'duration_min', 'type', 'captions', 'words', 'coverage', 'max_gap_s', 'status'])
    return f, w

def main():
    print('Using cookies.txt login' if COOKIES else 'No cookies.txt: running logged out')
    pick = sys.argv[1:] or list(CREATORS)
    queue = []
    for name in pick:
        done = load_done(name)
        n = 0
        for tab, from_streams in (('/videos', False), ('/streams', True)):
            for e in list_tab(CREATORS[name] + tab):
                vid, title, dur = e['id'], e.get('title') or '', e.get('duration')
                if vid in done or vid in SKIP_IDS: continue
                if dur and dur < MIN_SECONDS: continue
                queue.append((ORDER[kind(title, from_streams)], name, vid, title, from_streams)); n += 1
        print(f'{name}: {n} to fetch ({len(done)} already done)')
    queue.sort(key=lambda q: q[0])  # reviews first across all creators (listing is newest-first within each)
    files = {name: writer(name) for name in pick}
    print(f'Total to fetch: {len(queue)}. Reviews first.')
    for i, (_, name, vid, title0, from_streams) in enumerate(queue, 1):
        f, w = files[name]
        info, lines, caps, err = None, [], '', ''
        for attempt in range(3):
            try:
                info, lines, caps = fetch(vid)
                if not lines:
                    try: lines, caps = fetch_api(vid)
                    except Exception as ex: err = str(ex)[:120]
                break
            except Exception as ex:
                err = str(ex)[:160]
                if '429' in err or 'Too Many' in err:
                    print(f'  rate limited, cooling down {COOLDOWN // 60} min...'); time.sleep(COOLDOWN)
                else:
                    time.sleep(15 * (attempt + 1))
        if info is None:
            print(f'  [{i}/{len(queue)}] FAILED {name} {vid} {title0[:50]}: {err}')
            w.writerow([vid, '', title0, '', kind(title0, from_streams), '', 0, '', '', 'failed']); f.flush()
            continue
        title = info.get('title') or title0
        dur = int(info.get('duration') or 0)
        d = info.get('upload_date') or ''
        date = f'{d[:4]}-{d[4:6]}-{d[6:]}' if len(d) == 8 else ''
        typ = kind(title, from_streams, info.get('was_live'))
        text = ' '.join([title, info.get('description') or '', ' '.join(info.get('tags') or [])])
        if dur < MIN_SECONDS or not IDLEON.search(text):
            w.writerow([vid, date, title, round(dur / 60, 1), typ, '', 0, '', '', 'skipped']); f.flush(); continue
        if not lines:
            print(f'  [{i}/{len(queue)}] FAILED (no captions) {name} {date} {title[:50]}')
            w.writerow([vid, date, title, round(dur / 60, 1), typ, '', 0, '', '', 'failed']); f.flush(); continue
        cov, gap = coverage(lines, dur)
        status = 'ok' if cov >= 0.9 and gap <= 600 else 'partial'
        words = sum(len(t.split()) for _, t in lines)
        fn = os.path.join(ROOT, name, 'transcripts', f'{date or "nodate"}_{vid}.txt')
        with open(fn, 'w', encoding='utf-8') as out:
            out.write(f'title: {title}\nurl: https://www.youtube.com/watch?v={vid}\ndate: {date}\n'
                      f'duration_min: {round(dur / 60, 1)}\ntype: {typ}\ncaptions: {caps}\n---\n')
            out.write('\n'.join(f'[{ts(s)}] {t}' for s, t in lines))
        w.writerow([vid, date, title, round(dur / 60, 1), typ, caps, words, round(cov, 2), gap, status]); f.flush()
        print(f'  [{i}/{len(queue)}] {status} {name} {typ} {date} {title[:50]} ({words} words)')
        time.sleep(random.uniform(*PAUSE))
    for f, _ in files.values(): f.close()
    shutil.rmtree(TMP, ignore_errors=True)
    shutil.make_archive('idleon_transcripts', 'zip', 'idleon_transcripts')
    print('Done. Upload idleon_transcripts.zip to ChatGPT.')

if __name__ == '__main__':
    main()
