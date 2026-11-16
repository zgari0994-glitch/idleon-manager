#!/usr/bin/env bash
# Full refresh after a browser pull: decode -> AutoReview code -> store snapshot in git.
# Usage: tools/snapshot.sh <tool_result_file>
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
W=/home/claude/work; mkdir -p "$W"
python3 "$REPO/tools/decode_pull.py" "$1" "$W/live.json"
if [ ! -d "$W/ar" ]; then
  git clone -q --depth 1 https://github.com/TwoSpookyBoos/IdleOnAutoReviewBot.git "$W/ar"
  pip install --break-system-packages -q -r "$W/ar/mysite/requirements/common.txt" coloredlogs python-dotenv beautifulsoup4 lxml >/dev/null 2>&1
fi
(cd "$W/ar/mysite" && PYTHONPATH=. python3 "$REPO/tools/run_ar.py" "$W/live.json" "$W/review.json" 2>/dev/null | tail -1)
STAMP=$(python3 -c "import json;m=json.load(open('$W/review.json'))['meta'];print(m['game_save_utc'][:16].replace(':','').replace('-',''))")
D="$REPO/snapshots/$STAMP"; mkdir -p "$D"
gzip -c "$W/live.json" > "$D/raw.json.gz"; gzip -c "$W/review.json" > "$D/review.json.gz"
python3 -c "import json;json.dump(json.load(open('$W/review.json'))['meta'],open('$D/meta.json','w'),indent=1)"
echo "$STAMP" > "$REPO/snapshots/LATEST"
echo "saved snapshots/$STAMP"
