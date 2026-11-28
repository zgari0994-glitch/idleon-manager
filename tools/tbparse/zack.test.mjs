// Runs Idleon Toolbox's own parser (Morta1/IdleonToolbox parsers/index.ts parseData) on one save.
// Copied into the Toolbox clone by tools/tb_parse.sh. Env: ZRAW = raw.json.gz, ZOUT = output .json.gz
import fs from 'node:fs';
import zlib from 'node:zlib';
import '../../polyfills';
import { parseData } from '@parsers/index';
import { clonePlain } from './snapshot.mjs';
import { calcPrayerCost } from '@parsers/world-3/prayers';
import { CAULDRON_INFO, getBubbleBonus, getBubbleUpgradeCost, getCauldronBoostBonus, getVialsBonusByStat } from '@parsers/world-2/alchemy';
import { getAchievementStatus } from '@parsers/achievements';
import { growth } from '@utility/helpers';
import { baseTrackers } from '@utility/dashboard/baseTrackers';
import * as AA from '@utility/dashboard/account';
import * as CA from '@utility/dashboard/characters';
import { getDropRate } from '@parsers/character';
import { calcTotals } from '@parsers/world-3/printer';
import { getBuildCost, getExtraMaxLevels, getGildedBoostioBonus, getTotalGildedSlots } from '@parsers/world-3/construction';
import { getMaps, getOptimizedTesseractUpgrades, TESSERACT_UPGRADE_CATEGORIES } from '@parsers/class-specific/tesseract';
import { getOptimizedSpelunkingPowerUpgrades, getOptimizedSpelunkingAmberGainUpgrades } from '@parsers/world-7/spelunking';
import { getJadeUpgCost } from '@parsers/world-6/sneaking';
import { getEventShopRotation } from '@parsers/misc';

// ---- Zack 2026-11-28: numbers the website computes in its pages (pending "website-only" gaps)
const safe = (fn, fb = null) => { try { return fn(); } catch (e) { return { error: String(e).slice(0, 120) }; } };
const slim = (steps, n = 15) => (Array.isArray(steps) ? steps.slice(0, n).map((s) => {
  const o = {}; for (const k of ['name', 'index', 'level', 'nextLevel', 'cost', 'resourceType', 'x3', 'boneType', 'statChanges', 'readyHours', 'efficiency', 'affordable', 'category'])
    if (s?.[k] !== undefined) o[k] = s[k];
  if (s?.upgrade) { o.name ??= s.upgrade.name; o.index ??= s.upgrade.index; o.level ??= s.upgrade.level; }
  return o; }) : steps);
const buildings = (account) => {
  const speed = account?.construction?.totalBuildRate ?? 0;
  const atom = account?.atoms?.atoms?.find(({ name }) => name === 'Carbon_-_Wizard_Maximizer');
  const trimmed = getTotalGildedSlots(account); const boost = getGildedBoostioBonus(account);
  return { trimmedSlots: trimmed, trimmedBoost: boost, buildRate: speed, list: (account?.towers?.data ?? []).map((tw) => {
    const maxLevel = tw.maxLevel + getExtraMaxLevels(account, tw.maxLevel, atom?.level, tw?.index);
    const buildCost = getBuildCost(account?.towers, tw.level, tw.bonusInc, tw?.index);
    const isSlotTrimmed = tw.slot !== -1 && tw.slot < trimmed;
    return { name: tw.name, index: tw.index, level: tw.level, maxLevel, slot: tw.slot, inProgress: tw.inProgress, isSlotTrimmed,
      progress: tw.progress, buildCost, hoursLeft: speed ? (buildCost - tw.progress) / speed : null,
      trimmedHoursLeft: speed && boost ? (buildCost - tw.progress) / (boost * speed) : null };
  }) };
};
const websiteExtras = (account, characters) => {
  const out = {};
  out.dropRate = characters.map((c) => ({ name: c?.name, dropRate: safe(() => { const d = getDropRate(c, account, characters); return typeof d === 'object' ? (d?.dropRate ?? d?.value ?? d) : d; }) }));
  out.atomParticlesPerHour = safe(() => calcTotals(account)?.atom?.atoms ?? 0);
  out.buildings = safe(() => buildings(account));
  const cat = characters.find((c) => /Arcane/i.test(String(c?.class)));
  if (cat) {
    out.tesseractMaps = safe(() => getMaps(account, characters, cat));
    out.tesseractOptimizer = {};
    for (const k of Object.keys(TESSERACT_UPGRADE_CATEGORIES)) out.tesseractOptimizer[k] = safe(() => slim(getOptimizedTesseractUpgrades(cat, account, k, 15, { onlyAffordable: false, sharedFarmingTime: true })));
  }
  const sp = [...characters].sort((a, b) => (b?.skillsInfo?.spelunking?.level ?? 0) - (a?.skillsInfo?.spelunking?.level ?? 0))[0];
  if (sp) out.spelunkingOptimizer = { character: sp.name,
    power: safe(() => slim(getOptimizedSpelunkingPowerUpgrades(sp, account, 15, {}))),
    amber: safe(() => slim(getOptimizedSpelunkingAmberGainUpgrades(sp, account, 15, {}))) };
  out.ninjaUpgradeCosts = safe(() => (account?.sneaking?.upgrades || []).map((u, i) => ({ index: i, name: u.name, level: u.level, unlocked: u.isUnlocked,
    cost: safe(() => getJadeUpgCost(account, characters, i, u.level)) })));
  out.eventShop = safe(() => getEventShopRotation(account));
  return out;
};

// ---- Zack 2026-11-27: bubble costs, same math as Toolbox's Bubbles page (pages/account/world-2/bubbles.jsx materialCost)
const CROPS = { W6item1: 4, W6item2: 30, W6item3: 46, W6item4: 72, W6item5: 99 };
const ESSENCES = { W6item6: 0, W6item7: 1, W6item8: 2, W6item9: 3, W6item10: 4 };
const owned = (account, rawName = '') => {
  const liquid = rawName.match(/^Liquid(\d)$/)?.[1];
  if (liquid) return Number(account?.alchemy?.liquids?.[liquid - 1] ?? 0);
  if (rawName === 'Bits') return Number(account?.gaming?.bits ?? 0);
  if (rawName.startsWith('SailTr')) return Number(account?.sailing?.lootPile?.find(({ rawName: r }) => r === rawName.replace('SailTr', 'SailT'))?.amount ?? 0);
  if (rawName.startsWith('W6item')) {
    if (Object.hasOwn(CROPS, rawName)) return Number(account?.farming?.crop?.[CROPS[rawName]] ?? 0);
    return Object.hasOwn(ESSENCES, rawName) ? Number(account?.summoning?.essences?.[ESSENCES[rawName]] ?? 0) : null;
  }
  if (rawName.startsWith('W7item')) return Number(account?.spelunking?.discoveries?.flat()?.[Number(rawName.replace('W7item', ''))]?.amount ?? 0);
  return Number(account?.storage?.list?.find(({ rawName: r }) => r === rawName)?.amount ?? 0);
};
const matCost = (account, { index, cauldron }, level, { rawName, baseCost }) => {
  const bubbles = account?.alchemy?.bubbles?.[cauldron];
  const cauldronCostLvl = account?.alchemy?.cauldrons?.[cauldron]?.boosts?.cost?.level || 0;
  const multiBubble = cauldron !== 'kazam' ? bubbles?.[16]?.level || 0 : 0;
  const lastBubbleLvl = bubbles?.[14]?.level || 0;
  const vb = getVialsBonusByStat(account?.alchemy?.vials, 'AlchBubbleCost') + getBubbleBonus(account, 'UNDEVELOPED_COSTS', false);
  return getBubbleUpgradeCost({ rawName, bubbleIndex: index, level, baseCost, discounts: {
    cauldronBubble: Math.max(0.05, 1 - (growth('decay', lastBubbleLvl, 40, 12, false) / 100) * growth('decayMulti', multiBubble, 1.4, 30, false)),
    cauldronLevel: Math.max(0.1, 1 - getCauldronBoostBonus(CAULDRON_INFO.findIndex(({ name }) => name === cauldron), 2, cauldronCostLvl) / 100),
    vialAndBubble: Math.max(0.05, 1 - vb / 100), bargainTag: 1,
    smrt: Math.max(0.9, 1 - 0.1 * getAchievementStatus(account?.achievements, 108)) } });
};
const bubbleCosts = (account) => Object.values(account?.alchemy?.bubbles || {}).flat().filter((b) => (b?.level || 0) > 0).map((b) => {
  const mats = (b.itemReq || []).filter((i) => i?.rawName && !['Blank', 'ERROR'].includes(i.rawName));
  const next = mats.map((m) => ({ rawName: m.rawName, name: m.name, cost: matCost(account, b, b.level, m), owned: owned(account, m.rawName) }));
  // levels affordable now: walk level by level until any material runs out (cap 2000 levels)
  const left = Object.fromEntries(next.map((m) => [m.rawName, m.owned ?? 0]));
  let n = 0;
  for (; n < 2000; n++) {
    const c = mats.map((m) => [m.rawName, matCost(account, b, b.level + n, m)]);
    if (c.some(([r, v]) => left[r] < v)) break;
    c.forEach(([r, v]) => { left[r] -= v; });
  }
  const limit = next.slice().sort((x, y) => (x.owned ?? 0) / (x.cost || 1) - (y.owned ?? 0) / (y.cost || 1))[0];
  return { name: b.bubbleName, cauldron: b.cauldron, index: b.index, level: b.level, next, affordable: n, limitedBy: limit?.name };
});
// ---- Toolbox's own dashboard alerts with default trackers (utility/dashboard), same as hooks/useAlerts.jsx
const ACC = { General: AA.getGeneralAlerts, 'World 1': AA.getWorld1Alerts, 'World 2': AA.getWorld2Alerts, 'World 3': AA.getWorld3Alerts,
  'World 4': AA.getWorld4Alerts, 'World 5': AA.getWorld5Alerts, 'World 6': AA.getWorld6Alerts, 'World 7': AA.getWorld7Alerts };
const CHR = { anvil: CA.anvilAlerts, worship: CA.worshipAlerts, traps: CA.trapsAlerts, quests: CA.questsAlerts, alchemy: CA.alchemyAlerts,
  obols: CA.obolsAlerts, postOffice: CA.postOfficeAlerts, starSigns: CA.starSignsAlerts, tools: CA.toolsAlerts, talents: CA.talentsAlerts,
  cards: CA.cardsAlert, divinityStyle: CA.getDivinityAlert, divinityLink: CA.divinityLinkAlert, rightHand: CA.rightHandAlerts,
  equipment: CA.getEquipmentAlert, bags: CA.bagsAlerts, classSpecific: CA.classSpecificAlerts };
const toolboxAlerts = (account, characters, lastUpdated) => {
  const out = { account: {}, characters: [], failed: [] };
  for (const [section, fields] of Object.entries(baseTrackers.account || {})) {
    if (!ACC[section]) continue;
    try { out.account[section] = ACC[section](account, fields, AA.getOptions(fields), characters, lastUpdated, {}) || {}; }
    catch (e) { out.failed.push(section + ': ' + String(e).slice(0, 80)); }
  }
  const tr = baseTrackers.characters || {};
  const options = Object.entries(tr).reduce((r, [k, d]) => ({ ...r, [k]: { ...d, ...(d?.options || []).reduce((a, o) => ({ ...a, [o?.name]: o }), {}) } }), {});
  characters.forEach((ch) => {
    const a = {};
    for (const k of Object.keys(options)) {
      if (!options[k]?.checked || !CHR[k]) continue;
      try { a[k] = CHR[k](account, characters, ch, lastUpdated, options) || {}; } catch (e) { out.failed.push(ch?.name + ' ' + k + ': ' + String(e).slice(0, 80)); }
    }
    out.characters.push({ name: ch?.name, alerts: a });
  });
  return out;
};
it('parse save', () => {
  const fx = JSON.parse(zlib.gunzipSync(fs.readFileSync(process.env.ZRAW)).toString());
  // parse at the save's own time so timers/daily counters match the save, not "now"
  const t = (fx.data?.TimeAway && JSON.parse(fx.data.TimeAway).GlobalTime) || null;
  if (t) { vi.useFakeTimers({ toFake: ['Date'] }); vi.setSystemTime(new Date(t * 1000)); }
  const { account, characters } = parseData(fx.data ?? fx, fx.charNames ?? [], fx.companion ?? null, fx.guildData ?? null, fx.serverVars, fx.accountCreateTime, fx.tournament ?? null);
  // extras the website computes in its pages, added with Toolbox's own functions (Zack 2026-11-25)
  try { (account.prayers || []).forEach((p) => { p.nextCost = calcPrayerCost(p); }); } catch (e) { console.log('extra prayers failed', e); }
  account._zack = {};
  try { account._zack.bubbleCosts = bubbleCosts(account); } catch (e) { console.log('extra bubbleCosts failed', e); account._zack.bubbleCostsError = String(e); }
  try { account._zack.web = websiteExtras(account, characters); } catch (e) { console.log('extra web failed', e); account._zack.webError = String(e); }
  try { account._zack.alerts = toolboxAlerts(account, characters, (t || Date.now() / 1000) * 1000); } catch (e) { console.log('extra alerts failed', e); account._zack.alertsError = String(e); }
  const out = clonePlain({ account, characters, _meta: { parsed_at_save_time: t, toolbox_commit: process.env.ZCOMMIT || '' } });
  fs.writeFileSync(process.env.ZOUT, zlib.gzipSync(JSON.stringify(out)));
  if (t) vi.useRealTimers();
  console.log('PARSED sections', Object.keys(account).length, 'chars', characters.length);
});
