// The signed-in client's own profile + their Key Contacts (set by staff).
import { publicCustomer } from '../../_lib/store.js';
import { json } from '../../_lib/http.js';

export async function onRequestGet({ data }) {
  const c = publicCustomer(data.customer);
  return json({
    email: c.email,
    company: c.company,
    audience: c.audience,
    audience_label: c.audience_label,
    contacts: c.contacts,
  });
}
