"""Step 1 of the Apify transcript run: list every IdleOn video from Griffy, Pulse and Nocturne.
No transcripts are fetched here (listing is not rate limited the way transcripts were).

Run in Downloads:  py list_videos.py
Writes: idleon_transcripts\\video_list.csv (every video with include = yes/no and why)
"""
import csv, os, re
import yt_dlp

CREATORS = {
    'griffybit': 'https://www.youtube.com/channel/UCt5WC8O9Jrb-UeNcI5T9BoQ',
    'pulseidle': 'https://www.youtube.com/@PulseIdle',
    'nocturne': 'https://www.youtube.com/@NocturneGamingOfficial',
}
ALL_IDLEON = {'pulseidle'}  # IdleOn-only channel (Griffy posts other games too)
MIN_SECONDS = 120
SKIP_IDS = set()  # nothing excluded. N2EFqfVHNMM = Griffy's 21-hour F2P Remastered Movie: kept, flagged for Zack
IDLEON = re.compile(r'idle\s?on|lavaflame|\bw[1-7]\b|world [1-7]|master ?class|death ?bringer|wind ?walker|'
                    r'arcane cultist|royal guardian|voidwalker|vman|alchemy|sailing|divinity|summoning|sneaking|'
                    r'farming|breeding|spelunk|account review|roast|bingo|\brg\b|manic|purity|grimoire|compass|'
                    r'tesseract|research|sushi|jelly|clam|menagerie|zenith|statue|caverns?|the hole|gaming|lab\b|'
                    r'equinox|vault|shimmerfin|emperor|kattlekruk|cranium|legendary points|kpk|f2p', re.I)
ROOT = 'idleon_transcripts'
NOCTURNE_OK = re.compile(r'idle\s?on', re.I)
# Nocturne posts other games too. Titles with IdleOn keywords but no "IdleOn" are kept as 'check' (reviewed by hand),
# unless they name one of his other games.
OTHER_GAMES = re.compile(r'golf|valheim|forts|zomboid|risk of rain|deep rock|throne and liberty|move or die|content warning|'
                         r'lovers in a dangerous|subscriber|milestone|minecraft|lethal company|phasmophobia|stream raiders|pok[eé]mon|nuzlocke|'
                         r'archvale|shovel knight|skul|vexlands|all hail the orb|lay of the land|scale the depths|pixel art|'
                         r'phoenix point|ape escape|gacha|early access|\bfps\b|crit.s challenge|this ant|i am griffybit', re.I)


def kind(title, from_streams):
    t = (title or '').lower()
    if re.search(r'review|roast|bingo', t): return 'review'
    if from_streams: return 'stream'
    if re.search(r'\bep\.?\s?\d|episode|f2p|playthrough|next chapter|beginner', t): return 'playthrough'
    return 'guide'


def list_tab(url, tries=3):
    for t in range(tries):
        got = _list_tab(url)
        if got is None: return []  # channel has no such tab
        if got: return got
        print(f'  {url}: 0 videos, retrying ({t + 1}/{tries})')
    return []


def _list_tab(url):
    opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True,
            'extractor_args': {'youtubetab': {'approximate_date': ['']}}}
    try:
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(url, download=False) or {}
    except Exception as ex:
        if 'does not have a' in str(ex): return None
        raise
    return [e for e in (info.get('entries') or []) if e and e.get('id')]


def main():
    os.makedirs(ROOT, exist_ok=True)
    out = os.path.join(ROOT, 'video_list.csv')
    rows, seen = [], set()
    for name, url in CREATORS.items():
        for tab, from_streams in (('/videos', False), ('/streams', True)):
            entries = list_tab(url + tab)
            print(f'  {name}{tab}: {len(entries)} found')
            for e in entries:
                vid, title, dur = e['id'], e.get('title') or '', int(e.get('duration') or 0)
                if vid in seen: continue  # same video in both tabs
                seen.add(vid)
                d = e.get('upload_date') or ''
                date = f'{d[:4]}-{d[4:6]}-{d[6:]}' if len(d) == 8 else ''
                if vid in SKIP_IDS: why, inc = 'excluded by Zack', 'no'
                elif dur and dur < MIN_SECONDS: why, inc = 'under 2 min', 'no'
                elif name in ALL_IDLEON or NOCTURNE_OK.search(title): why, inc = 'idleon', 'yes'
                elif name == 'griffybit' and from_streams: why, inc = 'griffy stream (idleon)', 'yes'
                elif IDLEON.search(re.sub(r'nocturne\s*gaming', '', title, flags=re.I)) and not OTHER_GAMES.search(title): why, inc = 'keyword match, check by hand', 'check'
                else: why, inc = 'title not idleon', 'no'
                if vid == 'N2EFqfVHNMM': why = 'idleon (21-hour F2P Remastered Movie: confirm with Zack)'
                rows.append([name, vid, date, title, round(dur / 60, 1), kind(title, from_streams), tab[1:], inc, why])
        print(f'{name}: listed')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['creator', 'video_id', 'date', 'title', 'duration_min', 'type', 'tab', 'include', 'why'])
        w.writerows(rows)
    yes = [r for r in rows if r[7] == 'yes']; chk = [r for r in rows if r[7] == 'check']
    print(f'Done: {len(rows)} videos listed, {len(yes)} IdleOn videos, {len(chk)} to check by hand. File: {out}')


if __name__ == '__main__':
    main()
