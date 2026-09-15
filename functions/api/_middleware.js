// Runs before every /api/* route. State-changing calls must be JSON from this
// same site: a cross-site form can't send application/json without a CORS
// preflight (which we never grant), and SameSite=Lax cookies cover the rest.
import { error } from '../_lib/http.js';

const WRITE_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

export async function onRequest({ request, next }) {
  if (WRITE_METHODS.has(request.method)) {
    const ct = request.headers.get('Content-Type') || '';
    if (!ct.toLowerCase().includes('application/json')) return error('Expected a JSON request.', 415);
    const origin = request.headers.get('Origin');
    if (origin) {
      let same = false;
      try { same = new URL(origin).host === new URL(request.url).host; } catch (e) { same = false; }
      if (!same) return error('Cross-site request blocked.', 403);
    }
  }
  return next();
}
