import {
  verifyPassword, burnPasswordCheck, signSession, sessionCookie,
  CUSTOMER_COOKIE, CUSTOMER_TTL,
} from '../../_lib/auth.js';
import {
  getCustomer, putCustomer, logEvent, isRateLimited, noteFailedLogin, normEmail, nowIso,
} from '../../_lib/store.js';
import { json, error, readJson, clientIp } from '../../_lib/http.js';

const BAD_LOGIN = "Invalid email or password. If you don't have an account yet, contact your Streamax CSM.";

export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  const email = normEmail(body.email);
  const password = typeof body.password === 'string' ? body.password : '';
  if (!email || !password) return error('Please enter both your email and password.', 400);

  const ip = clientIp(request);
  if (await isRateLimited(env, 'customer', ip)) {
    return error('Too many sign-in attempts. Please wait 15 minutes and try again.', 429);
  }

  const account = await getCustomer(env, email);
  const ok = account && !account.disabled
    ? await verifyPassword(password, account.password_hash)
    : await burnPasswordCheck(password);
  if (!ok) {
    await noteFailedLogin(env, 'customer', ip);
    return error(BAD_LOGIN, 401);
  }

  // Bookkeeping is best effort - a KV hiccup must never block a valid sign-in.
  try {
    const now = nowIso();
    if (!account.first_login_at) account.first_login_at = now;
    account.last_login_at = now;
    await putCustomer(env, account);
    await logEvent(env, account.email, 'customer', 'password');
  } catch (e) { /* ignore */ }

  const token = await signSession(env, { sub: account.email, role: 'customer' }, CUSTOMER_TTL);
  return json({ ok: true }, 200, { 'Set-Cookie': sessionCookie(CUSTOMER_COOKIE, token, CUSTOMER_TTL) });
}
