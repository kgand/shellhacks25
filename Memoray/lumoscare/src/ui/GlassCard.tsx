// src/ui/GlassCard.tsx

import React from 'react';
import { View, StyleSheet, ViewStyle, Pressable } from 'react-native';
import { BlurView } from 'expo-blur';

interface GlassCardProps {
  children: React.ReactNode;
  onPress?: () => void;
  variant?: 'default' | 'elevated';
  padding?: 'sm' | 'md' | 'lg';
  style?: ViewStyle;
}

const GlassCard: React.FC<GlassCardProps> = ({
  children,
  onPress,
  variant = 'default',
  padding = 'md',
  style,
}) => {
  const getCardStyle = (): ViewStyle => {
    const baseStyle: ViewStyle = {
      borderRadius: 16,
      overflow: 'hidden',
      borderWidth: 1,
      borderColor: 'rgba(255, 255, 255, 0.12)',
    };

    const variantStyles = {
      default: {
        backgroundColor: 'rgba(255, 255, 255, 0.08)',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 8,
        elevation: 3,
      },
      elevated: {
        backgroundColor: 'rgba(255, 255, 255, 0.16)',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 12,
        elevation: 5,
      },
    };

    const paddingStyles = {
      sm: { padding: 12 },
      md: { padding: 16 },
      lg: { padding: 20 },
    };

    return {
      ...baseStyle,
      ...variantStyles[variant],
      ...paddingStyles[padding],
    };
  };

  const CardContent = () => (
    <BlurView
      intensity={20}
      tint="dark"
      style={getCardStyle()}
    >
      {children}
    </BlurView>
  );

  if (onPress) {
    return (
      <Pressable
        onPress={onPress}
        style={style}
        hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
      >
        <CardContent />
      </Pressable>
    );
  }

  return (
    <View style={style}>
      <CardContent />
    </View>
  );
};

export default GlassCard;
