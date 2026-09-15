import { clearedCookie, ADMIN_COOKIE } from '../../_lib/auth.js';
import { json } from '../../_lib/http.js';

export async function onRequestPost() {
  return json({ ok: true }, 200, { 'Set-Cookie': clearedCookie(ADMIN_COOKIE) });
}
