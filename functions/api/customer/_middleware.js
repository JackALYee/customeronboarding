// Every /api/customer/* route except login/logout needs a valid, still-active client.
import { readSession, sessionStillValid } from '../../_lib/auth.js';
import { getCustomer } from '../../_lib/store.js';
import { error } from '../../_lib/http.js';

const OPEN = new Set(['/api/customer/login', '/api/customer/logout']);

export async function onRequest(context) {
  const { request, env, next, data } = context;
  const path = new URL(request.url).pathname;
  if (OPEN.has(path)) return next();
  const session = await readSession(request, env, 'customer');
  const account = session ? await getCustomer(env, session.sub) : null;
  if (!account || account.disabled || !sessionStillValid(session, account)) return error('Not signed in.', 401);
  data.customer = account;
  return next();
}
