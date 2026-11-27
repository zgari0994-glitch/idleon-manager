// Cloudflare Pages Function: POST /upload-zack (Zack's own account, page /zack.html)
// Checks the passcode against its SHA-256 (the passcode itself is not in the repo), then commits the gzipped raw save
// to inbox/zack/raw.json.gz. That push triggers .github/workflows/zack-pull.yml (snapshot + pipeline + cards).
// Uses the same UPLOAD_GH_TOKEN secret as the brother page.
const REPO = 'zgari0994-glitch/idleon-manager';
const PATH = 'inbox/zack/raw.json.gz';
const EXPECT_FIRST = 'Autiszemo';
const PASS_SHA256 = '41e3a6ebf6616b23d061dda9491ada7fd8686be6dc7576a2532b517df586bfab';

async function sha256(s) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return new Response('bad request', { status: 400 }); }
  if (typeof body.passcode !== 'string' || (await sha256(body.passcode)) !== PASS_SHA256) return new Response('wrong passcode', { status: 403 });
  if (body.first != null && body.first !== EXPECT_FIRST) return new Response('that is not the ' + EXPECT_FIRST + ' account', { status: 400 });
  if (typeof body.gz_b64 !== 'string' || body.gz_b64.length < 1000 || body.gz_b64.length > 8_000_000)
    return new Response('raw data looks wrong', { status: 400 });

  const api = `https://api.github.com/repos/${REPO}/contents/${PATH}`;
  const h = { authorization: `Bearer ${env.UPLOAD_GH_TOKEN}`, accept: 'application/vnd.github+json', 'user-agent': 'idleon-zack-upload' };
  const cur = await fetch(api, { headers: h });
  const sha = cur.ok ? (await cur.json()).sha : undefined;
  const put = await fetch(api, { method: 'PUT', headers: { ...h, 'content-type': 'application/json' },
    body: JSON.stringify({ message: 'zack upload', content: body.gz_b64, ...(sha ? { sha } : {}) }) });
  if (!put.ok) return new Response('GitHub said ' + put.status, { status: 502 });
  return new Response('ok');
}
