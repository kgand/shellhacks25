// src/navigation/MainTabNavigator.js
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import DashboardScreen from '../screens/DashboardScreen';
import CareHubScreen from '../screens/CareHubScreen';
import SafeZonesScreen from '../screens/SafeZonesScreen';
import ProfileScreen from '../screens/ProfileScreen';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../utils/theme';

const Tab = createBottomTabNavigator();

// Safe helpers in case theme tokens are missing
const sizes = (theme?.fonts?.sizes) || { xs: 12, sm: 13, md: 15, lg: 17, xl: 20, '2xl': 24, '3xl': 28 };
const headerFontSize = sizes.xl || 20;
const labelFontSize  = sizes.xs || 12;

export default function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        headerStyle: {
          backgroundColor: theme.colors?.headerBg ?? theme.colors?.surface ?? '#1A1D1F',
          borderBottomColor: theme.colors?.border ?? '#2C3136',
          borderBottomWidth: 1,
        },
        headerTitleStyle: {
          color: theme.colors?.headerText ?? theme.colors?.textPrimary ?? '#FFFFFF',
          fontSize: headerFontSize,
          // Use Inter family instead of relying on numeric weights from theme
          fontFamily: 'Inter-SemiBold',
        },
        headerTintColor: theme.colors?.headerText ?? theme.colors?.textPrimary ?? '#FFFFFF',

        tabBarStyle: {
          backgroundColor: theme.colors?.navBg ?? theme.colors?.surface ?? '#1A1D1F',
          borderTopColor: theme.colors?.border ?? '#2C3136',
          borderTopWidth: 1,
          height: 60,
          paddingBottom: 8,
          paddingTop: 8,
        },
        tabBarActiveTintColor: theme.colors?.navActive ?? theme.colors?.textPrimary ?? '#FFFFFF',
        tabBarInactiveTintColor: theme.colors?.navInactive ?? theme.colors?.tabInactive ?? '#7C838C',
        tabBarLabelStyle: {
          fontSize: labelFontSize,
          marginBottom: 4,
          fontFamily: 'Inter-Regular',
        },

        // Correct prop for bottom tabs (contentStyle is for stacks)
        sceneContainerStyle: {
          backgroundColor: theme.colors?.background ?? '#111315',
        },

        tabBarIcon: ({ color, size }) => {
          const icons = {
            Dashboard: 'home-outline',
            'Care Hub': 'people-outline',
            'Safe Zones': 'shield-checkmark-outline',
            Profile: 'person-outline',
          };
          const name = icons[route.name] || 'ellipse-outline';
          return <Ionicons name={name} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Care Hub" component={CareHubScreen} />
      <Tab.Screen name="Safe Zones" component={SafeZonesScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
