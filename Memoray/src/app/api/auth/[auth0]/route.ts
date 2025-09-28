import {
    handleAuth,
    handleLogin,
    handleLogout,
    handleCallback,
  } from '@auth0/nextjs-auth0';
  
  export const GET = handleAuth({
    login: handleLogin({ returnTo: '/dashboard' }),
    logout: handleLogout({ returnTo: '/' }),
    callback: handleCallback(),
  });
  
  export const POST = GET; // allow POST for same endpoints
  