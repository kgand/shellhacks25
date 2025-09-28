// src/dev/mockFetch.js
import { DEV_FLAGS } from '../config/dev';

// Only patch fetch in dev while MOCK_API is on
if (__DEV__ && DEV_FLAGS.MOCK_API && typeof global !== 'undefined') {
  const realFetch = global.fetch;

  const ok = (data, status = 200) =>
    new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    });

  global.fetch = async (input, init = {}) => {
    const url = typeof input === 'string' ? input : input?.url ?? '';
    const method = (init?.method || 'GET').toUpperCase();
    const path = url.replace(/^https?:\/\/[^/]+/, '');

    // Minimal stubs — adjust paths if your backend differs
    if (path.endsWith('/auth/login') && method === 'POST') {
      return ok({
        token: 'dev-token',
        user: { id: 'dev-user', name: 'Demo User', email: 'demo@metasense.app' },
      });
    }
    if (path.endsWith('/users/me') && method === 'GET') {
      return ok({ id: 'dev-user', name: 'Demo User', email: 'demo@metasense.app' });
    }

    // Fall through to real network for everything else
    return realFetch(input, init);
  };
}
