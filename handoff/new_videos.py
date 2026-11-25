"""New creator videos only (Zack 2026-11-25). Run after list_videos.py, in Downloads:  py new_videos.py
Reads idleon_transcripts\\video_list.csv (fresh channel listing) and idleon_transcripts\\final_video_list.csv
(everything already fetched), writes idleon_transcripts\\new_video_list.csv = include=yes videos not fetched yet.
"""
import csv, os
ROOT = 'idleon_transcripts'
have = set()
fin = os.path.join(ROOT, 'final_video_list.csv')
if os.path.exists(fin):
    with open(fin, encoding='utf-8') as f:
        have = {r['video_id'] for r in csv.DictReader(f)}
with open(os.path.join(ROOT, 'video_list.csv'), encoding='utf-8') as f:
    rows = [r for r in csv.DictReader(f) if r.get('include') == 'yes' and r['video_id'] not in have]
cols = ['creator', 'video_id', 'title', 'duration_min', 'type', 'tab']
with open(os.path.join(ROOT, 'new_video_list.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
by = {}
for r in rows: by[r['creator']] = by.get(r['creator'], 0) + 1
print(f"{len(rows)} new videos to fetch: {by}")
