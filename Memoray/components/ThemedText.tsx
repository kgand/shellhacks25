// components/ThemedText.tsx
import * as React from 'react';
import { Text, type TextProps, StyleSheet } from 'react-native';
import { useThemeColor } from '../hooks/useThemeColor';

type Variant = 'title' | 'subtitle' | 'body' | 'muted' | 'label';

export type ThemedTextProps = TextProps & {
  color?: 'text' | 'textSecondary' | 'textMuted';
  variant?: Variant;
};

export function ThemedText({ style, color = 'text', variant = 'body', ...rest }: ThemedTextProps) {
  const resolved = useThemeColor({}, color);
  return <Text style={[styles[variant], { color: resolved }, style]} {...rest} />;
}

const styles = StyleSheet.create({
  title: { fontSize: 22, fontWeight: '700', lineHeight: 28 },
  subtitle: { fontSize: 17, fontWeight: '600', lineHeight: 22 },
  body: { fontSize: 15, lineHeight: 20 },
  muted: { fontSize: 14, lineHeight: 18, opacity: 0.9 },
  label: { fontSize: 12, fontWeight: '600', letterSpacing: 0.4 },
});
