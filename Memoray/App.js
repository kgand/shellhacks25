// App.js
import React, { useState, useEffect } from 'react';
import './src/ui/overrides/textColor';
import { View, StatusBar } from 'react-native';
import {
  useFonts,
  Inter_400Regular,
  Inter_600SemiBold,
  Inter_700Bold,
} from '@expo-google-fonts/inter';
import { theme } from './src/utils/theme';

import AppProviders from './src/context/AppProviders';
import AppNavigator from './src/navigation/AppNavigator';
import SplashScreen from './src/ui/components/SplashScreen';
import ErrorBoundary from './src/debug/ErrorBoundary';

export default function App() {
  const [fontsLoaded] = useFonts({
    'Inter-Regular': Inter_400Regular,
    'Inter-SemiBold': Inter_600SemiBold,
    'Inter-Bold': Inter_700Bold,
  });

  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    if (fontsLoaded) {
      const timer = setTimeout(() => setShowSplash(false), 900);
      return () => clearTimeout(timer);
    }
  }, [fontsLoaded]);

  if (!fontsLoaded || showSplash) {
    return <SplashScreen />;
  }

  return (
    <View style={{ flex: 1, backgroundColor: theme.colors.background }}>
      <StatusBar barStyle="light-content" backgroundColor={theme.colors.background} />
      <ErrorBoundary>
        <AppProviders>
          <AppNavigator />
        </AppProviders>
      </ErrorBoundary>
    </View>
  );
}
