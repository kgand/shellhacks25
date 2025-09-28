import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';
import Button from './Button';
import Card from './Card';
import LoadingStates from './LoadingStates';
import ErrorBoundary from './ErrorBoundary';

const ErrorRecoveryTest: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any[]>([]);

  const simulateLoading = () => {
    setLoading(true);
    setError(null);
    
    setTimeout(() => {
      setLoading(false);
      setData([{ id: 1, name: 'Test Data' }]);
    }, 2000);
  };

  const simulateError = () => {
    setLoading(true);
    setError(null);
    
    setTimeout(() => {
      setLoading(false);
      setError('Failed to load data. Please try again.');
    }, 2000);
  };

  const simulateEmpty = () => {
    setLoading(true);
    setError(null);
    
    setTimeout(() => {
      setLoading(false);
      setData([]);
    }, 2000);
  };

  const retry = () => {
    setError(null);
    simulateLoading();
  };

  const clearData = () => {
    setData([]);
    setError(null);
    setLoading(false);
  };

  return (
    <Card variant="elevated" style={styles.container}>
      <Text size="lg" weight="semibold" color="textPrimary" style={styles.title}>
        Error Recovery Tests
      </Text>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          Loading States
        </Text>
        <View style={styles.buttonRow}>
          <Button
            title="Simulate Loading"
            onPress={simulateLoading}
            variant="primary"
            size="sm"
            accessibilityLabel="Simulate loading state"
          />
          <Button
            title="Simulate Error"
            onPress={simulateError}
            variant="danger"
            size="sm"
            accessibilityLabel="Simulate error state"
          />
          <Button
            title="Simulate Empty"
            onPress={simulateEmpty}
            variant="secondary"
            size="sm"
            accessibilityLabel="Simulate empty state"
          />
        </View>
      </View>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          State Management
        </Text>
        <LoadingStates
          loading={loading}
          error={error}
          empty={!loading && !error && data.length === 0}
          emptyMessage="No data available"
          onRetry={retry}
        >
          <View style={styles.dataContainer}>
            {data.map((item) => (
              <Card key={item.id} variant="outlined" style={styles.dataItem}>
                <Text size="md" color="textPrimary">
                  {item.name}
                </Text>
              </Card>
            ))}
          </View>
        </LoadingStates>
      </View>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          Error Boundary Test
        </Text>
        <ErrorBoundary
          fallback={
            <Card variant="outlined" style={styles.errorBoundaryCard}>
              <Text size="md" color="textPrimary" style={styles.errorText}>
                Error Boundary Caught an Error
              </Text>
              <Button
                title="Retry"
                onPress={() => Alert.alert('Retry', 'Error boundary retry')}
                variant="primary"
                size="sm"
                style={styles.retryButton}
              />
            </Card>
          }
        >
          <Button
            title="Trigger Error"
            onPress={() => {
              throw new Error('Test error for error boundary');
            }}
            variant="danger"
            size="sm"
            accessibilityLabel="Trigger error for testing error boundary"
          />
        </ErrorBoundary>
      </View>

      <Button
        title="Clear All Data"
        onPress={clearData}
        variant="ghost"
        style={styles.clearButton}
        accessibilityLabel="Clear all test data"
      />
    </Card>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: theme.spacing.lg,
  },
  title: {
    marginBottom: theme.spacing.lg,
  },
  testSection: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    marginBottom: theme.spacing.sm,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    flexWrap: 'wrap',
  },
  dataContainer: {
    gap: theme.spacing.sm,
  },
  dataItem: {
    padding: theme.spacing.md,
  },
  errorBoundaryCard: {
    padding: theme.spacing.lg,
    alignItems: 'center',
  },
  errorText: {
    marginBottom: theme.spacing.md,
    textAlign: 'center',
  },
  retryButton: {
    marginTop: theme.spacing.sm,
  },
  clearButton: {
    marginTop: theme.spacing.md,
  },
});

export default ErrorRecoveryTest;
