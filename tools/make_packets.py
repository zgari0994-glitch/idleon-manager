"""Build trimmed tagging packets for ChatGPT (no AI, pure code).

- 2s caption lines -> 30s paragraphs, one [HH:MM:SS] per paragraph
- strips um/uh/[Music] and doubled words
- streams (tier 6): keep only minutes within +-2 of a keyword hit
- order: Lane A videos first, then tag_priority.csv; already-tagged videos skipped
Output: handoff/packets/NNN_<video_id>.txt + handoff/packets/ORDER.csv
"""
import csv, glob, gzip, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CR = os.path.join(ROOT, 'sources/creators')
OUT = os.path.join(ROOT, 'handoff/packets')
LANE_A = ['ypb7kpQov30']  # afk_spots gap order; hole orders already tagged
BLOCK = 30
FILL = re.compile(r'\[(music|applause|laughter)\]|\b(um+|uh+|uhm|erm|hmm+)\b', re.I)
DUP = re.compile(r'\b(\w+)( \1\b)+', re.I)


def hms(s):
    return '%02d:%02d:%02d' % (s // 3600, s % 3600 // 60, s % 60)


def secs(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s


def tagged():
    return {os.path.basename(f)[:-4] for f in glob.glob(CR + '/*/tags/*.csv')} | \
           {os.path.basename(f)[:-4] for f in glob.glob(os.path.join(ROOT, 'handoff/tags_out/*.csv'))}


def hit_minutes(idx, vid):
    keep = set()
    for c in idx:
        if c['v'] == vid and c['s']:
            m = c['t'] // 60
            keep.update(range(m - 2, m + 3))
    return keep


def build(path, keep=None):
    head, body = open(path, encoding='utf-8', errors='ignore').read().split('\n---\n', 1)
    meta = dict(l.split(': ', 1) for l in head.splitlines() if ': ' in l)
    blocks, cur, start, skip0, lastkept = [], [], None, None, True
    for line in body.splitlines():
        m = re.match(r'\[(\d\d:\d\d:\d\d)\]\s*(.*)', line)
        if not m:
            continue
        t, txt = secs(m.group(1)), m.group(2)
        if keep is not None and t // 60 not in keep:
            if cur:
                blocks.append('[%s] %s' % (hms(start), ' '.join(cur))); cur = []
            if skip0 is None:
                skip0 = t
            continue
        if skip0 is not None:
            blocks.append('[skip %s-%s no system keywords]' % (hms(skip0), hms(t))); skip0 = None
        if start is None or t - start >= BLOCK:
            if cur:
                blocks.append('[%s] %s' % (hms(start), ' '.join(cur)))
            cur, start = [], t
        if txt:
            cur.append(txt)
    if cur:
        blocks.append('[%s] %s' % (hms(start), ' '.join(cur)))
    text = '\n'.join(blocks)
    text = DUP.sub(r'\1', FILL.sub('', text))
    text = re.sub(r' {2,}', ' ', text)
    return meta, text


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(OUT + '/*.txt'):
        os.remove(f)
    idx = json.load(gzip.open(CR + '/transcript_index.json.gz'))
    pri = list(csv.DictReader(open(CR + '/tag_priority.csv')))
    order = [r for v in LANE_A for r in pri if r['video_id'] == v] + [r for r in pri if r['video_id'] not in LANE_A]
    done = tagged()
    rows, before, after, n = [], 0, 0, 0
    for r in order:
        if r['video_id'] in done:
            continue
        src = os.path.join(CR, r['creator'], 'transcripts', r['file'])
        keep = hit_minutes(idx, r['video_id']) if r['tier'] == '6' else None
        meta, text = build(src, keep)
        n += 1
        name = '%03d_%s.txt' % (n, r['video_id'])
        hdr = 'video_id: %s\ncreator: %s\ndate: %s\ntitle: %s\nduration_min: %s\n---\n' % (
            r['video_id'], r['creator'], r['date'], meta.get('title', ''), meta.get('duration_min', ''))
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(hdr + text + '\n')
        before += len(open(src, encoding='utf-8', errors='ignore').read().split())
        after += len(text.split())
        rows.append([n, r['video_id'], r['creator'], r['date'], r['tier'], name])
    with open(OUT + '/ORDER.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['n', 'video_id', 'creator', 'date', 'tier', 'packet']); w.writerows(rows)
    print('packets', n, 'words before', before, 'after', after, 'cut %.0f%%' % (100 - 100 * after / before))


if __name__ == '__main__':
    main()
