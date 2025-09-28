// src/ui/components/uber/PromoCard.tsx
import React from 'react';
import { TouchableOpacity, StyleSheet, View } from 'react-native';
import { Text } from '../../overrides/base';
import { theme } from '../../../utils/theme';

interface PromoCardProps {
  title: string;
  subtitle: string;
  buttonText?: string;
  onPress?: () => void;
}

export const PromoCard = ({ 
  title, 
  subtitle, 
  buttonText = "Book now", 
  onPress 
}: PromoCardProps) => {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.content}>
        <Text size="lg" weight="bold" color="textPrimary" style={styles.title}>
          {title}
        </Text>
        <Text size="md" color="textSecondary" style={styles.subtitle}>
          {subtitle}
        </Text>
        <TouchableOpacity style={styles.button}>
          <Text size="sm" weight="semibold" color="textPrimary">
            {buttonText}
          </Text>
        </TouchableOpacity>
      </View>
      <View style={styles.decorative}>
        <Text style={styles.decorativeEmoji}>🚗</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.xl,
    marginHorizontal: theme.spacing.lg,
    marginVertical: theme.spacing.lg,
    alignItems: 'center',
    ...theme.shadows.subtle,
  },
  content: {
    flex: 1,
  },
  title: {
    marginBottom: theme.spacing.sm,
  },
  subtitle: {
    marginBottom: theme.spacing.lg,
    lineHeight: (theme.fonts?.sizes?.md ?? 15) * 1.3,
  },
  button: {
    backgroundColor: theme.colors.background,
    borderRadius: theme.radii.sm,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
    alignSelf: 'flex-start',
  },
  decorative: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 60,
    height: 60,
  },
  decorativeEmoji: {
    fontSize: 32,
  },
});
