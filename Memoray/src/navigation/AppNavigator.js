// src/navigation/AppNavigator.js
import React from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { theme } from '../utils/theme';

import MainTabNavigator from './MainTabNavigator';
import LandingScreen from '../screens/LandingScreen';
import OnboardingScreen from '../screens/OnboardingScreen';
import PeopleScreen from '../screens/PeopleScreen';
import FoodGalleryScreen from '../screens/FoodGalleryScreen';
import CarGalleryScreen from '../screens/CarGalleryScreen';
import HomeGalleryScreen from '../screens/HomeGalleryScreen';
import LandmarksGalleryScreen from '../screens/LandmarksGalleryScreen';
import PhotosGalleryScreen from '../screens/PhotosGalleryScreen';
import MemoryGameScreen from '../screens/MemoryGameScreen';

const Stack = createNativeStackNavigator();

const navTheme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    background: theme.colors.background,
    card: theme.colors.card,
    text: theme.colors.textPrimary,
    border: theme.colors.border,
    primary: theme.colors.primary,
  },
};

export default function AppNavigator() {
  return (
    <NavigationContainer theme={navTheme}>
      <Stack.Navigator
        initialRouteName="Onboarding"
        screenOptions={{
          headerShown: false,
          animation: 'fade',
        }}
      >
        <Stack.Screen name="Landing" component={LandingScreen} />
        <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        <Stack.Screen name="MainTabs" component={MainTabNavigator} />
        <Stack.Screen name="PeopleScreen" component={PeopleScreen} />
        <Stack.Screen name="FoodGalleryScreen" component={FoodGalleryScreen} />
        <Stack.Screen name="CarGalleryScreen" component={CarGalleryScreen} />
        <Stack.Screen name="HomeGalleryScreen" component={HomeGalleryScreen} />
        <Stack.Screen name="LandmarksGalleryScreen" component={LandmarksGalleryScreen} />
        <Stack.Screen name="PhotosGalleryScreen" component={PhotosGalleryScreen} />
        <Stack.Screen name="MemoryGameScreen" component={MemoryGameScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
