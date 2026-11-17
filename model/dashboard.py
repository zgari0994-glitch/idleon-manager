"""Build the dashboard page from the latest plan + mechanics -> dashboard/index.html (self-contained).
Publish/republish with the artifacts publish_files tool (slug in dashboard/ARTIFACT)."""
import json, gzip, os, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
plan = json.load(open(os.path.join(R, 'plans', 'latest.json')))
mech = json.load(open(os.path.join(R, 'model', 'mechanics.json')))
review = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'review.json.gz')))
secs = {s['name']: s['tier'] for w in review['worlds'] for s in w['sections']}
rinse = json.load(open(os.path.join(R, 'rinse', 'latest.json')))
tp = os.path.join(R, 'snapshots', stamp, 'timers.json')
timers = json.load(open(tp)) if os.path.exists(tp) else None
acq = json.load(open(os.path.join(R, 'model', 'acquire.json')))
spots = {c['name']: c for c in (timers or {}).get('characters', [])}
for c in plan['cards']:
    sp = spots.get(c['name'])
    if sp: c['afk_now'] = f"{sp['spot']} ({sp['afk_for']})"

side = {
    'stage': {'high': secs.get('Pinchy high'), 'low': secs.get('Pinchy low')},
    'watch': [
        'Royal Guardian x2: unlock ASAP (250 orb at Bored Beans), don\'t push early (Griffy)',
        'Elite Class Swap Token: watch gem shop -> Autistronaut to Arcane Cultist',
        'Idle Skilling (Steam): slow roll for the Idle Skiller trophy; first character name = Autiszemo',
        
    ],
    'trophies_missing': mech['gallery_missing'].get('trophy', []),
    'capes_missing': mech['capes_missing'],
    'ach': {'done': mech['achievements_done'], 'open': len(mech['achievements_open'])},
    'companions': len(mech['companions']),
    'packs': len(mech['packs_owned']),
    'gaps': [{'score': r['score'], 'section': r['section'], 'label': r['label'][:90], 'cur': r['cur'], 'goal': r['goal']} for r in rinse['by_section'][:12]],
    'timers': timers,
    'ingame': {k: [x['name'] + ' (' + (x.get('bonus') or '') + ')' for x in acq[k] if x['kind'] == 'in-game'] for k in ('trophies', 'nametags', 'hats')},
    'doot': next((c['effect'] for c in mech['companions'] if c['name'] == 'King Doot'), ''),
}
data = {'account': plan.get('account', {}), 'meta': plan['meta'], 'cards': sorted(plan['cards'], key=lambda c: c['slot']), 'side': side, 'stamp': stamp}

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IdleOn Manager</title>
<style>
:root{--bg:#1c1220;--panel:#271a2d;--line:#3d2b45;--ink:#efe6f2;--mute:#a993b3;--gold:#e2b857;--em:#3fbf8f;--warn:#e07a5f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:13px/1.45 system-ui,-apple-system,Segoe UI,sans-serif}
header{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:baseline;padding:12px 16px;border-bottom:1px solid var(--line)}
h1{font-size:16px;margin:0;color:var(--gold);letter-spacing:.3px}.pill{color:var(--mute)}.pill b{color:var(--ink);font-weight:600}
.age.old b{color:var(--warn)}
main{display:grid;grid-template-columns:55fr 45fr;gap:14px;padding:14px 16px}
@media(max-width:860px){main{grid-template-columns:1fr}}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:10px;align-content:start}
.card,.box{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 11px}
.card h2{font-size:13px;margin:0 0 2px;display:flex;justify-content:space-between;gap:6px}.card h2 span{color:var(--gold)}
.sub{color:var(--mute);font-size:12px;margin-bottom:6px}.flag{color:var(--warn);font-size:12px;margin:2px 0}
.job{margin-top:6px}.job>.t{font-weight:600}.job .tier{color:var(--mute);font-weight:400;font-size:12px}
.job ul{list-style:none;margin:3px 0 0;padding:0}.job li{display:flex;gap:6px;align-items:flex-start;font-size:12px;color:#d9cde0;padding:1px 0}
.job li input{accent-color:var(--em);margin-top:2px}.job li.done span{text-decoration:line-through;color:var(--mute)}
.job li.done span::before{content:"✓ ";color:var(--em)}
.arrow{color:var(--em)}.move,.quick,.act,.afk,.lock{font-size:12px;margin:2px 0}.move b{color:var(--gold)}.quick b{color:var(--em)}.act b{color:#7fb3ff}.afk b{color:var(--mute)}.lock b{color:var(--warn)}.sh{color:var(--gold);font-size:11.5px;margin-top:3px}summary{cursor:pointer}
.box{margin-bottom:10px}.box h3{margin:0 0 6px;font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--gold)}
.box ul{margin:0;padding-left:16px}.box li{margin:2px 0}.tags{display:flex;flex-wrap:wrap;gap:4px}
.tag{border:1px solid var(--line);border-radius:10px;padding:1px 7px;font-size:11.5px;color:#d9cde0}
.muted{color:var(--mute)}
</style></head><body>
<header><h1>IdleOn Manager · Autiszemo</h1>
<span class="pill age" id="age"></span><span class="pill" id="stage"></span><span class="pill muted">Ordering: Griffy rinse (Thigh Gap v2)</span></header>
<main><section class="cards" id="cards"></section><aside id="side"></aside></main>
<script>
const D = __DATA__;
const el=(t,c,txt)=>{const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e};
const store={get(k){try{return JSON.parse(localStorage.getItem(k)||'{}')}catch(e){return{}}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const KEY='idleon-done-'+D.stamp; let done=store.get(KEY);
const save=new Date(D.meta.game_save_utc), hrs=(Date.now()-save)/36e5;
const age=document.getElementById('age');
age.innerHTML='';age.append('Game save ',Object.assign(el('b'),{textContent:D.meta.game_save_et}),' · ',Object.assign(el('b'),{textContent:(hrs<48?hrs.toFixed(1)+' h':(hrs/24).toFixed(1)+' days')+' old'}));
if(hrs>12)age.classList.add('old');
document.getElementById('stage').textContent='Stage: strongest '+(D.side.stage.high||'?')+' · weakest '+(D.side.stage.low||'?');
const C=document.getElementById('cards');
D.cards.forEach(cd=>{const c=el('div','card');c.id='slot-'+cd.slot;
 const h=el('h2');h.append(el('span',null,cd.slot+'. '+cd.name),el('small','muted',cd.level));c.append(h);
 c.append(el('div','sub',cd.class+' · coins '+Number(cd.money).toExponential(2)+(cd.afk_now?' · now '+cd.afk_now:'')));
 const line=(cls,lab,txt)=>{const d=el('div',cls);d.append(el('b',null,lab+' '),txt);c.append(d)};
 line('move','MOVE',cd.move.text+' ['+cd.move.src+']');
 cd.quick.forEach(q=>line('quick','QUICK',q));
 cd.active.forEach(t=>line('act','ACTIVE',t.task+(t.notes?' · '+t.notes.join('; '):'')));
 line('afk','AFK',cd.afk.text+' ['+cd.afk.src+']');
 cd.flags.forEach(f=>c.append(el('div','flag','⚑ '+f)));
 cd.jobs.forEach((j,ji)=>{const b=el('details','job');const t=el('summary','t',j.job);
  const tiers=Object.entries(j.tiers||{}).map(([k,v])=>k+' '+v).join(', ');if(tiers)t.append(' ',el('span','tier','('+tiers+')'));b.append(t);
  if(j.note)b.append(el('div','sub',j.note));if(j.state)b.append(el('div','sub',j.state));
  (j.findings||[]).forEach(f=>b.append(el('div','sub','findings: '+f)));
  (j.where||[]).forEach(w=>b.append(el('div','sub','data: '+w.system+' · Toolbox '+w.toolbox.join(', ')+' · sources '+w.sources)));
  if(j.maestro_behind)b.append(el('div','sub','behind: '+j.maestro_behind.join(', ')));
  const ul=el('ul');let xi=0;(j.subs||[]).forEach(sb=>{ul.append(el('li','sh',sb.name+(sb.more>0?' (+'+sb.more+' more)':'')));
   sb.items.forEach(x=>{const id=cd.slot+'-'+ji+'-'+(xi++);const li=el('li',done[id]?'done':'');
   const cb=el('input');cb.type='checkbox';cb.checked=!!done[id];cb.onchange=()=>{done[id]=cb.checked;li.classList.toggle('done',cb.checked);store.set(KEY,done)};
   const s=el('span');s.append(x.label.slice(0,110)+': '+(x.cur||'?')+' ',el('span','arrow','→'),' '+(x.goal||'?')+(x.ready?' READY':''));li.append(cb,s);ul.append(li)})});
  b.append(ul);c.append(b)});
 cd.locked.forEach(l=>line('lock','LOCKED',l.feature+' ← '+l.unlock));
 const tl=Object.entries(cd.talents||{});if(tl.length){const b=el('details','job');b.append(el('summary','t','Library talents'));tl.forEach(([k,v])=>b.append(el('div','sub',k+': '+v.join(', '))));c.append(b)}
 if(cd.bags.length)line('sub','Bags missing',cd.bags.join('; '));
 C.append(c)});
const S=document.getElementById('side'),sd=D.side;
const box=(title,node)=>{const b=el('div','box');b.append(el('h3',null,title),node);S.append(b)};
const list=a=>{const u=el('ul');a.forEach(x=>u.append(el('li',null,x)));return u};
const A=D.account||{};
if(A.loop)box('Daily loop',list(A.loop));
if(A.alerts)box('Account alerts',list(A.alerts.length?A.alerts.map(a=>a.name+' → '+a.owner+': '+a.hits.join('; ')):['none']));
if(A.active_ranked)box('Active tasks (ranked)',list(A.active_ranked.map(t=>t.importance+' · '+t.owner+': '+t.task+' ('+t.minutes+'m)')));
if(A.ledger){const lw=A.ledger.watch.map(w=>w.item+': '+Math.round(w.owned).toLocaleString()+(w.target?' / '+w.target.toLocaleString()+(w.eta_days?' · ETA '+w.eta_days.toFixed(1)+' d':''):'')+(w.rate_hr!=null?' · '+(w.rate_hr>=0?'+':'')+Math.round(w.rate_hr).toLocaleString()+'/hr':'')+(w.runout_days?' · RUNS OUT '+w.runout_days.toFixed(1)+' d':'')+(w.flag?' · '+w.flag:'')+' ('+w.owner+')');
 box('Materials (vs '+(A.ledger.vs||'n/a')+')',list(lw.concat((A.ledger.stamps||[]).map(x=>'STAMP '+x.stamp+' '+x.level+' → '+x.target+': next raise '+Math.round(x.next_raise).toLocaleString()+' '+x.material+' (own '+Math.round(x.owned).toLocaleString()+')'+(x.next_raise<=x.owned?' READY':'')),A.ledger.runout.length?A.ledger.runout.map(x=>'FALLING '+x.item+': out in '+x.runout_days.toFixed(1)+' d'):['Nothing running out within 7 days'])))}
if(A.coins){const e=x=>Number(x).toExponential(2);const C2=A.coins;
 box('Coins: Upgrade Vault (cheapest next)',list(C2.vault.slice(0,15).map(v=>v.name+' '+v.level+'/'+v.max+': next '+e(v.next)+' · '+C2.richest+' can buy +'+v.buy_richest+' ('+e(v.buy_cost)+')')));
 box('Coins: Advice Fish + vendor',list(C2.advice_fish.map(f=>f.name+' lv '+f.level+': next '+e(f.next)+' · '+(f.next_ok.slice(0,2).join(', ')||'nobody')).concat(C2.vendor.map(v=>v.name+': '+e(v.price)+' · '+(v.ok.slice(0,2).join(', ')||'nobody')+(v.check?' · check price':'')),C2.caveats)))}
if(A.money)box('Money',list(['Total '+Number(A.money.total).toExponential(2)+' · bank '+Number(A.money.bank).toExponential(2),A.money.holder+' holds the most']));
if(A.unassigned)box('Unassigned',list(A.unassigned.map(u=>u.job+': '+u.note)));
const tags=a=>{const d=el('div','tags');a.forEach(x=>d.append(el('span','tag',x)));if(!a.length)d.append(el('span','muted','none'));return d};
const gl=el('ul');sd.gaps.forEach(g=>{const li=el('li');li.append(el('b',null,g.score+' '),g.section+': '+g.label+' ',el('span','arrow',(g.cur||'?')+' → '+(g.goal||'?')));gl.append(li)});
box('Biggest Thigh Gaps (Griffy rinse, one per system)',gl);
if(sd.timers){const t=sd.timers,d=el('div');const cap=new Date(t.captured_utc);d.append(el('div','muted','Captured '+cap.toLocaleString()+' (countdowns are as of then)'));
 d.append(el('div',null,'Resets: '+Object.entries(t.resets).map(([k,v])=>k+' '+v).join(' · ')));
 ['READY NOW','NEXT 24 HOURS','THIS WEEK'].forEach(b=>{if(!(t.timers[b]||[]).length)return;d.append(el('div','sub',b));d.append(tags(t.timers[b].map(x=>x.name+(x.value?': '+x.value:''))))});
 box('Timers (Toolbox)',d)}
box('Watch list',list(sd.watch));
box('Rule-changers owned',list(['King Doot: '+sd.doot,sd.companions+' companions · '+sd.packs+' packs (details in repo model/mechanics.md)']));
box('Achievements',list([sd.ach.done+' done · '+sd.ach.open+' open','Completable-now list: coming with the wiki source pass']));
box('Trophies missing ('+sd.trophies_missing.length+')',tags(sd.trophies_missing));
box('Capes missing ('+sd.capes_missing.length+')',tags(sd.capes_missing));
box('Get by playing (trophies / nametags / hats)',list([].concat(sd.ingame.trophies.map(x=>'Trophy: '+x),sd.ingame.nametags.map(x=>'Nametag: '+x),sd.ingame.hats.slice(0,12).map(x=>'Hat: '+x))));
</script></body></html>"""
os.makedirs(os.path.join(R, 'dashboard'), exist_ok=True)
out = PAGE.replace('__DATA__', json.dumps(data).replace('</', '<\\/'))
open(os.path.join(R, 'dashboard', 'index.html'), 'w').write(out)
print('dashboard', len(out), 'bytes')
