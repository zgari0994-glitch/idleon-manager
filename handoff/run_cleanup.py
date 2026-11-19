"""Clean garbled/off-game tag names with Claude Haiku 5.5 (Batch API, about $0.10-0.30). Stdlib only.
  py run_cleanup.py      -> submits, waits, writes cleanup_results.json (re-run is safe)
"""
import json, os, sys, time, urllib.request, urllib.error

MODEL = "claude-haiku-5-5"
HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "cleanup_state.json")
API = "https://api.anthropic.com/v1"
PER_REQ = 40

SYSTEM = """You fix tags extracted from auto-captioned IdleOn (Legends of Idleon) YouTube videos.
For each row decide:
- "keep": subsystem already names a real IdleOn thing (talent, bubble, card, map, monster, item, upgrade, minigame, mechanic), even if it is not in the candidates.
- "fix": subsystem is a caption garble or a vague/misspelled version of a real IdleOn name. Give the correct real name in "name" (use a candidate when one fits; otherwise your own knowledge of IdleOn). Only fix when you are confident.
- "not_game": the row is not about game mechanics (stream chatter, giveaways, community, outro, channel talk, real-life topics).
Output ONLY a JSON array: [{"id": "...", "action": "keep|fix|not_game", "name": "..."}]. "name" only for fix."""


def key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if not k:
        sys.exit("ANTHROPIC_API_KEY not set.")
    return k


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"x-api-key": key(), "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for a in range(6):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read().decode()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and a < 5:
                time.sleep(20 * (a + 1)); continue
            sys.exit(f"API error {e.code}: {e.read().decode()[:400]}")


def main():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if not st.get("batch_id"):
        rows = [json.loads(l) for l in open(os.path.join(HERE, "cleanup_rows.jsonl"), encoding="utf-8") if l.strip()]
        reqs = []
        for i in range(0, len(rows), PER_REQ):
            chunk = rows[i:i + PER_REQ]
            reqs.append({"custom_id": f"c{i // PER_REQ:03d}", "params": {
                "model": MODEL, "max_tokens": 8000, "system": SYSTEM,
                "messages": [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}]}})
        r = json.loads(call("POST", "/messages/batches", {"requests": reqs}))
        st["batch_id"] = r["id"]; json.dump(st, open(STATE, "w"))
        print(f"Submitted {len(rows)} rows in {len(reqs)} requests. Batch {r['id']}. Waiting...")
    b = st["batch_id"]
    while True:
        s = json.loads(call("GET", f"/messages/batches/{b}"))
        print(time.strftime("%H:%M"), s["processing_status"], s["request_counts"], flush=True)
        if s["processing_status"] == "ended":
            break
        time.sleep(60)
    out, tin, tout, bad = [], 0, 0, []
    for line in call("GET", f"/messages/batches/{b}/results").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r["result"]["type"] != "succeeded":
            bad.append(r["custom_id"]); continue
        m = r["result"]["message"]; tin += m["usage"]["input_tokens"]; tout += m["usage"]["output_tokens"]
        t = "".join(x.get("text", "") for x in m["content"]).strip()
        t = t[t.find("["): t.rfind("]") + 1]
        try:
            out += json.loads(t)
        except Exception:
            bad.append(r["custom_id"])
    json.dump(out, open(os.path.join(HERE, "cleanup_results.json"), "w"), indent=0)
    print(f"Done: {len(out)} rows. Cost about ${tin / 1e6 * 0.05 + tout / 1e6 * 0.25:.2f}. Failed: {bad}. Tell Claude.")


main()
