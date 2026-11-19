"""Shared spend ranking: within one currency, rank buys by stat gain per share of the balance spent.

option = {item, currency, balance (None = unknown), cost, gain_pct (marginal % of the stat's total per level, None = unknown),
          stat, weight (1 default; >1 when a creator/AutoReview names it a priority), note}
score = weight * gain_pct / (cost / balance). Options with unknown gain sort after known ones, cheapest first.
"""


def rank(options):
    by = {}
    for o in options:
        by.setdefault(o['currency'], []).append(o)
    out = {}
    for cur, ops in by.items():
        for o in ops:
            share = (o['cost'] / o['balance']) if o.get('balance') and o.get('cost') else None
            o['share'] = share
            o['afford'] = None if o.get('balance') is None else (o['cost'] or 0) <= o['balance']
            o['score'] = (o.get('weight', 1) * o['gain_pct'] / share) if (o.get('gain_pct') is not None and share) else None
        out[cur] = sorted(ops, key=lambda o: (o['score'] is None, -(o['score'] or 0), o['cost'] or 0))
    return out


def h(x):
    """short number: 43.3K, 1.17T"""
    if x is None: return '?'
    for v, u in ((1e18, 'QQ'), (1e15, 'Q'), (1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if abs(x) >= v: return f"{x / v:.3g}{u}"
    return f"{x:,.0f}"


def fmt(o):
    g = f"+{o['gain_pct']:.2f}% {o['stat']}/lv" if o.get('gain_pct') is not None else o.get('stat', '')
    c = h(o.get('cost'))
    sh = f", {o['share'] * 100:.3g}% of balance" if o.get('share') is not None else ''
    return f"{o['item']} ({g}, next {c}{sh}){' [' + o['note'] + ']' if o.get('note') else ''}"
