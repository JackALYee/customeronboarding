// GET    /api/admin/customers/:email -> one client (incl. Key Contacts)
// PATCH  /api/admin/customers/:email -> update company / audience / password /
//                                       contacts (null = reset to defaults) / disabled
// DELETE /api/admin/customers/:email -> remove the account
import { hashPassword } from '../../../_lib/auth.js';
import {
  getCustomer, putCustomer, deleteCustomer, publicCustomer, cleanContacts,
  AUDIENCES, MIN_PASSWORD, normEmail,
} from '../../../_lib/store.js';
import { json, error, readJson } from '../../../_lib/http.js';

function emailParam(params) {
  try { return normEmail(decodeURIComponent(params.email || '')); } catch (e) { return ''; }
}

export async function onRequestGet({ env, params }) {
  const c = await getCustomer(env, emailParam(params));
  if (!c) return error('No such client.', 404);
  return json({ customer: publicCustomer(c) });
}

export async function onRequestPatch({ request, env, params }) {
  const c = await getCustomer(env, emailParam(params));
  if (!c) return error('No such client.', 404);
  const body = await readJson(request);

  if ('company' in body) {
    const company = String(body.company || '').trim();
    if (!company) return error('Company name cannot be empty.', 400);
    c.company = company.slice(0, 200);
  }
  if ('audience' in body) {
    if (!AUDIENCES[body.audience]) return error('Audience must be fleet or tsp.', 400);
    c.audience = body.audience;
  }
  if ('password' in body) {
    const pw = typeof body.password === 'string' ? body.password : '';
    if (pw.length < MIN_PASSWORD) return error(`Password must be at least ${MIN_PASSWORD} characters.`, 400);
    c.password_hash = await hashPassword(pw);
    c.session_epoch = Math.floor(Date.now() / 1000); // signs out existing sessions
  }
  if ('contacts' in body) {
    c.contacts = body.contacts === null ? null : cleanContacts(body.contacts);
    if (Array.isArray(c.contacts) && c.contacts.length === 0) c.contacts = null;
  }
  if ('disabled' in body) c.disabled = !!body.disabled;

  await putCustomer(env, c);
  return json({ customer: publicCustomer(c) });
}

export async function onRequestDelete({ env, params }) {
  const email = emailParam(params);
  if (!(await getCustomer(env, email))) return error('No such client.', 404);
  await deleteCustomer(env, email);
  return json({ ok: true });
}
