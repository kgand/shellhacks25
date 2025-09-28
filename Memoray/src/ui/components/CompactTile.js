// src/ui/components/CompactTile.js
import React from 'react';
import { TouchableOpacity, StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';
import { Text } from '../overrides/base';

const CompactTile = ({ emoji, label, onPress }) => {
  return (
    <TouchableOpacity
      style={styles.tile}
      onPress={onPress}
      activeOpacity={0.8}
    >
      <Text style={styles.emoji}>{emoji}</Text>
      <Text size="xs" color="textPrimary" style={styles.label}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  tile: {
    width: 96,
    height: 96,
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    alignItems: 'center',
    justifyContent: 'center',
    padding: theme.spacing.sm,
  },
  emoji: {
    fontSize: 24,
    marginBottom: theme.spacing.xs,
  },
  label: {
    textAlign: 'center',
    fontFamily: 'Inter-Regular',
  },
});

export default CompactTile;
