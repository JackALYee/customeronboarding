// Server-side gate for every /admin/* page (same pattern as the customer gate).
import { readSession, sessionStillValid, clearedCookie, ADMIN_COOKIE } from '../_lib/auth.js';
import { getAdmin } from '../_lib/store.js';
import { noStore, redirect, apexRedirect } from '../_lib/http.js';

function isLoginPath(p) {
  return p === '/admin/login' || p.startsWith('/admin/login/');
}

export async function onRequest({ request, env, next }) {
  const canonical = apexRedirect(request);
  if (canonical) return canonical;
  const url = new URL(request.url);
  const session = await readSession(request, env, 'admin');
  const admin = session ? await getAdmin(env, session.sub) : null;
  const valid = !!(admin && sessionStillValid(session, admin));

  if (isLoginPath(url.pathname)) {
    if (valid) return redirect('/admin/');
    return noStore(await next());
  }
  if (!valid) {
    return redirect('/admin/login/', session ? { 'Set-Cookie': clearedCookie(ADMIN_COOKIE) } : {});
  }
  return noStore(await next());
}
