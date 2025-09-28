// src/screens/LandingScreen.js
import React from 'react';
import { View, StatusBar } from 'react-native';
import { Screen, Text } from '../ui/overrides/base';
import { theme } from '../utils/theme';

export default function LandingScreen({ navigation }) {
  return (
    <Screen>
      <StatusBar barStyle="light-content" />
      <View style={styles.content}>
        <Text size="3xl" weight="bold" color="textPrimary" style={styles.title}>
          MetaSense
        </Text>
        <Text size="md" color="textSecondary" style={styles.subtitle}>
          Gentle memory cues. Private by default.
        </Text>
      </View>
    </Screen>
  );
}

const styles = {
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: theme.spacing['2xl'],
  },
  title: {
    marginBottom: theme.spacing.md,
    textAlign: 'center',
  },
  subtitle: {
    textAlign: 'center',
  },
};
