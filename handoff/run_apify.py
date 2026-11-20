"""Step 2: fetch transcripts for every video in final_video_list.csv through Apify.

Setup (once): sign up at apify.com, copy your API token (Settings > Integrations), then in a command window:
    setx APIFY_TOKEN "your-token"
Close that window and open a new one. The token stays on this PC.

Run in Downloads:  py run_apify.py
Writes the same layout as before:
    idleon_transcripts\\sources\\creators\\<creator>\\transcripts\\<date>_<id>.txt
    idleon_transcripts\\sources\\creators\\<creator>\\index.csv
Already-saved transcripts are skipped. Spending is capped per batch and in total.
"""
import csv, json, os, shutil, sys, time, urllib.request

ACTOR = 'om_kh~youtube-transcript-api'
FALLBACK_ACTOR = 'apihq~youtube-transcript-scraper'  # used for whatever the main actor could not do (e.g. very long videos)
API = 'https://api.apify.com/v2'
LIST = os.path.join('idleon_transcripts', 'final_video_list.csv')
ROOT = os.path.join('idleon_transcripts', 'sources', 'creators')
BATCH = 20   # 100-video runs failed on Apify; 20 worked
BATCH_CAP_USD = 1.00
TOTAL_CAP_USD = 3.00
# Optional:  py run_apify.py --list <csv> --cap <usd>   (e.g. the will309 list, sources/creators/will309/video_list.csv)
if '--list' in sys.argv: LIST = sys.argv[sys.argv.index('--list') + 1]
if '--cap' in sys.argv: TOTAL_CAP_USD = float(sys.argv[sys.argv.index('--cap') + 1])


def call(method, path, token, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode() or '{}')


def ts(sec):
    s = int(sec or 0); return f'{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}'


def done_ids():
    ids = set()
    for name in os.listdir(ROOT) if os.path.isdir(ROOT) else []:
        tdir = os.path.join(ROOT, name, 'transcripts')
        if os.path.isdir(tdir):
            for fn in os.listdir(tdir):
                if fn.endswith('.txt') and os.path.getsize(os.path.join(tdir, fn)) > 500:
                    ids.add(fn[:-4].split('_', 1)[1] if '_' in fn else fn[:-4])
    return ids


def save(item, meta):
    name, typ = meta['creator'], meta['type']
    vid = item.get('video_id') or meta['video_id']
    segs = item.get('segments') or []
    title = item.get('title') or meta['title']
    date = (item.get('published_at') or '')[:10]
    dur = item.get('video_length_seconds') or 0
    words = item.get('word_count') or sum(len((s.get('text') or '').split()) for s in segs)
    base = os.path.join(ROOT, name); tdir = os.path.join(base, 'transcripts'); os.makedirs(tdir, exist_ok=True)
    with open(os.path.join(tdir, f'{date or "nodate"}_{vid}.txt'), 'w', encoding='utf-8') as out:
        out.write(f'title: {title}\nurl: https://www.youtube.com/watch?v={vid}\ndate: {date}\n'
                  f'duration_min: {round(dur / 60, 1)}\ntype: {typ}\ncaptions: {"auto" if item.get("is_generated", True) else "manual"}\n---\n')
        if segs:
            out.write('\n'.join(f'[{ts(s.get("start"))}] {(s.get("text") or "").strip()}' for s in segs))
        else:
            out.write(item.get('text') or '')
    idx = os.path.join(base, 'index.csv'); new = not os.path.exists(idx) or os.path.getsize(idx) == 0
    with open(idx, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if new: w.writerow(['video_id', 'date', 'title', 'duration_min', 'type', 'captions', 'words', 'coverage', 'max_gap_s', 'status'])
        w.writerow([vid, date, title, round(dur / 60, 1), typ, 'auto' if item.get('is_generated', True) else 'manual', words, '', '', 'ok'])


def normalize_fallback(it):
    md = it.get('metadata') or {}
    return {'video_id': it.get('video_id'), 'title': md.get('title'), 'video_length_seconds': md.get('duration_seconds') or 0,
            'is_generated': it.get('is_auto_generated', True), 'segments': it.get('transcript') or [], 'published_at': ''}


def run_fallback(token, todo):
    print(f'Fallback actor for {len(todo)} remaining videos...')
    saved, missing = 0, []
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]; by_id = {r['video_id']: r for r in batch}
        run = call('POST', f'/acts/{FALLBACK_ACTOR}/runs', token,
                   {'videoIds': list(by_id), 'language': 'en', 'maxTotalChargeUsd': 0.50})['data']
        while run['status'] in ('READY', 'RUNNING'):
            time.sleep(15); run = call('GET', f'/actor-runs/{run["id"]}', token)['data']
        items = call('GET', f'/datasets/{run["defaultDatasetId"]}/items?clean=1&format=json', token)
        items = items if isinstance(items, list) else items.get('data', [])
        got = set()
        for it in items:
            vid = it.get('video_id')
            if it.get('success') and vid in by_id and it.get('transcript'):
                save(normalize_fallback(it), by_id[vid]); got.add(vid); saved += 1
            elif vid in by_id:
                print(f'  {by_id[vid]["title"][:55]}: {it.get("code") or it.get("error") or "no transcript"}')
        missing += [by_id[v]['title'] for v in by_id if v not in got]
        print(f'  run {run["status"]}: saved {len(got)}/{len(batch)}')
    return saved, missing


def main():
    token = os.environ.get('APIFY_TOKEN')
    if not token: sys.exit('APIFY_TOKEN not set. Run:  setx APIFY_TOKEN "your-token"  then open a NEW command window.')
    with open(LIST, encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    have = done_ids()
    todo = [r for r in rows if r['video_id'] not in have]
    if '--fallback' in sys.argv:
        saved, missing = run_fallback(token, todo)
        print(f'Done: {saved} saved by fallback, {len(missing)} still missing.')
        with open(os.path.join('idleon_transcripts', 'missing.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(missing))
        shutil.make_archive('idleon_transcripts', 'zip', 'idleon_transcripts'); print('Zipped: idleon_transcripts.zip')
        return
    # very long videos (e.g. the 21-hour F2P movie) go last, one per run, so they can't sink a whole batch
    long_ = [r for r in todo if float(r.get('duration_min') or 0) > 180]
    todo = [r for r in todo if r not in long_]
    print(f'{len(rows)} videos on the list, {len(rows) - len(todo)} already saved, {len(todo)} to fetch.')
    spent, saved, missing = 0.0, 0, []
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)] + [[r] for r in long_]
    for n, batch in enumerate(batches, 1):
        if spent >= TOTAL_CAP_USD: print(f'Total cap ${TOTAL_CAP_USD} reached, stopping.'); break
        by_id = {r['video_id']: r for r in batch}
        body = {'videos': [f'https://www.youtube.com/watch?v={r["video_id"]}' for r in batch],
                'includeSegments': True, 'language': 'en', 'maxTotalChargeUsd': min(BATCH_CAP_USD, TOTAL_CAP_USD - spent)}
        run = call('POST', f'/acts/{ACTOR}/runs', token, body)['data']
        print(f'Batch {n}/{len(batches)}: {len(batch)} videos, run {run["id"]} started...')
        while run['status'] in ('READY', 'RUNNING'):
            time.sleep(15); run = call('GET', f'/actor-runs/{run["id"]}', token)['data']
        if run['status'] != 'SUCCEEDED':
            print(f'  run ended {run["status"]}: {run.get("statusMessage") or "no message"}; saving whatever it returned.')
            try:
                req = urllib.request.Request(f'{API}/actor-runs/{run["id"]}/log', headers={'Authorization': f'Bearer {token}'})
                with urllib.request.urlopen(req, timeout=60) as r:
                    print('  last log lines:\n    ' + '\n    '.join(r.read().decode(errors='ignore').strip().splitlines()[-8:]))
            except Exception as ex:
                print(f'  (could not read log: {ex})')
        items = call('GET', f'/datasets/{run["defaultDatasetId"]}/items?clean=1&format=json', token)
        items = items if isinstance(items, list) else items.get('data', [])
        got = set()
        for it in items:
            vid = it.get('video_id')
            if vid in by_id and (it.get('segments') or it.get('text')):
                save(it, by_id[vid]); got.add(vid); saved += 1
        missing += [by_id[v]['title'] for v in by_id if v not in got]
        spent += max(float(run.get('usageTotalUsd') or 0), 0.005 * len(got))  # conservative
        print(f'  saved {len(got)}/{len(batch)}  (spent so far about ${spent:.2f})')
    print(f'Done: {saved} transcripts saved, {len(missing)} without captions/failed, about ${spent:.2f} spent.')
    if missing:
        with open(os.path.join('idleon_transcripts', 'missing.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(missing))
        print('List of missing ones: idleon_transcripts\\missing.txt')
    shutil.make_archive('idleon_transcripts', 'zip', 'idleon_transcripts')
    print('Zipped: idleon_transcripts.zip (for ChatGPT)')


if __name__ == '__main__':
    main()
