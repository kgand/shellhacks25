// src/ui/components/DarkCard.js
import React from 'react';
import { View, StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

const DarkCard = ({ children, style, ...props }) => {
  return (
    <View style={[styles.container, style]} {...props}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.radii.card,
    borderWidth: 1,
    borderColor: theme.colors.border,
    padding: theme.spacing.lg,
    ...theme.shadows.subtle,
  },
});

export default DarkCard;
