// src/ui/components/uber/SuggestionTile.tsx
import React from 'react';
import { TouchableOpacity, StyleSheet, View } from 'react-native';
import { Text } from '../../overrides/base';
import { theme } from '../../../utils/theme';

interface SuggestionTileProps {
  emoji: string;
  label: string;
  onPress?: () => void;
  promo?: boolean;
}

export const SuggestionTile = ({ emoji, label, onPress, promo = false }: SuggestionTileProps) => {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      {promo && (
        <View style={styles.promoBadge}>
          <Text size="xs" weight="semibold" color="textPrimary">Promo</Text>
        </View>
      )}
      <Text style={styles.emoji}>{emoji}</Text>
      <Text size="sm" weight="semibold" color="textPrimary" style={styles.label}>
        {label}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    aspectRatio: 1,
    position: 'relative',
    ...theme.shadows.subtle,
  },
  promoBadge: {
    position: 'absolute',
    top: theme.spacing.sm,
    left: theme.spacing.sm,
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.sm,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: 2,
  },
  emoji: {
    fontSize: 24,
    marginBottom: theme.spacing.sm,
  },
  label: {
    textAlign: 'center',
  },
});
