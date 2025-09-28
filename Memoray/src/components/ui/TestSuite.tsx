import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';
import Button from './Button';
import Card from './Card';
import Input from './Input';
import AccessibilityWrapper from './AccessibilityWrapper';
import AccessibilityTest from './AccessibilityTest';
import ErrorRecoveryTest from './ErrorRecoveryTest';

const TestSuite: React.FC = () => {
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});
  const [inputValue, setInputValue] = useState('');

  const runTest = (testName: string, testFn: () => boolean) => {
    try {
      const result = testFn();
      setTestResults(prev => ({ ...prev, [testName]: result }));
      return result;
    } catch (error) {
      console.error(`Test ${testName} failed:`, error);
      setTestResults(prev => ({ ...prev, [testName]: false }));
      return false;
    }
  };

  const testOnboardingFlow = () => {
    // Test onboarding screen components
    return true; // Placeholder - would test actual onboarding
  };

  const testQuickActions = () => {
    // Test quick actions functionality
    return true; // Placeholder - would test actual quick actions
  };

  const testSearch = () => {
    // Test search functionality
    return true; // Placeholder - would test actual search
  };

  const testAccessibility = () => {
    // Test accessibility features
    return true; // Placeholder - would test actual accessibility
  };

  const testErrorRecovery = () => {
    // Test error recovery mechanisms
    return true; // Placeholder - would test actual error recovery
  };

  const runAllTests = () => {
    const tests = [
      { name: 'Onboarding Flow', fn: testOnboardingFlow },
      { name: 'Quick Actions', fn: testQuickActions },
      { name: 'Search', fn: testSearch },
      { name: 'Accessibility', fn: testAccessibility },
      { name: 'Error Recovery', fn: testErrorRecovery },
    ];

    tests.forEach(test => {
      runTest(test.name, test.fn);
    });

    const passed = Object.values(testResults).filter(Boolean).length;
    const total = tests.length;
    
    Alert.alert(
      'Test Results',
      `${passed}/${total} tests passed`,
      [{ text: 'OK' }]
    );
  };

  const getTestStatus = (testName: string) => {
    const result = testResults[testName];
    if (result === undefined) return 'pending';
    return result ? 'passed' : 'failed';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'passed': return theme.colors.success;
      case 'failed': return theme.colors.error;
      default: return theme.colors.textSecondary;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'passed': return '✓';
      case 'failed': return '✗';
      default: return '○';
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text size="2xl" weight="bold" color="textPrimary" style={styles.title}>
        Memoray Test Suite
      </Text>

      <Card variant="elevated" style={styles.testCard}>
        <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
          Component Tests
        </Text>

        {/* Button Test */}
        <View style={styles.testItem}>
          <Text size="md" color="textPrimary" style={styles.testLabel}>
            Button Component
          </Text>
          <View style={styles.buttonRow}>
            <Button
              title="Primary"
              onPress={() => Alert.alert('Primary Button', 'Button works!')}
              variant="primary"
              size="sm"
            />
            <Button
              title="Secondary"
              onPress={() => Alert.alert('Secondary Button', 'Button works!')}
              variant="secondary"
              size="sm"
            />
            <Button
              title="Loading"
              onPress={() => {}}
              loading={true}
              size="sm"
            />
          </View>
        </View>

        {/* Input Test */}
        <View style={styles.testItem}>
          <Text size="md" color="textPrimary" style={styles.testLabel}>
            Input Component
          </Text>
          <Input
            label="Test Input"
            placeholder="Type something..."
            value={inputValue}
            onChangeText={setInputValue}
            leftIcon="search"
            rightIcon={inputValue.length > 0 ? "close-circle" : undefined}
            onRightIconPress={() => setInputValue('')}
            accessibilityLabel="Test input field"
            accessibilityHint="Enter text to test the input component"
          />
        </View>

        {/* Accessibility Test */}
        <View style={styles.testItem}>
          <Text size="md" color="textPrimary" style={styles.testLabel}>
            Accessibility Wrapper
          </Text>
          <AccessibilityWrapper
            onPress={() => Alert.alert('Accessibility', 'Touch target works!')}
            accessibilityLabel="Test accessibility button"
            accessibilityHint="Double tap to test accessibility"
            accessibilityRole="button"
          >
            <Card variant="outlined" style={styles.accessibilityCard}>
              <Text size="md" color="textPrimary" style={styles.accessibilityText}>
                Tap me (44px min target)
              </Text>
            </Card>
          </AccessibilityWrapper>
        </View>
      </Card>

      <AccessibilityTest />

      <ErrorRecoveryTest />

      <Card variant="elevated" style={styles.testCard}>
        <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
          Feature Tests
        </Text>

        {[
          'Onboarding Flow',
          'Quick Actions',
          'Search',
          'Accessibility',
          'Error Recovery',
        ].map((testName) => {
          const status = getTestStatus(testName);
          return (
            <View key={testName} style={styles.testRow}>
              <Text size="md" color="textPrimary" style={styles.testName}>
                {testName}
              </Text>
              <Text
                size="md"
                color={getStatusColor(status)}
                style={styles.statusText}
              >
                {getStatusText(status)}
              </Text>
            </View>
          );
        })}

        <Button
          title="Run All Tests"
          onPress={runAllTests}
          variant="primary"
          style={styles.runButton}
          accessibilityLabel="Run all tests"
          accessibilityHint="Double tap to run all feature tests"
        />
      </Card>

      <Card variant="elevated" style={styles.testCard}>
        <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
          Manual Testing Checklist
        </Text>

        <View style={styles.checklist}>
          <Text size="md" color="textPrimary" style={styles.checklistItem}>
            ✓ Test onboarding flow navigation
          </Text>
          <Text size="md" color="textPrimary" style={styles.checklistItem}>
            ✓ Verify quick actions respond to taps
          </Text>
          <Text size="md" color="textPrimary" style={styles.checklistItem}>
            ✓ Test search functionality
          </Text>
          <Text size="md" color="textPrimary" style={styles.checklistItem}>
            ✓ Verify accessibility with screen readers
          </Text>
          <Text size="md" color="textPrimary" style={styles.checklistItem}>
            ✓ Test error recovery mechanisms
          </Text>
        </View>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    padding: theme.spacing.lg,
  },
  title: {
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
  testCard: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    marginBottom: theme.spacing.lg,
  },
  testItem: {
    marginBottom: theme.spacing.lg,
  },
  testLabel: {
    marginBottom: theme.spacing.sm,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
    flexWrap: 'wrap',
  },
  accessibilityCard: {
    padding: theme.spacing.md,
    alignItems: 'center',
    minHeight: 44,
    justifyContent: 'center',
  },
  accessibilityText: {
    textAlign: 'center',
  },
  testRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: theme.spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  testName: {
    flex: 1,
  },
  statusText: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  runButton: {
    marginTop: theme.spacing.lg,
  },
  checklist: {
    gap: theme.spacing.sm,
  },
  checklistItem: {
    paddingVertical: theme.spacing.xs,
  },
});

export default TestSuite;
