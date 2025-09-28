// components/ThemedView.tsx
import * as React from 'react';
import { View, type ViewProps } from 'react-native';
import { useThemeColor } from '../hooks/useThemeColor';

export type ThemedViewProps = ViewProps & {
  background?: 'background' | 'card';
};

export function ThemedView({ style, background = 'background', ...otherProps }: ThemedViewProps) {
  const bg = useThemeColor({}, background);
  return <View style={[{ backgroundColor: bg }, style]} {...otherProps} />;
}
