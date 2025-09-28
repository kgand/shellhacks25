import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Modal, Animated } from 'react-native';
import { BlurView } from 'expo-blur';
import { Text } from '../ui/overrides/base';
import { theme } from '../../utils/theme';
import ProgressButton from './ProgressButton';

interface ProcessingSheetProps {
  visible: boolean;
  title: string;
  message: string;
  progress: number; // 0-100
  onCancel?: () => void;
  showCancel?: boolean;
  cancelText?: string;
}

const ProcessingSheet: React.FC<ProcessingSheetProps> = ({
  visible,
  title,
  message,
  progress,
  onCancel,
  showCancel = true,
  cancelText = 'Cancel',
}) => {
  const slideAnim = useRef(new Animated.Value(0)).current;
  const progressAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (visible) {
      Animated.spring(slideAnim, {
        toValue: 1,
        useNativeDriver: true,
        tension: 100,
        friction: 8,
      }).start();
    } else {
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 250,
        useNativeDriver: true,
      }).start();
    }
  }, [visible, slideAnim]);

  useEffect(() => {
    Animated.timing(progressAnim, {
      toValue: progress,
      duration: 300,
      useNativeDriver: false,
    }).start();
  }, [progress, progressAnim]);

  const translateY = slideAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [400, 0],
  });

  return (
    <Modal
      visible={visible}
      transparent
      animationType="none"
      statusBarTranslucent
    >
      <View style={styles.container}>
        <BlurView
          intensity={20}
          style={StyleSheet.absoluteFillObject}
          tint="dark"
        />
        
        <Animated.View
          style={[
            styles.sheet,
            {
              transform: [{ translateY }],
            },
          ]}
        >
          {/* Handle */}
          <View style={styles.handle} />
          
          {/* Content */}
          <View style={styles.content}>
            <Text style={styles.title} color="textPrimary" weight="semibold">
              {title}
            </Text>
            
            <Text style={styles.message} color="textSecondary">
              {message}
            </Text>
            
            {/* Progress Bar */}
            <View style={styles.progressContainer}>
              <View style={styles.progressTrack}>
                <Animated.View
                  style={[
                    styles.progressFill,
                    {
                      width: progressAnim.interpolate({
                        inputRange: [0, 100],
                        outputRange: ['0%', '100%'],
                      }),
                    },
                  ]}
                />
              </View>
              <Text style={styles.progressText} color="textSecondary">
                {Math.round(progress)}%
              </Text>
            </View>
            
            {/* Cancel Button */}
            {showCancel && onCancel && (
              <View style={styles.cancelContainer}>
                <ProgressButton
                  title={cancelText}
                  onPress={onCancel}
                  variant="ghost"
                  size="md"
                />
              </View>
            )}
          </View>
        </Animated.View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  sheet: {
    backgroundColor: theme.colors.surface,
    borderTopLeftRadius: theme.radii.xl,
    borderTopRightRadius: theme.radii.xl,
    paddingTop: theme.spacing.md,
    paddingBottom: theme.spacing.xl,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: -4,
    },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 8,
  },
  handle: {
    width: 40,
    height: 4,
    backgroundColor: theme.colors.border,
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: theme.spacing.lg,
  },
  content: {
    paddingHorizontal: theme.spacing.xl,
    alignItems: 'center',
  },
  title: {
    fontSize: 20,
    marginBottom: theme.spacing.sm,
    textAlign: 'center',
  },
  message: {
    fontSize: 16,
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  progressContainer: {
    width: '100%',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  progressTrack: {
    width: '100%',
    height: 8,
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: 4,
    overflow: 'hidden',
    marginBottom: theme.spacing.sm,
  },
  progressFill: {
    height: '100%',
    backgroundColor: theme.colors.accent,
    borderRadius: 4,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
  },
  cancelContainer: {
    marginTop: theme.spacing.md,
  },
});

export default ProcessingSheet;
