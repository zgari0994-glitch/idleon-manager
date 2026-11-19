"""Tag IdleOn transcript packets with Claude Sonnet 5.5 (Batch API). Stdlib only.

Setup once:  setx ANTHROPIC_API_KEY "your-key"   (then reopen the command window)
Put this file next to idleon_api_packets.zip (it unzips itself).

  py run_tags.py pilot     -> tags 3 videos live, prints real cost + projected total
  py run_tags.py submit    -> sends everything else as one batch (refuses if projection > CAP)
  py run_tags.py collect   -> waits for the batch, writes out\\<video_id>.csv
Re-running is safe: finished videos are skipped.
"""
import json, os, re, sys, time, zipfile, urllib.request, urllib.error

MODEL = "claude-sonnet-5-5"
CAP_USD = 20.0                      # hard stop for the projected total
PRICE = {"live": (2.0, 10.0), "batch": (1.0, 5.0)}   # $ per 1M tokens (input, output)
CHUNK_WORDS = 12000
MAX_TOKENS = 20000
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(HERE, "packets")
OUT = os.path.join(HERE, "out")
STATE = os.path.join(HERE, "state.json")
API = "https://api.anthropic.com/v1"

SYSTEM = open(os.path.join(HERE, "TAGGER.md"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "TAGGER.md")) else ""
INSTR = ("You tag one IdleOn transcript chunk. Follow the tagger card's CSV, column, system and class rules exactly "
         "(ignore its git/loop instructions). Output ONLY the CSV: the header line, then one row per distinct claim. "
         "No prose, no code fences. Max detail, front to back, no skimming. If the chunk has no IdleOn claims, output the header "
         "and one row with system none.")


def key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if not k:
        sys.exit("ANTHROPIC_API_KEY not set. Run: setx ANTHROPIC_API_KEY \"your-key\" then reopen the window.")
    return k


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"x-api-key": key(), "anthropic-version": "2023-06-01", "content-type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read().decode()
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:500]
            if e.code in (429, 500, 502, 503, 529) and attempt < 5:
                time.sleep(20 * (attempt + 1)); continue
            sys.exit(f"API error {e.code}: {msg}")


def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"out_per_in": None, "batch_id": None, "spent": 0.0}


def save_state(s):
    json.dump(s, open(STATE, "w"), indent=1)


def packets():
    if not os.path.isdir(PK):
        zipfile.ZipFile(os.path.join(HERE, "idleon_api_packets.zip")).extractall(HERE)
    return sorted(f for f in os.listdir(PK) if f.endswith(".txt"))


def chunks(fname):
    text = open(os.path.join(PK, fname), encoding="utf-8").read()
    head, body = text.split("\n---\n", 1)
    out, cur, n = [], [], 0
    for line in body.splitlines():
        w = len(line.split())
        if cur and n + w > CHUNK_WORDS:
            out.append(cur); cur, n = [], 0
        cur.append(line); n += w
    if cur:
        out.append(cur)
    return head, ["\n".join(c) for c in out]


def vid(fname):
    return fname.split("_", 1)[1][:-4]


def params(head, chunk, i, total):
    return {"model": MODEL, "max_tokens": MAX_TOKENS,
            "system": [{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": f"{INSTR}\n\n{head}\nchunk: {i + 1}/{total}\n---\n{chunk}"}]}


def clean(text):
    text = re.sub(r"^```[a-z]*\n?|```$", "", text.strip(), flags=re.M).strip()
    lines = [l for l in text.splitlines() if l.strip()]
    if lines and lines[0].startswith("t_start"):
        lines = lines[1:]
    return lines


def write(v, parts):
    os.makedirs(OUT, exist_ok=True)
    rows = [r for p in parts for r in p]
    with open(os.path.join(OUT, v + ".csv"), "w", encoding="utf-8", newline="") as f:
        f.write("t_start,t_end,system,subsystem,class,claim_type,stage,numbers,statement,explicit,confidence\n")
        f.write("\n".join(rows) + "\n")
    return len(rows)


def todo():
    done = {f[:-4] for f in os.listdir(OUT)} if os.path.isdir(OUT) else set()
    return [f for f in packets() if vid(f) not in done]


def words(f):
    return len(open(os.path.join(PK, f), encoding="utf-8").read().split())


def pilot():
    s = load_state(); tin = tout = w = 0
    for f in todo()[:3]:
        head, cs = chunks(f); parts = []
        for i, c in enumerate(cs):
            r = json.loads(call("POST", "/messages", params(head, c, i, len(cs))))
            u = r["usage"]; tin += u["input_tokens"] + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0); tout += u["output_tokens"]
            parts.append(clean("".join(b.get("text", "") for b in r["content"])))
        w += words(f)
        print(f"{vid(f)}: {write(vid(f), parts)} rows")
    cost = tin / 1e6 * PRICE["live"][0] + tout / 1e6 * PRICE["live"][1]
    s["spent"] += cost; s["in_per_word"] = tin / w; s["out_per_word"] = tout / w; save_state(s)
    rest = sum(words(f) for f in todo())
    proj = rest * (s["in_per_word"] * PRICE["batch"][0] + s["out_per_word"] * PRICE["batch"][1]) / 1e6
    print(f"\nPilot cost ${cost:.2f}. Remaining {len(todo())} videos, {rest:,} words.")
    print(f"Projected batch cost for the rest: ${proj:.2f} (cap ${CAP_USD:.0f}). If OK: py run_tags.py submit")


def submit():
    s = load_state()
    if s.get("batch_id"):
        sys.exit(f"Batch {s['batch_id']} already submitted. Run: py run_tags.py collect")
    if not s.get("out_per_word"):
        sys.exit("Run the pilot first: py run_tags.py pilot")
    files = todo(); rest = sum(words(f) for f in files)
    proj = rest * (s["in_per_word"] * PRICE["batch"][0] + s["out_per_word"] * PRICE["batch"][1]) / 1e6
    if proj > CAP_USD:
        sys.exit(f"Projected ${proj:.2f} is over the ${CAP_USD:.0f} cap. Stopping. Nothing was sent.")
    reqs = []
    for f in files:
        head, cs = chunks(f)
        for i, c in enumerate(cs):
            reqs.append({"custom_id": f"{vid(f)}__{i:03d}", "params": params(head, c, i, len(cs))})
    r = json.loads(call("POST", "/messages/batches", {"requests": reqs}))
    s["batch_id"] = r["id"]; s["batch_files"] = [vid(f) for f in files]; save_state(s)
    print(f"Submitted {len(reqs)} requests for {len(files)} videos (projected ${proj:.2f}). Batch {r['id']}.")
    print("Now run: py run_tags.py collect   (it waits until done)")


def collect():
    s = load_state(); b = s.get("batch_id")
    if not b:
        sys.exit("No batch submitted yet.")
    while True:
        st = json.loads(call("GET", f"/messages/batches/{b}"))
        c = st["request_counts"]
        print(time.strftime("%H:%M"), st["processing_status"], c, flush=True)
        if st["processing_status"] == "ended":
            break
        time.sleep(300)
    raw = call("GET", f"/messages/batches/{b}/results")
    parts, tin, tout, errs = {}, 0, 0, []
    for line in raw.splitlines():
        if not line.strip():
            continue
        r = json.loads(line); v, i = r["custom_id"].rsplit("__", 1)
        res = r["result"]
        if res["type"] != "succeeded":
            errs.append(r["custom_id"]); continue
        m = res["message"]; u = m["usage"]
        tin += u["input_tokens"] + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0); tout += u["output_tokens"]
        parts.setdefault(v, {})[int(i)] = clean("".join(x.get("text", "") for x in m["content"]))
    total = 0
    for v, d in parts.items():
        total += write(v, [d[k] for k in sorted(d)])
    cost = tin / 1e6 * PRICE["batch"][0] + tout / 1e6 * PRICE["batch"][1]
    s["spent"] += cost; s["batch_done"] = True; save_state(s)
    print(f"\nWrote {len(parts)} videos, {total:,} rows. Batch cost about ${cost:.2f}. Total spent ${s['spent']:.2f}.")
    if errs:
        print(f"{len(errs)} chunks failed: {errs[:10]}. Tell Claude.")


if __name__ == "__main__":
    {"pilot": pilot, "submit": submit, "collect": collect}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
