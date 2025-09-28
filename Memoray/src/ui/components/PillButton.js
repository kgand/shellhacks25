// src/ui/components/PillButton.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

const PillButton = ({ 
  children, 
  onPress, 
  style, 
  textStyle, 
  disabled = false,
  variant = 'neutral', // 'neutral', 'accent'
  ...props 
}) => {
  const getBackgroundColor = () => {
    switch (variant) {
      case 'accent':
        return theme.colors.accentGreen;
      default:
        return theme.colors.pill;
    }
  };

  const getTextColor = () => {
    switch (variant) {
      case 'accent':
        return '#000000';
      default:
        return theme.colors.textPrimary;
    }
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      style={[
        styles.container, 
        { backgroundColor: getBackgroundColor() },
        disabled && styles.disabled, 
        style
      ]}
      accessibilityRole="button"
      accessibilityLabel={typeof children === 'string' ? children : 'Button'}
      hitSlop={10}
      {...props}
    >
      <Text style={[styles.text, { color: getTextColor() }, textStyle]}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: theme.radii.pill,
    paddingVertical: theme.spacing.lg,
    paddingHorizontal: theme.spacing.xxl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44, // Minimum tap target
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    fontSize: theme.fonts.sizes.body,
    fontWeight: theme.fonts.weights.semibold,
    fontFamily: 'Inter-SemiBold',
  },
});

export default PillButton;
