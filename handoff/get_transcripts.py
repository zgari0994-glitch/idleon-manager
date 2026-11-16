"""Pull full, timestamped YouTube transcripts for IdleOn creators (Griffy, Pulse, Nocturne). LIGHTWEIGHT version.
Run on your own PC. Output: idleon_transcripts/sources/creators/<creator>/{transcripts/*.txt, index.csv}
plus idleon_transcripts.zip. Safe to stop and re-run: finished videos are skipped, failures retried.

Why it's light:
- Channel lists come from a few listing requests (title, length, approximate date). No per-video details call.
- Per video: only the transcript request (youtube-transcript-api). Nothing else.
- Videos whose title doesn't look like IdleOn are NOT fetched; they're listed as 'unclear' in index.csv to decide later.
- Reviews first across all three creators.

Setup (Windows, once):  py -m pip install -U yt-dlp youtube-transcript-api
Run:                    py get_transcripts.py
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
MIN_SECONDS = 120
PAUSE = (4, 8)
COOLDOWN = 900
SKIP_IDS = {'N2EFqfVHNMM'}  # 21-hour Remastered Movie (excluded by Zack)
IDLEON = re.compile(r'idle\s?on|lavaflame|\bw[1-7]\b|world [1-7]|master ?class|death ?bringer|wind ?walker|'
                    r'arcane cultist|royal guardian|voidwalker|vman|alchemy|sailing|divinity|summoning|sneaking|'
                    r'farming|breeding|spelunk|account review|roast|bingo', re.I)
ORDER = {'review': 0, 'guide': 1, 'playthrough': 2, 'stream': 3}
API = YouTubeTranscriptApi()

def kind(title, from_streams=False):
    t = (title or '').lower()
    if re.search(r'review|roast|bingo', t): return 'review'
    if from_streams: return 'stream'
    if re.search(r'\bep\.?\s?\d|episode|f2p guide|playthrough|next chapter', t): return 'playthrough'
    return 'guide'

def list_tab(url):
    opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True,
            'extractor_args': {'youtubetab': {'approximate_date': ['']}}}
    try:
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(url, download=False) or {}
    except Exception as ex:
        if 'does not have a' in str(ex): return []
        raise
    return [e for e in (info.get('entries') or []) if e and e.get('id')]

def ts(sec):
    s = int(sec); return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'

def coverage(lines, duration):
    if not lines or not duration: return 0.0, 0
    starts = [s for s, _ in lines]
    gaps = [b - a for a, b in zip(starts, starts[1:])] + [duration - starts[-1], starts[0]]
    return min(1.0, starts[-1] / duration), int(max(gaps))

def load_done(name):
    p = os.path.join(ROOT, name, 'index.csv')
    if not os.path.exists(p) or os.path.getsize(p) == 0: return set()
    with open(p, encoding='utf-8') as f:
        return {r['video_id'] for r in csv.DictReader(f) if r.get('status') in ('ok', 'partial', 'skipped', 'unclear')}

def writer(name):
    base = os.path.join(ROOT, name); os.makedirs(os.path.join(base, 'transcripts'), exist_ok=True)
    p = os.path.join(base, 'index.csv'); new = not os.path.exists(p) or os.path.getsize(p) == 0
    f = open(p, 'a', newline='', encoding='utf-8'); w = csv.writer(f)
    if new:
        w.writerow(['video_id', 'date', 'title', 'duration_min', 'type', 'captions', 'words', 'coverage', 'max_gap_s', 'status']); f.flush()
    return f, w

def main():
    pick = sys.argv[1:] or list(CREATORS)
    files = {name: writer(name) for name in pick}
    queue = []
    for name in pick:
        done = load_done(name); f, w = files[name]; n = unclear = 0
        for tab, from_streams in (('/videos', False), ('/streams', True)):
            for e in list_tab(CREATORS[name] + tab):
                vid, title, dur = e['id'], e.get('title') or '', int(e.get('duration') or 0)
                d = e.get('upload_date') or ''
                date = f'{d[:4]}-{d[4:6]}-{d[6:]}' if len(d) == 8 else ''
                if vid in done or vid in SKIP_IDS: continue
                if dur and dur < MIN_SECONDS: continue
                if not IDLEON.search(title):
                    w.writerow([vid, date, title, round(dur / 60, 1), '', '', 0, '', '', 'unclear']); unclear += 1; continue
                queue.append((ORDER[kind(title, from_streams)], name, vid, title, dur, date, from_streams)); n += 1
        f.flush()
        print(f'{name}: {n} to fetch, {unclear} unclear titles listed (not fetched), {len(done)} already done')
    queue.sort(key=lambda q: q[0])
    print(f'Total to fetch: {len(queue)}. Reviews first. Dates are approximate (from "x months ago").')
    for i, (_, name, vid, title, dur, date, from_streams) in enumerate(queue, 1):
        f, w = files[name]; typ = kind(title, from_streams)
        lines, caps, err = None, '', ''
        for attempt in range(3):
            try:
                t = API.fetch(vid, languages=['en', 'en-US', 'en-GB'])
                lines = [(s.start, s.text) for s in t]
                caps = 'auto' if getattr(t, 'is_generated', True) else 'manual'
                break
            except Exception as ex:
                err = f'{type(ex).__name__}: {str(ex)[:120]}'
                low = err.lower()
                if any(k in low for k in ('429', 'too many', 'blocked', 'requestblocked', 'ipblocked')):
                    print(f'  rate limited, cooling down {COOLDOWN // 60} min...'); time.sleep(COOLDOWN)
                elif any(k in low for k in ('disabled', 'notranscript', 'unavailable', 'no transcript')):
                    break
                else:
                    time.sleep(10 * (attempt + 1))
        if not lines:
            print(f'  [{i}/{len(queue)}] FAILED {name} {title[:50]}: {err[:80]}')
            w.writerow([vid, date, title, round(dur / 60, 1), typ, '', 0, '', '', 'failed']); f.flush()
            continue
        cov, gap = coverage(lines, dur)
        status = 'ok' if (not dur or (cov >= 0.9 and gap <= 600)) else 'partial'
        words = sum(len(x.split()) for _, x in lines)
        fn = os.path.join(ROOT, name, 'transcripts', f'{date or "nodate"}_{vid}.txt')
        with open(fn, 'w', encoding='utf-8') as out:
            out.write(f'title: {title}\nurl: https://www.youtube.com/watch?v={vid}\ndate: {date} (approx)\n'
                      f'duration_min: {round(dur / 60, 1)}\ntype: {typ}\ncaptions: {caps}\n---\n')
            out.write('\n'.join(f'[{ts(s)}] {x}' for s, x in lines))
        w.writerow([vid, date, title, round(dur / 60, 1), typ, caps, words, round(cov, 2), gap, status]); f.flush()
        print(f'  [{i}/{len(queue)}] {status} {name} {typ} {date} {title[:50]} ({words} words)')
        time.sleep(random.uniform(*PAUSE))
    for f, _ in files.values(): f.close()
    shutil.make_archive('idleon_transcripts', 'zip', 'idleon_transcripts')
    print('Done. Upload idleon_transcripts.zip to ChatGPT.')

if __name__ == '__main__':
    main()
