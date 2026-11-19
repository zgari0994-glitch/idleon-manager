#!/usr/bin/env bash
# Brother (IdleOnLech) refresh: raw save JSON -> throwaway copy of Zack's pipeline -> accounts/brother/ outputs.
# Zack's own files (snapshots/, plans/, model/*.json, dashboard/) are never written.
# Usage: accounts/brother/run.sh <raw.json>     (env: WORK=/tmp/bro_work)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
B="$REPO/accounts/brother"
W="${WORK:-/tmp/bro_work}"; mkdir -p "$W"
RAW="$1"

python3 - "$RAW" "$B/charnames.json" <<'EOF'
# Accept both shapes: profile JSON {data, charNames} or Toolbox "Copy raw data" (bare save, no names list).
# Bare saves get the stored slot order (charnames.json); refuse if the roster changed.
import sys, json
raw, cn = sys.argv[1], sys.argv[2]
j = json.load(open(raw))
if 'data' not in j:
    assert 'CogO' in j, 'not a Toolbox raw save'
    cog = j['CogO']; cog = json.loads(cog) if isinstance(cog, str) else cog
    names = {k[7:] for k in cog if k.startswith('Player_')}
    order = json.load(open(cn))
    assert names == set(order), f'roster changed: save has {sorted(names)}, stored order {order}. Upload once via the profile route or update charnames.json'
    j = {'data': j, 'charNames': order}
    json.dump(j, open(raw, 'w'))
else:
    assert j.get('charNames'), 'missing charNames'
    json.dump(j['charNames'], open(cn, 'w'))
print('raw ok:', len(j['charNames']), 'characters, first', j['charNames'][0])
EOF

# 1) fresh copy of the code, brother data linked in
rm -rf "$W/code"; mkdir -p "$W/code" "$B/snapshots" "$B/plans" "$B/state" "$B/dashboard"
(cd "$REPO" && tar --exclude=.git --exclude=./snapshots --exclude=./plans --exclude=./accounts -cf - .) | (cd "$W/code" && tar xf -)
ln -s "$B/snapshots" "$W/code/snapshots"; ln -s "$B/plans" "$W/code/plans"
cp "$B/jobs.yaml" "$W/code/model/jobs.yaml"
[ -f "$B/state/confirmed.json" ] || echo '{}' > "$B/state/confirmed.json"
cp "$B/state/confirmed.json" "$W/code/state/confirmed.json"
python3 "$B/patch_copy.py" "$W/code"

# 2) AutoReview's own code
if [ ! -d "$W/ar" ]; then
  git clone -q --depth 1 https://github.com/TwoSpookyBoos/IdleOnAutoReviewBot.git "$W/ar"
  [ "${INSTALL:-0}" = 1 ] && pip install -q -r "$W/ar/mysite/requirements/common.txt"
fi
export PYTHONPATH="$W/ar/mysite"
(cd "$W/ar/mysite" && python3 "$W/code/tools/run_ar.py" "$RAW" "$W/review.json" 2>/dev/null | tail -1)

# 3) snapshot (skip if this game save is already stored)
STAMP=$(python3 -c "import json;m=json.load(open('$W/review.json'))['meta'];print(m['game_save_utc'][:16].replace(':','').replace('-',''))")
D="$B/snapshots/$STAMP"
if [ -f "$D/meta.json" ] && [ "${FORCE:-0}" != 1 ]; then echo "save $STAMP already stored, nothing new"; exit 0; fi
mkdir -p "$D"
gzip -c "$RAW" > "$D/raw.json.gz"; gzip -c "$W/review.json" > "$D/review.json.gz"
cp "$W/review_chars.json" "$D/chars.json"; cp "$W/review_systems.json.gz" "$D/systems.json.gz"
python3 -c "import json;json.dump(json.load(open('$W/review.json'))['meta'],open('$D/meta.json','w'),indent=1)"
echo "$STAMP" > "$B/snapshots/LATEST"

# 4) same play-session steps as Zack's (CLAUDE.md), minus browser-only reads
cd "$W/code"
for s in model/ledger.py model/coins.py model/buffs.py model/mechanics.py rinse/rinse.py model/plan.py model/acquire.py model/dashboard.py; do
  python3 "$s" 2>&1 | tail -1 | sed "s|^|[$s] |"
done
cp "$W/code/dashboard/index.html" "$B/dashboard/index.html"
echo "brother dashboard built for save $STAMP"
