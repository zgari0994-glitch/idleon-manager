"""Validate ChatGPT packet tags (handoff/tags_out) and write full-spec CSVs to sources/creators/<c>/tags/.
Run on "check tags". Prints per-video row counts, errors and rows/min."""
import csv, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = open(os.path.join(ROOT, 'handoff/tagging_spec.md'), encoding='utf-8').read()
PAGES = dict(re.findall(r'`([a-z_0-9]+)`=([a-z0-9/-]*)', SPEC))
CARD = open(os.path.join(ROOT, 'handoff/TAGGER.md'), encoding='utf-8').read()
SYSTEMS = set(CARD.split('## Systems')[1].split('##')[0].split())
TYPES = set('priority blocker target threshold how_to setup afk_spot active_task mechanic skip warning comparison meta_change account_note opinion'.split())
OUTCOLS = 'video_id,creator,date,t_start,t_end,system,toolbox_page,subsystem,class,claim_type,stage,numbers,statement,explicit,confidence'.split(',')
TS = re.compile(r'^\d\d:\d\d:\d\d$')

order = {r['video_id']: r for r in csv.DictReader(open(os.path.join(ROOT, 'handoff/packets/ORDER.csv')))}
tot = bad = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'handoff/tags_out/*.csv'))):
    vid = os.path.basename(f)[:-4]
    o = order.get(vid)
    if not o:
        print('?? not in ORDER', vid); continue
    pk = open(os.path.join(ROOT, 'handoff/packets', o['packet']), encoding='utf-8').read()
    dur = float(re.search(r'duration_min: ([\d.]*)', pk).group(1) or 0)
    out, errs = [], []
    for i, r in enumerate(csv.DictReader(open(f, encoding='utf-8'))):
        r = {k.strip(): (v or '').strip() for k, v in r.items() if k}
        for s in (r.get('system') or 'general').split('|'):
            s = s.strip()
            e = []
            if s not in SYSTEMS: e.append('system=' + s)
            if r.get('claim_type') not in TYPES and s != 'none': e.append('type=' + r.get('claim_type', ''))
            if not TS.match(r.get('t_start', '')): e.append('t_start')
            if not r.get('statement'): e.append('statement')
            if e: errs.append('row %d: %s' % (i + 2, ','.join(e)))
            row = dict(r, video_id=vid, creator=o['creator'], date=o['date'], system=s, toolbox_page=PAGES.get(s, ''))
            out.append({k: row.get(k, '') for k in OUTCOLS})
    dst = os.path.join(ROOT, 'sources/creators', o['creator'], 'tags', vid + '.csv')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, OUTCOLS); w.writeheader(); w.writerows(out)
    tot += 1; bad += bool(errs)
    print('%s %s rows=%d (%.1f/min) %s' % (o['n'], vid, len(out), len(out) / dur if dur else 0, '; '.join(errs[:5]) or 'ok'))
print('videos', tot, 'with errors', bad, 'left', len(order) - tot)
