// Every /api/admin/* route except login/logout needs a valid staff session.
import { readSession, sessionStillValid } from '../../_lib/auth.js';
import { getAdmin } from '../../_lib/store.js';
import { error } from '../../_lib/http.js';

const OPEN = new Set(['/api/admin/login', '/api/admin/logout']);

export async function onRequest(context) {
  const { request, env, next, data } = context;
  const path = new URL(request.url).pathname;
  if (OPEN.has(path)) return next();
  const session = await readSession(request, env, 'admin');
  const admin = session ? await getAdmin(env, session.sub) : null;
  if (!admin || !sessionStillValid(session, admin)) return error('Not signed in.', 401);
  data.admin = admin;
  return next();
}
