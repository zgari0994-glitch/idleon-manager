// Cog board plan from Idleon Toolbox's own construction optimizer (parsers/world-3/constructionOptimizer.ts),
// run on the snapshot's Toolbox parse with the Construction page defaults (weighted 1/1/1, max characters
// = min(2, owned), swap budgets 1/4/10/20). Replaces monoblos Cogtimizer (2023, breaks on Excogia/Yang cogs).
// Usage: node --experimental-strip-types tools/cog_plan.mjs <snapshot dir> [seconds=20]
import fs from 'node:fs'; import zlib from 'node:zlib'; import path from 'node:path';
const TB = process.env.TB || '/home/claude/work/tbsrc/IdleonToolbox';
const opt = await import(path.join(TB, 'parsers/world-3/constructionOptimizer.ts'));
const [, , dir, secs = '20'] = process.argv;
const d = JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(dir, 'tb_parsed.json.gz'))));
const c = d.account.construction;
const characters = d.characters.map(({ name, constructionExpPerHour }) => ({ name, constructionExpPerHour }));
const owned = opt.countBoardCharacters(c.baseBoard) + (c.spareCogs || []).filter(opt.isCharacterCog).length;
const weights = { totalBuildRate: 1, totalPlayerExpRate: 1, totalFlaggyRate: 1 };
const options = { stat: opt.WEIGHTED_STAT, weights, time: Math.round(+secs * 1000), characters,
  spareCogs: structuredClone(c.spareCogs || []), multipliers: c.boardMultipliers, maxCharacters: Math.min(2, owned) };
const now = opt.evaluateBoard(structuredClone(c.baseBoard), characters);
const curve = opt.optimizeSwapCurve(structuredClone(c.baseBoard), options);
const label = opt.cogSlotLabel;
const pick = (t) => t && ({ build: t.totalBuildRate, playerExp: t.totalPlayerExpRate, flaggy: t.totalFlaggyRate });
const plans = opt.curvePlans(curve).map((e) => ({
  swaps: e.maxSwaps ?? 'unlimited', gain: e.gain, totals: pick(e),
  moves: (e.moves ?? []).map((m) => ({ cog: m.name, from: label(m.fromIndex), to: label(m.to), displaced: m.displacedName }))
}));
const out = { source: 'Idleon Toolbox constructionOptimizer (page defaults)', toolbox_file_date: process.env.TBDATE || null,
  now: pick(curve.current ?? now), spares: (c.spareCogs || []).filter((x) => x && x.name !== 'Blank' && !opt.isCharacterCog(x)).length, maxCharacters: options.maxCharacters, weights, plans, best: opt.bestValuePlan(curve)?.maxSwaps ?? 'unlimited' };
fs.writeFileSync(path.join(dir, 'cog_plan.json'), JSON.stringify(out, null, 1));
console.log(JSON.stringify({ now: out.now, best: out.best, plans: plans.map((p) => ({ swaps: p.swaps, gain: p.gain, n: p.moves.length })) }));
