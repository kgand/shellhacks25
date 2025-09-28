// src/ui/components/Card.js
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

const Card = ({ children, style, ...props }) => {
  return (
    <View style={[styles.container, style]} {...props}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    ...theme.shadows.card,
  },
});

export default Card;
