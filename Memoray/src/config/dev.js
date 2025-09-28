// src/config/dev.js
// Safe dev-only switches (never ship with AUTH_BYPASS = true)
export const DEV_FLAGS = {
    AUTH_BYPASS: true, // tap Login → go straight into the app
    MOCK_API: true     // fake /auth/login and /users/me for Expo Go demos
  };
  