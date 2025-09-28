// src/ui/components/uber/SectionHeader.tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from '../../overrides/base';
import { theme } from '../../../utils/theme';

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export const SectionHeader = ({ title, subtitle, action }: SectionHeaderProps) => {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Text size="xl" weight="bold" color="textPrimary" style={styles.title}>
          {title}
        </Text>
        {subtitle && (
          <Text size="md" color="textSecondary" style={styles.subtitle}>
            {subtitle}
          </Text>
        )}
      </View>
      {action && <View style={styles.action}>{action}</View>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginHorizontal: theme.spacing.lg,
    marginTop: theme.spacing['3xl'],
    marginBottom: theme.spacing.lg,
  },
  content: {
    flex: 1,
  },
  title: {
    marginBottom: theme.spacing.xs,
  },
  subtitle: {
    lineHeight: (theme.fonts?.sizes?.md ?? 15) * 1.3,
  },
  action: {
    marginLeft: theme.spacing.lg,
  },
});
