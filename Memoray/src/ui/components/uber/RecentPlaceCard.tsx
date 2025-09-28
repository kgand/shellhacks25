// src/ui/components/uber/RecentPlaceCard.tsx
import React from 'react';
import { TouchableOpacity, StyleSheet, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../overrides/base';

interface RecentPlaceCardProps {
  title: string;
  subtitle: string;
  onPress?: () => void;
}

export const RecentPlaceCard = ({ title, subtitle, onPress }: RecentPlaceCardProps) => {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.iconContainer}>
        <Ionicons name="time" size={16} color={theme.colors.textSecondary} />
      </View>
      <View style={styles.content}>
        <Text size="md" weight="semibold" color="textPrimary" style={styles.title}>
          {title}
        </Text>
        <Text size="sm" color="textSecondary" style={styles.subtitle}>
          {subtitle}
        </Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    marginHorizontal: theme.spacing.lg,
    marginBottom: theme.spacing.sm,
    ...theme.shadows.subtle,
  },
  iconContainer: {
    width: 32,
    height: 32,
    borderRadius: theme.radii.sm,
    backgroundColor: theme.colors.surfaceAlt,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: theme.spacing.md,
  },
  content: {
    flex: 1,
  },
  title: {
    marginBottom: 2,
  },
  subtitle: {
    lineHeight: (theme.fonts?.sizes?.sm ?? 13) * 1.2,
  },
});
