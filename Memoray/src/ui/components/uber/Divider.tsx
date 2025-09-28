// src/ui/components/uber/Divider.tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { theme } from '../../../utils/theme';

interface DividerProps {
  style?: any;
}

export const Divider = ({ style }: DividerProps) => {
  return <View style={[styles.divider, style]} />;
};

const styles = StyleSheet.create({
  divider: {
    height: 1,
    backgroundColor: theme.colors.border,
    marginHorizontal: theme.spacing.lg,
  },
});
