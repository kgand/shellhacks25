import React from 'react';
import { View, StyleSheet, Modal, ActivityIndicator } from 'react-native';
import { BlurView } from 'expo-blur';
import { Text } from '../ui/overrides/base';
import { theme } from '../../utils/theme';

interface LoadingOverlayProps {
  visible: boolean;
  message?: string;
  transparent?: boolean;
}

const LoadingOverlay: React.FC<LoadingOverlayProps> = ({
  visible,
  message = 'Loading...',
  transparent = false,
}) => {
  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      statusBarTranslucent
    >
      <View style={styles.container}>
        {!transparent && (
          <BlurView
            intensity={20}
            style={StyleSheet.absoluteFillObject}
            tint="dark"
          />
        )}
        
        <View style={[
          styles.content,
          transparent && styles.transparentContent
        ]}>
          <View style={styles.spinnerContainer}>
            <ActivityIndicator
              size="large"
              color={theme.colors.accent}
            />
          </View>
          
          {message && (
            <Text style={styles.message} color="textSecondary">
              {message}
            </Text>
          )}
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  content: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.xl,
    alignItems: 'center',
    minWidth: 120,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 8,
  },
  transparentContent: {
    backgroundColor: 'transparent',
    shadowOpacity: 0,
    elevation: 0,
  },
  spinnerContainer: {
    marginBottom: theme.spacing.md,
  },
  message: {
    textAlign: 'center',
    fontSize: 16,
  },
});

export default LoadingOverlay;
