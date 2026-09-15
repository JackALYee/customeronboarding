// Recent sign-ins (customers + staff) for the Activity tab.
import { recentEvents, countEvents } from '../../_lib/store.js';
import { json } from '../../_lib/http.js';

export async function onRequestGet({ request, env }) {
  const limit = Math.min(200, Math.max(1, parseInt(new URL(request.url).searchParams.get('limit') || '50', 10) || 50));
  const [events, total] = await Promise.all([recentEvents(env, limit), countEvents(env)]);
  return json({ events, total: total.count, total_capped: total.capped });
}
