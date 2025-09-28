// src/ui/overrides/base.tsx
import React from 'react';
import {
  View,
  Text as RNText,
  StyleSheet,
  ScrollView,
  ViewStyle,
  TextStyle,
  TextProps as RNTextProps,
} from 'react-native';
import { SafeAreaView, SafeAreaViewProps } from 'react-native-safe-area-context';
import { theme } from '../../utils/theme';

// Keys your theme uses
type SizeKey = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
type WeightKey = 'regular' | 'semibold' | 'bold';
type ColorKey = keyof typeof theme.colors;

// Props
type ScreenProps = SafeAreaViewProps & {
  children?: React.ReactNode;
  style?: ViewStyle | ViewStyle[];
  scrollable?: boolean;
};

type TextProps = Omit<RNTextProps, 'style'> & {
  children?: React.ReactNode;
  style?: TextStyle | TextStyle[];
  size?: SizeKey;
  weight?: WeightKey;
  color?: ColorKey;
};

// Screen wrapper component
export const Screen: React.FC<ScreenProps> = ({
  children,
  style,
  scrollable = false,
  ...props
}) => {
  const Container: any = scrollable ? ScrollView : View;

  return (
    <SafeAreaView style={[styles.screen, style]} {...props}>
      <Container
        style={styles.container}
        showsVerticalScrollIndicator={false}
        {...(scrollable ? { contentContainerStyle: styles.scrollContent } : {})}
      >
        {children}
      </Container>
    </SafeAreaView>
  );
};

// Text wrapper component with default styling
export const Text: React.FC<TextProps> = ({
  children,
  style,
  size = 'md',
  weight = 'regular',
  color = 'textPrimary',
  ...props
}) => {
  // Loosely read from theme, but keep TS happy
  const sizes =
    (((theme as any).fonts?.sizes ?? {}) as Partial<Record<SizeKey, number>>);

  const weightStyle =
    (((theme as any).fonts?.[weight] ?? {}) as TextStyle);

  const fontSize = sizes[size] ?? 15;
  const resolvedColor =
    ((theme.colors as any)[color] ?? theme.colors.textPrimary ?? '#FFFFFF') as string;

  const textStyle: (TextStyle | undefined)[] = [
    styles.text,
    {
      fontSize,
      lineHeight: Math.round(fontSize * 1.25),
      color: resolvedColor,
    },
    weightStyle, // spread equivalent, but typed
    style as any,
  ];

  return (
    <RNText style={textStyle} {...props}>
      {children}
    </RNText>
  );
};

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  container: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
  },
  text: {
    color: theme.colors.textPrimary,
  },
});
