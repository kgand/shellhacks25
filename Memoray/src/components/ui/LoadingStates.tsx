import React from 'react';
import { View, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';

interface LoadingStatesProps {
  loading?: boolean;
  error?: string | null;
  empty?: boolean;
  emptyMessage?: string;
  emptyIcon?: string;
  onRetry?: () => void;
  children: React.ReactNode;
}

const LoadingStates: React.FC<LoadingStatesProps> = ({
  loading = false,
  error = null,
  empty = false,
  emptyMessage = 'No items found',
  emptyIcon = 'inbox-outline',
  onRetry,
  children,
}) => {
  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color={theme.colors.accent} />
        <Text size="md" color="textSecondary" style={styles.loadingText}>
          Loading...
        </Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text size="lg" weight="semibold" color="textPrimary" style={styles.errorTitle}>
          Failed to load
        </Text>
        <Text size="md" color="textSecondary" style={styles.errorMessage}>
          {error}
        </Text>
        {onRetry && (
          <TouchableOpacity style={styles.retryButton} onPress={onRetry}>
            <Text size="md" weight="semibold" color="textPrimary">
              Try Again
            </Text>
          </TouchableOpacity>
        )}
      </View>
    );
  }

  if (empty) {
    return (
      <View style={styles.container}>
        <Text size="lg" weight="semibold" color="textPrimary" style={styles.emptyTitle}>
          {emptyMessage}
        </Text>
        <Text size="md" color="textSecondary" style={styles.emptyMessage}>
          Get started by adding your first item
        </Text>
      </View>
    );
  }

  return <>{children}</>;
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  loadingText: {
    marginTop: theme.spacing.md,
    textAlign: 'center',
  },
  errorTitle: {
    marginBottom: theme.spacing.md,
    textAlign: 'center',
  },
  errorMessage: {
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: theme.spacing.xl,
  },
  retryButton: {
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.xl,
  },
  emptyTitle: {
    marginBottom: theme.spacing.md,
    textAlign: 'center',
  },
  emptyMessage: {
    textAlign: 'center',
    lineHeight: 24,
  },
});

export default LoadingStates;
