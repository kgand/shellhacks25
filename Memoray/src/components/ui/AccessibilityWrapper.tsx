import React from 'react';
import { View, StyleSheet, TouchableOpacity, Pressable } from 'react-native';
import { theme } from '../../utils/theme';

interface AccessibilityWrapperProps {
  children: React.ReactNode;
  onPress?: () => void;
  accessibilityLabel: string;
  accessibilityHint?: string;
  accessibilityRole?: 'button' | 'link' | 'text' | 'image' | 'none';
  accessibilityState?: {
    disabled?: boolean;
    selected?: boolean;
    checked?: boolean | 'mixed';
    expanded?: boolean;
    busy?: boolean;
  };
  minTouchTarget?: boolean;
  style?: any;
}

const AccessibilityWrapper: React.FC<AccessibilityWrapperProps> = ({
  children,
  onPress,
  accessibilityLabel,
  accessibilityHint,
  accessibilityRole = 'button',
  accessibilityState,
  minTouchTarget = true,
  style,
}) => {
  const minSize = minTouchTarget ? 44 : undefined;

  const accessibilityProps = {
    accessibilityLabel,
    accessibilityHint,
    accessibilityRole,
    accessibilityState,
  };

  if (onPress) {
    const TouchableComponent = accessibilityRole === 'button' ? TouchableOpacity : Pressable;
    
    return (
      <TouchableComponent
        onPress={onPress}
        style={[
          styles.wrapper,
          minTouchTarget && styles.minTouchTarget,
          { minHeight: minSize, minWidth: minSize },
          style,
        ]}
        activeOpacity={0.8}
        {...accessibilityProps}
      >
        {children}
      </TouchableComponent>
    );
  }

  return (
    <View
      style={[
        styles.wrapper,
        minTouchTarget && styles.minTouchTarget,
        { minHeight: minSize, minWidth: minSize },
        style,
      ]}
      {...accessibilityProps}
    >
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  wrapper: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  minTouchTarget: {
    // Ensure minimum touch target size for accessibility
  },
});

export default AccessibilityWrapper;
