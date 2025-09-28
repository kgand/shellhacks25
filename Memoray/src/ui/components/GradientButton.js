// src/ui/components/GradientButton.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { theme } from '../../utils/theme';

const GradientButton = ({ 
  children, 
  onPress, 
  style, 
  textStyle, 
  disabled = false,
  variant = 'primary', // 'primary', 'people', 'zones', 'alerts'
  ...props 
}) => {
  const getGradientColors = () => {
    switch (variant) {
      case 'people':
        return [theme.colors.peopleAccent, '#06B6D4'];
      case 'zones':
        return [theme.colors.zonesAccent, '#10B981'];
      case 'alerts':
        return [theme.colors.alertsAccent, '#F59E0B'];
      default:
        return [theme.colors.primaryGradientStart, theme.colors.primaryGradientEnd];
    }
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      style={[styles.container, style]}
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
    borderRadius: theme.radii.md,
    overflow: 'hidden',
    ...theme.shadows.glow,
  },
  gradient: {
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: '#FFFFFF',
    fontSize: theme.fonts.sizes.body,
    fontWeight: '600',
  },
});

export default GradientButton;
