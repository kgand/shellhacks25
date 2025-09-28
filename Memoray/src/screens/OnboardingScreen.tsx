import React, { useState, useRef } from 'react';
import { View, StyleSheet, Dimensions, TouchableOpacity, Animated } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { Text } from '../ui/overrides/base';
import { theme } from '../utils/theme';

const { width } = Dimensions.get('window');

interface OnboardingScreenProps {
  onComplete?: () => void;
}

const OnboardingScreen: React.FC<OnboardingScreenProps> = ({ onComplete }) => {
  const navigation = useNavigation();
  const [currentStep, setCurrentStep] = useState(0);
  const scrollX = useRef(new Animated.Value(0)).current;

  const steps = [
    {
      title: 'Welcome to Memoray',
      subtitle: 'Your gentle memory companion',
      description: 'Memoray helps you remember important people, places, and daily tasks with gentle reminders.',
      icon: '🧠',
      color: '#6E7CF6',
    },
    {
      title: 'Smart Reminders',
      subtitle: 'Never miss what matters',
      description: 'Set reminders for medications, appointments, and daily activities. Get gentle prompts when you need them.',
      icon: '⏰',
      color: '#2EE98A',
    },
    {
      title: 'Memory Gallery',
      subtitle: 'Remember the people you love',
      description: 'Keep photos and memories of family, friends, and important places. Everything organized and easy to find.',
      icon: '📸',
      color: '#F59E0B',
    },
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Navigate to main tabs when onboarding is complete
      navigation.navigate('MainTabs' as never);
      onComplete?.();
    }
  };

  const handleSkip = () => {
    // Navigate to main tabs when skipping
    navigation.navigate('MainTabs' as never);
    onComplete?.();
  };

  const renderStep = (step: typeof steps[0], index: number) => (
    <View key={index} style={styles.stepContainer}>
      <View style={styles.iconContainer}>
        <Text style={styles.stepIcon}>{step.icon}</Text>
      </View>
      
      <Text size="2xl" weight="bold" color="textPrimary" style={styles.stepTitle}>
        {step.title}
      </Text>
      
      <Text size="lg" color="textSecondary" style={styles.stepSubtitle}>
        {step.subtitle}
      </Text>
      
      <Text size="md" color="textSecondary" style={styles.stepDescription}>
        {step.description}
      </Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#0F1113', '#1A1D1F', '#2A2E33']}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text size="xl" weight="bold" color="textPrimary">
            Memoray
          </Text>
          <TouchableOpacity onPress={handleSkip} style={styles.skipButton}>
            <Text size="sm" color="textSecondary">Skip</Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        <View style={styles.content}>
          {renderStep(steps[currentStep], currentStep)}
        </View>

        {/* Progress Indicators */}
        <View style={styles.progressContainer}>
          {steps.map((_, index) => (
            <View
              key={index}
              style={[
                styles.progressDot,
                index === currentStep && styles.progressDotActive,
              ]}
            />
          ))}
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <TouchableOpacity style={styles.nextButton} onPress={handleNext}>
            <Text size="md" weight="semibold" color="textPrimary">
              {currentStep === steps.length - 1 ? 'Get Started' : 'Next'}
            </Text>
            <Ionicons 
              name={currentStep === steps.length - 1 ? 'checkmark' : 'arrow-forward'} 
              size={20} 
              color={theme.colors.textPrimary} 
            />
          </TouchableOpacity>
        </View>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
    paddingTop: 50,
    paddingBottom: theme.spacing.lg,
  },
  skipButton: {
    padding: theme.spacing.sm,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
  },
  stepContainer: {
    alignItems: 'center',
    maxWidth: 300,
  },
  iconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: theme.colors.surface,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: theme.spacing.xl,
    borderWidth: 2,
    borderColor: theme.colors.border,
  },
  stepIcon: {
    fontSize: 40,
    lineHeight: 48,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  stepTitle: {
    textAlign: 'center',
    marginBottom: theme.spacing.sm,
  },
  stepSubtitle: {
    textAlign: 'center',
    marginBottom: theme.spacing.lg,
  },
  stepDescription: {
    textAlign: 'center',
    lineHeight: 24,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: theme.spacing.xl,
    gap: theme.spacing.sm,
  },
  progressDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.colors.border,
  },
  progressDotActive: {
    backgroundColor: theme.colors.accent,
    width: 24,
  },
  footer: {
    paddingHorizontal: theme.spacing.lg,
    paddingBottom: 40,
  },
  nextButton: {
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.lg,
    paddingHorizontal: theme.spacing.xl,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: theme.spacing.sm,
    minHeight: 56,
  },
});

export default OnboardingScreen;
