"""Decode a browser-pane Toolbox pull (saved tool-result file) into a raw save JSON.
Usage: python decode_pull.py <tool_result_file> <out.json>
"""
import sys, json, base64, gzip
arr = json.load(open(sys.argv[1]))
t = arr[0]['text'] if isinstance(arr, list) else str(arr)
parts = t[t.index('GZB64|'):].split('|')
b64 = parts[2]
assert len(b64) == int(parts[1]), 'truncated pull'
raw = gzip.decompress(base64.b64decode(b64))
j = json.loads(raw)
assert len(j.get('charNames', [])) == 11, 'expected 11 characters'
open(sys.argv[2], 'wb').write(raw)
ta = j['data']['TimeAway']; ta = json.loads(ta) if isinstance(ta, str) else ta
print('ok', len(raw), 'bytes, GlobalTime', ta['GlobalTime'])
