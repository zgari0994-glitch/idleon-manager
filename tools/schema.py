#!/usr/bin/env python3
"""Compact shape of a parsed-save path, for writing planners. Usage: tools/schema.py account.tesseract [depth]"""
import sys; sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'model'))
from data import load
v = load().get(sys.argv[1], allow_empty=True); D = int(sys.argv[2]) if len(sys.argv) > 2 else 2
def sh(x, d, ind):
    pad = '  ' * ind
    if isinstance(x, dict):
        if d <= 0: return f"{{{len(x)} keys: {', '.join(list(x)[:8])}}}"
        return '\n' + '\n'.join(f"{pad}{k}: {sh(y, d - 1, ind + 1)}" for k, y in list(x.items())[:30]) + (f"\n{pad}... {len(x) - 30} more" if len(x) > 30 else '')
    if isinstance(x, list):
        if not x: return '[]'
        return f"[{len(x)}] of " + sh(x[0], d - 1, ind + 1) if isinstance(x[0], (dict, list)) else f"[{len(x)}] {str(x[:6])[:100]}"
    s = repr(x); return s if len(s) < 90 else s[:87] + '...'
print(sh(v, D, 0))
