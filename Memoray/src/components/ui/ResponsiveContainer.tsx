import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { theme } from '../../utils/theme';

interface ResponsiveContainerProps {
  children: React.ReactNode;
  maxWidth?: number;
  padding?: 'sm' | 'md' | 'lg' | 'xl';
  style?: any;
}

const ResponsiveContainer: React.FC<ResponsiveContainerProps> = ({
  children,
  maxWidth = 1200,
  padding = 'md',
  style,
}) => {
  const { width } = Dimensions.get('window');
  const isTablet = width >= 768;
  const isDesktop = width >= 1024;

  const getPadding = () => {
    if (isDesktop) {
      switch (padding) {
        case 'sm': return theme.spacing.lg;
        case 'lg': return theme.spacing['3xl'];
        case 'xl': return theme.spacing['4xl'];
        default: return theme.spacing.xl;
      }
    } else if (isTablet) {
      switch (padding) {
        case 'sm': return theme.spacing.md;
        case 'lg': return theme.spacing.xl;
        case 'xl': return theme.spacing['2xl'];
        default: return theme.spacing.lg;
      }
    } else {
      switch (padding) {
        case 'sm': return theme.spacing.sm;
        case 'lg': return theme.spacing.lg;
        case 'xl': return theme.spacing.xl;
        default: return theme.spacing.md;
      }
    }
  };

  const containerStyles = [
    styles.container,
    {
      paddingHorizontal: getPadding(),
      maxWidth: isDesktop ? maxWidth : undefined,
    },
    style,
  ];

  return (
    <View style={containerStyles}>
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
    alignSelf: 'center',
  },
});

export default ResponsiveContainer;
