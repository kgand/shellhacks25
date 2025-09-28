// src/screens/LoginScreen.js
import React, { useContext, useState } from 'react';
import { View, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { AuthContext } from '../context/AuthContext';
import { DEV_FLAGS } from '../config/dev';
import { Screen, Text } from '../ui/overrides/base';
import { theme } from '../utils/theme';

export default function LoginScreen({ navigation }) {
  const { signIn } = useContext(AuthContext);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const onLogin = async () => {
    // In demo mode, don't require credentials
    const res = await signIn(
      DEV_FLAGS.AUTH_BYPASS ? undefined : { email, password }
    );

    // If your signIn returns { ok: boolean }, accept both demo + real
    if (!res || res.ok) {
      // Context should re-render AppNavigator to show tabs.
      // Fallback: try to force navigation to the root tabs by name.
      try {
        navigation.reset?.({ index: 0, routes: [{ name: 'MainTabs' }] });
      } catch {}
    }
  };

  return (
    <Screen>
      <View style={styles.content}>
        <View style={styles.header}>
          <Text size="3xl" weight="bold" color="textPrimary" style={styles.title}>
            MetaSense
          </Text>
          <Text size="md" color="textSecondary" style={styles.subtitle}>
            Gentle memory cues.
          </Text>
        </View>

        <View style={styles.formCard}>
          {!DEV_FLAGS.AUTH_BYPASS && (
            <>
              <TextInput
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                placeholderTextColor={theme.colors.textSecondary}
                keyboardType="email-address"
                autoCapitalize="none"
                style={styles.input}
              />
              <TextInput
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                placeholderTextColor={theme.colors.textSecondary}
                secureTextEntry
                style={styles.input}
              />
            </>
          )}

          <TouchableOpacity style={styles.loginButton} onPress={onLogin}>
            <Text size="md" weight="semibold" color="textPrimary">
              {DEV_FLAGS.AUTH_BYPASS ? 'Enter (Demo Mode)' : 'Login'}
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: theme.spacing['3xl'],
  },
  header: {
    alignItems: 'center',
    marginBottom: theme.spacing['3xl'],
  },
  title: {
    marginBottom: theme.spacing.sm,
    textAlign: 'center',
  },
  subtitle: {
    textAlign: 'center',
  },
  formCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.xl,
    ...theme.shadows.subtle,
  },
  input: {
    color: theme.colors.textPrimary,
    borderColor: theme.colors.inputBorder,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    marginBottom: theme.spacing.lg,
    backgroundColor: theme.colors.inputBg,
    fontSize: theme.fonts?.sizes?.md ?? 15,
    fontFamily: 'Inter-Regular',
  },
  loginButton: {
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.lg,
    paddingVertical: theme.spacing.lg,
    alignItems: 'center',
    marginTop: theme.spacing.md,
  },
});