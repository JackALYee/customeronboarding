import {
  verifyPassword, burnPasswordCheck, signSession, sessionCookie, ADMIN_COOKIE, ADMIN_TTL,
} from '../../_lib/auth.js';
import { getAdmin, logEvent, isRateLimited, noteFailedLogin } from '../../_lib/store.js';
import { json, error, readJson, clientIp } from '../../_lib/http.js';

export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  const username = String(body.username || '').trim().toLowerCase();
  const password = typeof body.password === 'string' ? body.password : '';
  if (!username || !password) return error('Please enter both your username and password.', 400);

  const ip = clientIp(request);
  if (await isRateLimited(env, 'admin', ip)) {
    return error('Too many sign-in attempts. Please wait 15 minutes and try again.', 429);
  }

  const admin = await getAdmin(env, username);
  const ok = admin ? await verifyPassword(password, admin.password_hash) : await burnPasswordCheck(password);
  if (!ok) {
    await noteFailedLogin(env, 'admin', ip);
    return error('Invalid username or password.', 401);
  }
  try { await logEvent(env, admin.username, 'staff', 'password'); } catch (e) { /* best effort */ }

  const token = await signSession(env, { sub: admin.username, role: 'admin' }, ADMIN_TTL);
  return json({ ok: true, username: admin.username }, 200, {
    'Set-Cookie': sessionCookie(ADMIN_COOKIE, token, ADMIN_TTL),
  });
}
