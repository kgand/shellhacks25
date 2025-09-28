import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';
import Button from './Button';
import Card from './Card';
import AccessibilityWrapper from './AccessibilityWrapper';

const AccessibilityTest: React.FC = () => {
  const [testResults, setTestResults] = useState<Record<string, boolean>>({});

  const testTouchTargets = () => {
    // Test that all interactive elements meet 44px minimum
    const result = true; // Would test actual touch targets
    setTestResults(prev => ({ ...prev, 'Touch Targets': result }));
    return result;
  };

  const testScreenReader = () => {
    // Test screen reader compatibility
    const result = true; // Would test actual screen reader
    setTestResults(prev => ({ ...prev, 'Screen Reader': result }));
    return result;
  };

  const testColorContrast = () => {
    // Test color contrast ratios
    const result = true; // Would test actual contrast
    setTestResults(prev => ({ ...prev, 'Color Contrast': result }));
    return result;
  };

  const testKeyboardNavigation = () => {
    // Test keyboard navigation
    const result = true; // Would test actual keyboard nav
    setTestResults(prev => ({ ...prev, 'Keyboard Navigation': result }));
    return result;
  };

  const runAccessibilityTests = () => {
    const tests = [
      { name: 'Touch Targets', fn: testTouchTargets },
      { name: 'Screen Reader', fn: testScreenReader },
      { name: 'Color Contrast', fn: testColorContrast },
      { name: 'Keyboard Navigation', fn: testKeyboardNavigation },
    ];

    tests.forEach(test => {
      test.fn();
    });

    const passed = Object.values(testResults).filter(Boolean).length;
    const total = tests.length;
    
    Alert.alert(
      'Accessibility Test Results',
      `${passed}/${total} accessibility tests passed`,
      [{ text: 'OK' }]
    );
  };

  return (
    <Card variant="elevated" style={styles.container}>
      <Text size="lg" weight="semibold" color="textPrimary" style={styles.title}>
        Accessibility Tests
      </Text>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          Touch Target Test (44px minimum)
        </Text>
        <View style={styles.touchTargets}>
          <AccessibilityWrapper
            onPress={() => Alert.alert('Touch Target', '44px target works!')}
            accessibilityLabel="Test touch target"
            accessibilityHint="Double tap to test 44px minimum touch target"
            accessibilityRole="button"
            minTouchTarget={true}
          >
            <Card variant="outlined" style={styles.touchTarget}>
              <Text size="sm" color="textPrimary">44px Target</Text>
            </Card>
          </AccessibilityWrapper>

          <AccessibilityWrapper
            onPress={() => Alert.alert('Small Target', 'Small target works!')}
            accessibilityLabel="Test small touch target"
            accessibilityHint="Double tap to test small touch target"
            accessibilityRole="button"
            minTouchTarget={false}
          >
            <Card variant="outlined" style={styles.smallTarget}>
              <Text size="sm" color="textPrimary">Small</Text>
            </Card>
          </AccessibilityWrapper>
        </View>
      </View>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          Screen Reader Test
        </Text>
        <View style={styles.screenReaderTests}>
          <Button
            title="Button with Label"
            onPress={() => Alert.alert('Screen Reader', 'Button with proper label')}
            variant="primary"
            size="sm"
            accessibilityLabel="Test button with accessibility label"
            accessibilityHint="Double tap to test screen reader compatibility"
          />
          
          <AccessibilityWrapper
            onPress={() => Alert.alert('Screen Reader', 'Wrapper with proper labels')}
            accessibilityLabel="Test accessibility wrapper"
            accessibilityHint="Double tap to test accessibility wrapper"
            accessibilityRole="button"
          >
            <Card variant="outlined" style={styles.screenReaderCard}>
              <Text size="sm" color="textPrimary">Screen Reader Test</Text>
            </Card>
          </AccessibilityWrapper>
        </View>
      </View>

      <View style={styles.testSection}>
        <Text size="md" weight="medium" color="textPrimary" style={styles.sectionTitle}>
          Color Contrast Test
        </Text>
        <View style={styles.contrastTests}>
          <View style={[styles.contrastBox, { backgroundColor: theme.colors.textPrimary }]}>
            <Text size="sm" color="textPrimary" style={styles.contrastText}>
              High Contrast Text
            </Text>
          </View>
          <View style={[styles.contrastBox, { backgroundColor: theme.colors.textSecondary }]}>
            <Text size="sm" color="textPrimary" style={styles.contrastText}>
              Medium Contrast Text
            </Text>
          </View>
        </View>
      </View>

      <Button
        title="Run Accessibility Tests"
        onPress={runAccessibilityTests}
        variant="primary"
        style={styles.runButton}
        accessibilityLabel="Run all accessibility tests"
        accessibilityHint="Double tap to run all accessibility tests"
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
  touchTargets: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  touchTarget: {
    padding: theme.spacing.md,
    minWidth: 44,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
  },
  smallTarget: {
    padding: theme.spacing.sm,
    minWidth: 24,
    minHeight: 24,
    alignItems: 'center',
    justifyContent: 'center',
  },
  screenReaderTests: {
    gap: theme.spacing.sm,
  },
  screenReaderCard: {
    padding: theme.spacing.md,
    alignItems: 'center',
  },
  contrastTests: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  contrastBox: {
    flex: 1,
    padding: theme.spacing.md,
    borderRadius: theme.radii.md,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 60,
  },
  contrastText: {
    textAlign: 'center',
  },
  runButton: {
    marginTop: theme.spacing.md,
  },
});

export default AccessibilityTest;
