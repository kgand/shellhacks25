// src/ui/components/SecondaryButton.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

const SecondaryButton = ({ 
  children, 
  onPress, 
  style, 
  textStyle, 
  disabled = false,
  ...props 
}) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      style={[styles.container, disabled && styles.disabled, style]}
      accessibilityRole="button"
      accessibilityLabel={typeof children === 'string' ? children : 'Button'}
      hitSlop={10}
      {...props}
    >
      <Text style={[styles.text, textStyle]}>
        {children}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: theme.radii.lg,
    borderWidth: 1,
    borderColor: theme.colors.border,
    paddingVertical: theme.spacing.lg,
    paddingHorizontal: theme.spacing.xxl,
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 44, // Minimum tap target
    backgroundColor: theme.colors.surface,
  },
  disabled: {
    opacity: 0.5,
  },
  text: {
    color: theme.colors.text,
    fontSize: theme.fonts.sizes.body,
    fontWeight: theme.fonts.weights.medium,
  },
});

export default SecondaryButton;
