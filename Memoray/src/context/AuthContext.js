// src/context/AuthContext.js
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react';
import { DEV_FLAGS } from '../config/dev';

const initial = {
  user: null,
  loading: true,
  // keep signatures stable so existing code works
  signIn: async (_creds) => ({ ok: false }),
  signOut: async () => {},
};

export const AuthContext = createContext(initial);

// ✅ Export a hook so other modules can `import { useAuth } from '../context/AuthContext'`
export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Initialize on mount
  useEffect(() => {
    let mounted = true;

    const init = async () => {
      if (DEV_FLAGS.AUTH_BYPASS) {
        if (mounted) {
          setUser({
            id: 'dev-user',
            name: 'Demo User',
            email: 'demo@metasense.app',
          });
          setLoading(false);
        }
        return;
      }

      // Real init (safe fail)
      try {
        // If your app normally calls /users/me here,
        // our dev mock in src/dev/mockFetch.js will return a demo user.
        const res = await fetch('/users/me').then((r) => r.json());
        if (mounted) setUser(res ?? null);
      } catch {
        if (mounted) setUser(null);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    init();
    return () => {
      mounted = false;
    };
  }, []);

  // Accept either (email,password) object or nothing in demo
  const signIn = useCallback(async (creds) => {
    if (DEV_FLAGS.AUTH_BYPASS) {
      setUser({
        id: 'dev-user',
        name: 'Demo User',
        email: 'demo@metasense.app',
      });
      return { ok: true };
    }

    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(creds || {}),
      }).then((r) => r.json());

      const nextUser = res?.user ?? null;
      setUser(nextUser);
      return { ok: !!nextUser };
    } catch {
      return { ok: false };
    }
  }, []);

  const signOut = useCallback(async () => {
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, loading, signIn, signOut }),
    [user, loading, signIn, signOut]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
