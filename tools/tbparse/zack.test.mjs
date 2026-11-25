// Runs Idleon Toolbox's own parser (Morta1/IdleonToolbox parsers/index.ts parseData) on one save.
// Copied into the Toolbox clone by tools/tb_parse.sh. Env: ZRAW = raw.json.gz, ZOUT = output .json.gz
import fs from 'node:fs';
import zlib from 'node:zlib';
import '../../polyfills';
import { parseData } from '@parsers/index';
import { clonePlain } from './snapshot.mjs';
it('parse save', () => {
  const fx = JSON.parse(zlib.gunzipSync(fs.readFileSync(process.env.ZRAW)).toString());
  // parse at the save's own time so timers/daily counters match the save, not "now"
  const t = (fx.data?.TimeAway && JSON.parse(fx.data.TimeAway).GlobalTime) || null;
  if (t) { vi.useFakeTimers({ toFake: ['Date'] }); vi.setSystemTime(new Date(t * 1000)); }
  const { account, characters } = parseData(fx.data ?? fx, fx.charNames ?? [], fx.companion ?? null, fx.guildData ?? null, fx.serverVars, fx.accountCreateTime, fx.tournament ?? null);
  const out = clonePlain({ account, characters, _meta: { parsed_at_save_time: t, toolbox_commit: process.env.ZCOMMIT || '' } });
  fs.writeFileSync(process.env.ZOUT, zlib.gzipSync(JSON.stringify(out)));
  if (t) vi.useRealTimers();
  console.log('PARSED sections', Object.keys(account).length, 'chars', characters.length);
});
