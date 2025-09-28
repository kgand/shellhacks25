// src/ui/components/GlassCard.js
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { BlurView } from 'expo-blur';
import { theme } from '../../utils/theme';

const GlassCard = ({ children, style, intensity = 20, tint = 'dark', ...props }) => {
  return (
    <View style={[styles.container, style]} {...props}>
      <BlurView
        intensity={intensity}
        tint={tint}
        style={styles.blurView}
      >
        <View style={styles.content}>
          {children}
        </View>
      </BlurView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: theme.radii.lg,
    overflow: 'hidden',
    backgroundColor: theme.colors.glassSurface,
    borderWidth: 1,
    borderColor: theme.colors.glassBorder,
    ...theme.shadows.glass,
  },
  blurView: {
    flex: 1,
  },
  content: {
    padding: theme.spacing.lg,
  },
});

export default GlassCard;
