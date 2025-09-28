// src/ui/components/PrimaryButton.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { theme } from '../../utils/theme';

const PrimaryButton = ({ 
  children, 
  onPress, 
  style, 
  textStyle, 
  disabled = false,
  variant = 'primary', // 'primary', 'people', 'zones', 'alert'
  ...props 
}) => {
  const getGradientColors = () => {
    switch (variant) {
      case 'people':
        return [theme.colors.people, '#06B6D4'];
      case 'zones':
        return [theme.colors.zones, '#10B981'];
      case 'alert':
        return [theme.colors.alert, '#F59E0B'];
      default:
        return [theme.colors.primaryGradientStart, theme.colors.primaryGradientEnd];
    }
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      style={[styles.container, style]}
      accessibilityRole="button"
      accessibilityLabel={typeof children === 'string' ? children : 'Button'}
      hitSlop={10}
      {...props}
    >
      <LinearGradient
        colors={getGradientColors()}
        style={[styles.gradient, disabled && styles.disabled]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 0 }}
      >
        <Text style={[styles.text, textStyle]}>
          {children}
        </Text>
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: theme.radii.lg,
    overflow: 'hidden',
    minHeight: 44, // Minimum tap target
    ...theme.shadows.card,
  },
  gradient: {
    paddingVertical: theme.spacing.lg,
    paddingHorizontal: theme.spacing.xxl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44,
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: '#FFFFFF',
    fontSize: theme.fonts.sizes.body,
    fontWeight: theme.fonts.weights.medium,
  },
});

export default PrimaryButton;
