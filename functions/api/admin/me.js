import { json } from '../../_lib/http.js';

export async function onRequestGet({ data }) {
  return json({ username: data.admin.username });
}
