// Cloudflare Pages Function: POST /upload
// Checks the passcode, then commits the gzipped raw save to accounts/brother/inbox/raw.json.gz in GitHub.
// That push triggers .github/workflows/brother.yml, which rebuilds and redeploys the dashboard.
// Secrets (set by the workflow): UPLOAD_PASSCODE, UPLOAD_GH_TOKEN (fine-grained, Contents: write on this repo only).
const REPO = 'zgari0994-glitch/idleon-manager';
const PATH = 'accounts/brother/inbox/raw.json.gz';
const EXPECT_FIRST = 'IdleOnLech';

export async function onRequestPost({ request, env }) {
  let body;
  try { body = await request.json(); } catch { return new Response('bad request', { status: 400 }); }
  if (!env.UPLOAD_PASSCODE || body.passcode !== env.UPLOAD_PASSCODE) return new Response('wrong passcode', { status: 403 });
  if (body.first != null && body.first !== EXPECT_FIRST) return new Response('that is not the ' + EXPECT_FIRST + ' account', { status: 400 });
  if (typeof body.gz_b64 !== 'string' || body.gz_b64.length < 1000 || body.gz_b64.length > 5_000_000)
    return new Response('raw data looks wrong', { status: 400 });

  const api = `https://api.github.com/repos/${REPO}/contents/${PATH}`;
  const h = { authorization: `Bearer ${env.UPLOAD_GH_TOKEN}`, accept: 'application/vnd.github+json', 'user-agent': 'idleon-brother-upload' };
  const cur = await fetch(api, { headers: h });
  const sha = cur.ok ? (await cur.json()).sha : undefined;
  const put = await fetch(api, { method: 'PUT', headers: { ...h, 'content-type': 'application/json' },
    body: JSON.stringify({ message: 'brother upload', content: body.gz_b64, ...(sha ? { sha } : {}) }) });
  if (!put.ok) return new Response('GitHub said ' + put.status, { status: 502 });
  return new Response('ok');
}
