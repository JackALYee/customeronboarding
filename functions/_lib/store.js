// Data layer - everything lives in one Workers KV namespace, bound as `KV`.
//
//   customer:<email>        full record JSON; list-metadata = table summary
//   admin:<username>        { username, password_hash, created_at }
//   event:<inv-ts>:<rand>   login audit row; the row itself is the metadata,
//                           key sorts newest-first; expires after 180 days
//   rl:<scope>:<ip>         failed-login counter, 15-minute window
//   config:session_key      HMAC key for session cookies (see auth.js)
//
// KV is eventually consistent (~60 s across regions): a brand-new account can
// take up to a minute to be visible from far-away edges, and list() lags the
// same way. Fine for this portal's scale; see HANDOFF.md.

export const DEFAULT_CONTACTS = [
  { role: 'Customer Success', contact: 'csm@streamax.com' },
  { role: 'Technical Support', contact: 'support@streamax.com' },
  { role: 'Hardware RMA', contact: 'rma@streamax.com' },
  { role: 'Billing', contact: 'billing@streamax.com' },
  { role: 'Emergency hotline', contact: 'Available 24/7 via your CSM' },
];

export const AUDIENCES = { fleet: 'Fleet Operator', tsp: 'TSP / Channel Partner' };

export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const MIN_PASSWORD = 8;

const EVENT_TTL = 180 * 24 * 3600;
const RATE_WINDOW = 15 * 60;
const RATE_MAX_FAILURES = 10;

export function normEmail(email) {
  return String(email || '').trim().toLowerCase();
}

export function nowIso() {
  return new Date().toISOString();
}

// ---- customers --------------------------------------------------------------

function customerMeta(c) {
  return {
    company: String(c.company || '').slice(0, 200),
    audience: c.audience,
    created_at: c.created_at || null,
    created_by: String(c.created_by || '').slice(0, 80),
    first_login_at: c.first_login_at || null,
    last_login_at: c.last_login_at || null,
    disabled: !!c.disabled,
  };
}

export async function getCustomer(env, email) {
  return env.KV.get(`customer:${normEmail(email)}`, { type: 'json' });
}

export async function putCustomer(env, c) {
  c.email = normEmail(c.email);
  await env.KV.put(`customer:${c.email}`, JSON.stringify(c), { metadata: customerMeta(c) });
  return c;
}

export async function deleteCustomer(env, email) {
  await env.KV.delete(`customer:${normEmail(email)}`);
}

export async function listCustomers(env) {
  const out = [];
  let cursor;
  do {
    const page = await env.KV.list({ prefix: 'customer:', cursor, limit: 1000 });
    for (const k of page.keys) {
      out.push({ email: k.name.slice('customer:'.length), ...(k.metadata || {}) });
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  out.sort((a, b) => String(b.created_at || '').localeCompare(String(a.created_at || '')) || a.email.localeCompare(b.email));
  return out;
}

// What an admin (or the client's own portal) may see - never the hash.
export function publicCustomer(c) {
  const hasCustom = Array.isArray(c.contacts) && c.contacts.length > 0;
  return {
    email: c.email,
    company: c.company || '',
    audience: c.audience,
    audience_label: AUDIENCES[c.audience] || AUDIENCES.fleet,
    created_at: c.created_at || null,
    created_by: c.created_by || null,
    first_login_at: c.first_login_at || null,
    last_login_at: c.last_login_at || null,
    disabled: !!c.disabled,
    contacts: hasCustom ? c.contacts : DEFAULT_CONTACTS.map((x) => ({ ...x })),
    contacts_are_default: !hasCustom,
  };
}

export function cleanContacts(list) {
  if (!Array.isArray(list)) return [];
  return list
    .map((x) => ({
      role: String((x && x.role) || '').trim().slice(0, 120),
      contact: String((x && x.contact) || '').trim().slice(0, 240),
    }))
    .filter((x) => x.role || x.contact)
    .slice(0, 30);
}

// ---- admins -------------------------------------------------------------------

export async function getAdmin(env, username) {
  return env.KV.get(`admin:${String(username || '').trim().toLowerCase()}`, { type: 'json' });
}

// ---- login audit log --------------------------------------------------------

export async function logEvent(env, email, role, method) {
  const at = nowIso();
  const inv = String(9999999999999 - Date.now()).padStart(13, '0');
  const rand = Math.random().toString(36).slice(2, 8);
  await env.KV.put(`event:${inv}:${rand}`, '', {
    expirationTtl: EVENT_TTL,
    metadata: { email: String(email).slice(0, 200), role, method, at },
  });
}

export async function recentEvents(env, limit = 50) {
  const page = await env.KV.list({ prefix: 'event:', limit });
  return page.keys.map((k) => k.metadata || {});
}

export async function countEvents(env, cap = 10000) {
  let n = 0;
  let cursor;
  do {
    const page = await env.KV.list({ prefix: 'event:', cursor, limit: 1000 });
    n += page.keys.length;
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor && n < cap);
  return { count: n, capped: !!cursor };
}

// ---- brute-force brake (best effort: KV is eventually consistent) -------------

export async function isRateLimited(env, scope, ip) {
  const n = parseInt((await env.KV.get(`rl:${scope}:${ip}`)) || '0', 10);
  return n >= RATE_MAX_FAILURES;
}

export async function noteFailedLogin(env, scope, ip) {
  try {
    const key = `rl:${scope}:${ip}`;
    const n = parseInt((await env.KV.get(key)) || '0', 10) + 1;
    await env.KV.put(key, String(n), { expirationTtl: RATE_WINDOW });
  } catch (e) {
    // Never let the brake itself break login (e.g. daily KV write quota).
  }
}
