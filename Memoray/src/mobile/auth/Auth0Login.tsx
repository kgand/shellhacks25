// src/mobile/auth/Auth0Login.tsx
import * as React from 'react';
import { Button, View, Text } from 'react-native';
import * as WebBrowser from 'expo-web-browser';
import * as SecureStore from 'expo-secure-store';
import Constants from 'expo-constants';
import {
  makeRedirectUri,
  useAuthRequest,
  useAutoDiscovery,
  exchangeCodeAsync,
  revokeAsync,
  ResponseType,
} from 'expo-auth-session';

WebBrowser.maybeCompleteAuthSession();

const AUTH0_DOMAIN = 'https://dev-65glq2dbqdgmchei.us.auth0.com';
const CLIENT_ID = 'UMpSLl81GLE4QkLj1xQKfnBdJJTKGBLM';

const isExpoGo = Constants.appOwnership === 'expo';

const redirectUri = isExpoGo
  ? makeRedirectUri() // https://auth.expo.io/@aaravbejjinki/memoray
  : makeRedirectUri({ scheme: 'memoray', path: 'redirect' }); // memoray://redirect

export default function Auth0Login() {
  const discovery = useAutoDiscovery(AUTH0_DOMAIN);
  const [request, response, promptAsync] = useAuthRequest(
    {
      clientId: CLIENT_ID,
      responseType: ResponseType.Code,
      redirectUri,
      scopes: ['openid', 'profile', 'email', 'offline_access'],
      usePKCE: true,
    },
    discovery
  );

  const [profile, setProfile] = React.useState<any>(null);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    (async () => {
      if (response?.type === 'success' && discovery && request) {
        try {
          const tokenRes = await exchangeCodeAsync(
            {
              clientId: CLIENT_ID,
              code: response.params.code,
              redirectUri,
              extraParams: { code_verifier: request.codeVerifier! },
            },
            discovery
          );

          await SecureStore.setItemAsync('access_token', tokenRes.accessToken ?? '');
          if (tokenRes.refreshToken) {
            await SecureStore.setItemAsync('refresh_token', tokenRes.refreshToken);
          }

          const me = await fetch(`${AUTH0_DOMAIN}/userinfo`, {
            headers: { Authorization: `Bearer ${tokenRes.accessToken}` },
          }).then(r => r.json());

          setProfile(me);
          setError(null);
        } catch (e: any) {
          console.warn('Auth0 exchange error:', e);
          setError(e?.message ?? 'Login failed');
        }
      }
    })();
  }, [response, discovery, request]);

  async function onLogin() {
    // No options; redirectUri already decides proxy vs scheme
    await promptAsync();
  }

  async function onLogout() {
    try {
      const accessToken = await SecureStore.getItemAsync('access_token');
      if (accessToken && discovery) {
        await revokeAsync({ token: accessToken, clientId: CLIENT_ID }, discovery);
      }
    } catch {
      /* ignore */
    } finally {
      await SecureStore.deleteItemAsync('access_token');
      await SecureStore.deleteItemAsync('refresh_token');
    }

    await WebBrowser.openBrowserAsync(
      `${AUTH0_DOMAIN}/v2/logout?client_id=${CLIENT_ID}&returnTo=${encodeURIComponent(
        isExpoGo ? 'https://auth.expo.io/@aaravbejjinki/memoray' : 'memoray://logout'
      )}`
    );

    setProfile(null);
  }

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', gap: 16, padding: 24 }}>
      <Text style={{ fontSize: 22, fontWeight: '700' }}>Memoray</Text>
      <Text style={{ opacity: 0.7 }}>
        Env: {isExpoGo ? 'Expo Go (proxy)' : 'Dev/Standalone (scheme)'}
      </Text>
      {error ? <Text style={{ color: 'tomato' }}>{error}</Text> : null}

      {profile ? (
        <>
          <Text>Hi {profile.name || profile.email}</Text>
          <Button title="Logout" onPress={onLogout} />
        </>
      ) : (
        <Button title="Login with Auth0" disabled={!request} onPress={onLogin} />
      )}
    </View>
  );
}
