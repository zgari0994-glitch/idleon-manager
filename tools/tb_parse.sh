#!/usr/bin/env bash
# Toolbox numbers without the website (Zack 2026-11-25): update the Idleon Toolbox source, run its own parser
# on a snapshot's save, write snapshots/<save>/tb_parsed.json.gz. Usage: tools/tb_parse.sh [snapshot stamp]
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TB=/home/claude/work/tbsrc/IdleonToolbox
STAMP="${1:-$(cat "$REPO/snapshots/LATEST")}"; D="$REPO/snapshots/$STAMP"
if [ ! -d "$TB/.git" ]; then mkdir -p "$(dirname "$TB")"; git clone -q --depth 1 https://github.com/Morta1/IdleonToolbox.git "$TB"; fi
OLD=$(git -C "$TB" rev-parse HEAD); git -C "$TB" pull -q --ff-only || echo "WARN: Toolbox source update failed, using $OLD"
NEW=$(git -C "$TB" rev-parse HEAD)
if [ ! -d "$TB/node_modules" ] || ! git -C "$TB" diff --quiet "$OLD" "$NEW" -- package.json; then (cd "$TB" && npm install --ignore-scripts --no-audit --no-fund >/dev/null 2>&1); fi
cp "$REPO/tools/tbparse/zack.test.mjs" "$REPO/tools/tbparse/zack.config.mjs" "$TB/tools/parse-golden/"
(cd "$TB" && ZRAW="$D/raw.json.gz" ZOUT="$D/tb_parsed.json.gz" ZCOMMIT="$NEW" VITE_CONFIG_NATIVE_IGNORE_WARNING=true \
  npx vitest run --config tools/parse-golden/zack.config.mjs 2>&1 | grep -E "FAIL|Error" | head -5 || true)
test -s "$D/tb_parsed.json.gz" || { echo "ERROR: Toolbox parse produced nothing"; exit 1; }
echo "toolbox parse ok ($(git -C "$TB" log -1 --format='%cd' --date=short) source) -> snapshots/$STAMP/tb_parsed.json.gz"
