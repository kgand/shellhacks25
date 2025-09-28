// src/screens/DashboardScreen.js
import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../utils/theme';
import { Screen, Text } from '../ui/overrides/base';
import DailyReminders from '../components/dashboard/reminders/DailyReminders';
import ThingsIKnow from '../components/dashboard/ThingsIKnow';
import QuickActions from '../components/dashboard/QuickActions';
import SearchBar from '../components/search/SearchBar';
import QuickAddReminder from '../components/dashboard/reminders/QuickAddReminder';
import ResponsiveContainer from '../components/ui/ResponsiveContainer';
import Card from '../components/ui/Card';
import TestSuite from '../components/ui/TestSuite';

const DashboardScreen = ({ navigation }) => {
  const [showQuickAdd, setShowQuickAdd] = useState(false);
  const [showTestSuite, setShowTestSuite] = useState(false);

  const handleCareHubPress = () => {
    navigation.navigate('Care Hub');
  };


  return (
    <Screen scrollable>
      <ResponsiveContainer>
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <View>
              <Text size="3xl" weight="bold" color="textPrimary" style={styles.greeting}>
                Good morning
              </Text>
              <Text size="lg" color="textSecondary" style={styles.subtitle}>
                Here's what's happening today
              </Text>
            </View>
            <TouchableOpacity
              style={styles.testButton}
              onPress={() => setShowTestSuite(!showTestSuite)}
              accessibilityLabel="Toggle test suite"
              accessibilityHint="Double tap to show or hide the test suite"
            >
              <Ionicons name="flask" size={24} color={theme.colors.textSecondary} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Search Bar */}
        <SearchBar />

        {/* Quick Actions */}
        <QuickActions onQuickAddReminder={() => setShowQuickAdd(true)} />

        {/* Daily Reminders Section */}
        <DailyReminders />

        {/* Remember Me Section */}
        <View style={styles.rememberMeSection}>
          <View style={styles.sectionHeader}>
            <Text size="xl" weight="bold" color="textPrimary" style={styles.sectionTitle}>
              Remember Me
            </Text>
          </View>
          <Card variant="elevated" style={styles.gameCard}>
            <View style={styles.gameContent}>
              <View style={styles.gameText}>
                <Text size="lg" weight="bold" color="textPrimary" style={styles.gameTitle}>
                  Memory Game
                </Text>
                <Text size="md" color="textSecondary" style={styles.gameSubtitle}>
                  Match faces and answer questions
                </Text>
              </View>
              <TouchableOpacity 
                style={styles.playButton}
                onPress={() => navigation.navigate('MemoryGameScreen')}
                accessibilityLabel="Play Remember Me game"
                accessibilityRole="button"
              >
                <Text size="sm" weight="semibold" color="textPrimary">Play</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.gameIcon}>
              <Text style={styles.gameEmoji}>🎯</Text>
            </View>
          </Card>
        </View>

        {/* Things I Know Section */}
        <ThingsIKnow />

        {/* Test Suite */}
        {showTestSuite && <TestSuite />}

        {/* Quick Add Reminder Modal */}
        <QuickAddReminder
          visible={showQuickAdd}
          onClose={() => setShowQuickAdd(false)}
        />
      </ResponsiveContainer>
    </Screen>
  );
};

const styles = StyleSheet.create({
  header: {
    marginBottom: theme.spacing.xl,
    paddingTop: theme.spacing.lg,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  greeting: {
    marginBottom: theme.spacing.xs,
  },
  subtitle: {
    opacity: 0.8,
  },
  testButton: {
    padding: theme.spacing.sm,
    borderRadius: theme.radii.lg,
    backgroundColor: theme.colors.surfaceAlt,
  },
  rememberMeSection: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
  },
  sectionHeader: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    // default from Text component
  },
  gameCard: {
    backgroundColor: theme.colors.accent,
    minHeight: 120,
  },
  gameContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    flex: 1,
  },
  gameText: {
    flex: 1,
  },
  gameTitle: {
    marginBottom: theme.spacing.xs,
    color: theme.colors.textPrimary,
  },
  gameSubtitle: {
    opacity: 0.9,
    color: theme.colors.textPrimary,
  },
  playButton: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: theme.radii.lg,
    paddingVertical: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    marginLeft: theme.spacing.md,
  },
  gameIcon: {
    marginLeft: theme.spacing.lg,
  },
  gameEmoji: {
    fontSize: 32,
    lineHeight: 36,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
});

export default DashboardScreen;