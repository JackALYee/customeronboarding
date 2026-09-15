// GET  /api/admin/customers  -> all client accounts (summary rows)
// POST /api/admin/customers  -> create a client account
import { hashPassword } from '../../../_lib/auth.js';
import {
  listCustomers, getCustomer, putCustomer, publicCustomer, cleanContacts,
  AUDIENCES, EMAIL_RE, MIN_PASSWORD, normEmail, nowIso,
} from '../../../_lib/store.js';
import { json, error, readJson } from '../../../_lib/http.js';

export async function onRequestGet({ env }) {
  return json({ customers: await listCustomers(env) });
}

export async function onRequestPost({ request, env, data }) {
  const body = await readJson(request);
  const email = normEmail(body.email);
  const company = String(body.company || '').trim();
  const audience = AUDIENCES[body.audience] ? body.audience : 'fleet';
  const password = typeof body.password === 'string' ? body.password : '';

  if (!EMAIL_RE.test(email)) return error('Please enter a valid email.', 400);
  if (!company) return error('Please enter the company name.', 400);
  if (password.length < MIN_PASSWORD) return error(`Password must be at least ${MIN_PASSWORD} characters.`, 400);
  if (await getCustomer(env, email)) return error(`An account for ${email} already exists.`, 409);

  const record = {
    email,
    company: company.slice(0, 200),
    audience,
    password_hash: await hashPassword(password),
    created_at: nowIso(),
    created_by: `staff:${data.admin.username}`,
    first_login_at: null,
    last_login_at: null,
    disabled: false,
    contacts: Array.isArray(body.contacts) ? cleanContacts(body.contacts) : null,
  };
  await putCustomer(env, record);
  return json({ customer: publicCustomer(record) }, 201);
}
