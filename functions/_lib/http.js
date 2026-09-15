// Small HTTP helpers shared by the API routes.

// One canonical host. The apex is attached to the project too, but anything
// under /customer or /admin on it is sent to www (session cookies are
// host-only, so mixing hosts would look like random sign-outs). Done here, not
// in a root _middleware.js, so static assets never invoke a Function.
const APEX_HOST = 'streamax-trucking.com';
const CANONICAL_ORIGIN = 'https://www.streamax-trucking.com';

export function apexRedirect(request) {
  const url = new URL(request.url);
  if (url.hostname !== APEX_HOST) return null;
  return new Response(null, {
    status: 301,
    headers: { Location: CANONICAL_ORIGIN + url.pathname + url.search, 'Cache-Control': 'public, max-age=3600' },
  });
}

export function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...headers,
    },
  });
}

export function error(message, status) {
  return json({ error: message }, status);
}

export async function readJson(request) {
  try {
    const data = await request.json();
    return data && typeof data === 'object' ? data : {};
  } catch (e) {
    return {};
  }
}

export function clientIp(request) {
  return request.headers.get('CF-Connecting-IP') || 'unknown';
}

// Personalised or gated responses must never be stored by a shared cache.
export function noStore(response) {
  const r = new Response(response.body, response);
  r.headers.set('Cache-Control', 'private, no-store');
  return r;
}

export function redirect(location, extraHeaders = {}) {
  return new Response(null, {
    status: 302,
    headers: { Location: location, 'Cache-Control': 'no-store', ...extraHeaders },
  });
}

// Only allow same-site relative targets after login (no open redirects).
export function safeNext(next, prefix, fallback) {
  if (typeof next !== 'string') return fallback;
  if (!next.startsWith(prefix) || next.startsWith('//') || next.includes('\\')) return fallback;
  return next;
}
