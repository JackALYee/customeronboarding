// Password hashing + signed session cookies (Web Crypto only - no dependencies).
//
// Password format (identical to tools/set_admin.py and the retired Python app):
//     pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>
// The iteration count travels with each hash, so it can be tuned later without
// breaking existing accounts. Workers' Web Crypto rejects PBKDF2 above 100,000.
//
// Session cookie: v1.<base64url(payload JSON)>.<base64url(HMAC-SHA256)>, signed
// with a random key stored in KV at `config:session_key`. Rotating that key
// signs everyone out at once.

export const PBKDF2_ITERATIONS = 100000;
const PBKDF2_MAX = 100000;

export const CUSTOMER_COOKIE = 'stx_session';
export const ADMIN_COOKIE = 'stx_admin';
export const CUSTOMER_TTL = 7 * 24 * 3600; // 7 days, as in the old portal
export const ADMIN_TTL = 12 * 3600;        // staff sessions expire the same day

const enc = new TextEncoder();
const dec = new TextDecoder();

export function toHex(buf) {
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
}

export function fromHex(hex) {
  if (typeof hex !== 'string' || hex.length % 2) throw new Error('bad hex');
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(hex.substr(i * 2, 2), 16);
  return out;
}

function b64url(bytes) {
  let s = '';
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function unb64url(str) {
  const s = str.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((str.length + 3) % 4);
  const bin = atob(s);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

async function pbkdf2(plain, salt, iterations) {
  const key = await crypto.subtle.importKey('raw', enc.encode(plain), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations }, key, 256);
  return new Uint8Array(bits);
}

export async function hashPassword(plain) {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const hash = await pbkdf2(plain, salt, PBKDF2_ITERATIONS);
  return `pbkdf2_sha256$${PBKDF2_ITERATIONS}$${toHex(salt)}$${toHex(hash)}`;
}

export async function verifyPassword(plain, stored) {
  if (typeof stored !== 'string' || !stored.startsWith('pbkdf2_sha256$')) return false;
  const parts = stored.split('$');
  if (parts.length !== 4) return false;
  const iterations = parseInt(parts[1], 10);
  if (!(iterations > 0 && iterations <= PBKDF2_MAX)) return false;
  try {
    const computed = await pbkdf2(plain, fromHex(parts[2]), iterations);
    return timingSafeEqual(computed, fromHex(parts[3]));
  } catch (e) {
    return false;
  }
}

// Spend the same work as a real check when the account doesn't exist, so
// response timing doesn't reveal which emails have accounts.
const DUMMY_SALT = new Uint8Array(16);
export async function burnPasswordCheck(plain) {
  await pbkdf2(plain || 'x', DUMMY_SALT, PBKDF2_ITERATIONS);
  return false;
}

// ---- session signing ------------------------------------------------------

async function sessionKey(env) {
  let hex = await env.KV.get('config:session_key', { cacheTtl: 300 });
  if (!hex) {
    // Normally created by tools/set_admin.py before the first deploy; this is
    // only a first-run fallback.
    hex = toHex(crypto.getRandomValues(new Uint8Array(32)));
    await env.KV.put('config:session_key', hex);
  }
  return crypto.subtle.importKey('raw', fromHex(hex), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign', 'verify']);
}

export async function signSession(env, payload, ttlSeconds) {
  const now = Math.floor(Date.now() / 1000);
  const body = b64url(enc.encode(JSON.stringify({ ...payload, iat: now, exp: now + ttlSeconds })));
  const signed = `v1.${body}`;
  const sig = await crypto.subtle.sign('HMAC', await sessionKey(env), enc.encode(signed));
  return `${signed}.${b64url(new Uint8Array(sig))}`;
}

export async function verifySession(env, token, role) {
  if (typeof token !== 'string') return null;
  const parts = token.split('.');
  if (parts.length !== 3 || parts[0] !== 'v1') return null;
  try {
    const ok = await crypto.subtle.verify(
      'HMAC', await sessionKey(env), unb64url(parts[2]), enc.encode(`${parts[0]}.${parts[1]}`)
    );
    if (!ok) return null;
    const payload = JSON.parse(dec.decode(unb64url(parts[1])));
    if (!payload || payload.role !== role || typeof payload.sub !== 'string') return null;
    if (!(payload.exp > Math.floor(Date.now() / 1000))) return null;
    return payload;
  } catch (e) {
    return null;
  }
}

// ---- cookies ----------------------------------------------------------------

export function getCookie(request, name) {
  const header = request.headers.get('Cookie') || '';
  for (const part of header.split(';')) {
    const i = part.indexOf('=');
    if (i > -1 && part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return null;
}

export function sessionCookie(name, value, maxAge) {
  return `${name}=${value}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;
}

export function clearedCookie(name) {
  return `${name}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;
}

// A password reset stamps the account with `session_epoch` (unix seconds);
// any session issued before that moment is rejected - so a reset really
// signs out whoever held the old password, instead of waiting for expiry.
export function sessionStillValid(session, account) {
  if (!session || !account) return false;
  const epoch = Number(account.session_epoch || 0);
  return !(epoch && session.iat < epoch);
}

export async function readSession(request, env, role) {
  const name = role === 'admin' ? ADMIN_COOKIE : CUSTOMER_COOKIE;
  return verifySession(env, getCookie(request, name), role);
}
