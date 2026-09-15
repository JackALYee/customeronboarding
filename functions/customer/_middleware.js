// Server-side gate for every /customer/* page. Signed-out visitors are
// redirected to the login page before any portal HTML is served. The account
// is re-read on every page view, so disabling or deleting a client takes
// effect immediately instead of when their cookie expires.
import { readSession, sessionStillValid, clearedCookie, CUSTOMER_COOKIE } from '../_lib/auth.js';
import { getCustomer } from '../_lib/store.js';
import { noStore, redirect, apexRedirect } from '../_lib/http.js';

function isLoginPath(p) {
  return p === '/customer/login' || p.startsWith('/customer/login/');
}

export async function onRequest({ request, env, next }) {
  const canonical = apexRedirect(request);
  if (canonical) return canonical;
  const url = new URL(request.url);
  const session = await readSession(request, env, 'customer');
  const account = session ? await getCustomer(env, session.sub) : null;
  const valid = !!(account && !account.disabled && sessionStillValid(session, account));

  if (isLoginPath(url.pathname)) {
    if (valid) return redirect('/customer/');
    return noStore(await next());
  }
  if (!valid) {
    const target = `/customer/login/?next=${encodeURIComponent(url.pathname + url.search)}`;
    return redirect(target, session ? { 'Set-Cookie': clearedCookie(CUSTOMER_COOKIE) } : {});
  }
  return noStore(await next());
}
