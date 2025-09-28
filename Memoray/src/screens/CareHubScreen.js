// src/screens/CareHubScreen.js
import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity, Switch } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../utils/theme';
import { Screen, Text } from '../ui/overrides/base';

const CareHubScreen = () => {
  const [locationSharing, setLocationSharing] = useState(true);

  const dailyReminders = [
    { icon: 'medical-outline', label: 'Take your medicine', time: '8:00 AM' },
    { icon: 'water-outline', label: 'Drink water', time: 'Every 2 hours' },
    { icon: 'call-outline', label: 'Call family', time: '7:00 PM' },
    { icon: 'walk-outline', label: 'Go for a walk', time: '3:00 PM' },
    { icon: 'restaurant-outline', label: 'Eat lunch at 12', time: '12:00 PM' },
  ];

  const safeZones = [
    { icon: 'home-outline', label: 'Home', status: 'Active' },
    { icon: 'leaf-outline', label: 'Park', status: 'Active' },
    { icon: 'cafe-outline', label: 'Café', status: 'Inactive' },
  ];

  return (
    <Screen scrollable>
      {/* Subtitle */}
      <View style={styles.subtitleContainer}>
        <Text size="md" color="textSecondary" style={styles.subtitle}>
          Caregiver Dashboard
        </Text>
      </View>

      {/* Location Sharing Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            Share Location
          </Text>
        </View>
        
        <View style={styles.locationCard}>
          <View style={styles.locationContent}>
            <Ionicons
              name="location-outline"
              size={24}
              color={theme.colors.textSecondary}
              style={styles.locationIcon}
            />
            <View style={styles.locationText}>
              <Text size="md" weight="semibold" color="textPrimary">
                Allow caregiver to see your location.
              </Text>
              <Text size="sm" color="textSecondary">
                Current Place: Home
              </Text>
            </View>
          </View>
          <Switch
            value={locationSharing}
            onValueChange={setLocationSharing}
            trackColor={{ false: theme.colors.border, true: theme.colors.accent }}
            thumbColor={theme.colors.textPrimary}
          />
        </View>
      </View>

      {/* Daily Reminders Management */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            Daily Reminders
          </Text>
        </View>
        
        {dailyReminders.map((reminder, index) => (
          <View key={index} style={styles.reminderCard}>
            <View style={styles.reminderContent}>
              <Ionicons
                name={reminder.icon}
                size={24}
                color={theme.colors.textSecondary}
                style={styles.reminderIcon}
              />
              <View style={styles.reminderText}>
                <Text size="md" weight="semibold" color="textPrimary">
                  {reminder.label}
                </Text>
                <Text size="sm" color="textSecondary">
                  {reminder.time}
                </Text>
              </View>
            </View>
            <TouchableOpacity style={styles.editButton}>
              <Ionicons
                name="create-outline"
                size={20}
                color={theme.colors.textSecondary}
              />
            </TouchableOpacity>
          </View>
        ))}
        
        <TouchableOpacity style={styles.addReminderButton}>
          <Ionicons
            name="add-outline"
            size={24}
            color={theme.colors.textSecondary}
            style={styles.addIcon}
          />
          <Text size="md" weight="semibold" color="textPrimary">
            Add New Reminder
          </Text>
        </TouchableOpacity>
      </View>

      {/* Safe Zones Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            Safe Zones
          </Text>
        </View>
        
        {safeZones.map((zone, index) => (
          <TouchableOpacity
            key={index}
            style={styles.zoneCard}
            onPress={() => console.log('Edit zone', zone.label)}
          >
            <View style={styles.zoneContent}>
              <Ionicons
                name={zone.icon}
                size={24}
                color={theme.colors.textSecondary}
                style={styles.zoneIcon}
              />
              <View style={styles.zoneText}>
                <Text size="md" weight="semibold" color="textPrimary">
                  {zone.label}
                </Text>
                <Text size="sm" color="textSecondary">
                  Status: {zone.status}
                </Text>
              </View>
            </View>
            <Ionicons
              name="chevron-forward"
              size={20}
              color={theme.colors.textSecondary}
            />
          </TouchableOpacity>
        ))}
        
        <TouchableOpacity style={styles.addZoneButton}>
          <Ionicons
            name="add-outline"
            size={24}
            color={theme.colors.textSecondary}
            style={styles.addIcon}
          />
          <Text size="md" weight="semibold" color="textPrimary">
            Add New Safe Zone
          </Text>
        </TouchableOpacity>
      </View>
    </Screen>
  );
};

const styles = StyleSheet.create({
  subtitleContainer: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.lg,
    marginTop: theme.spacing.sm,
  },
  subtitle: {
    textAlign: 'center',
  },
  section: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
  },
  sectionHeader: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    // default from Text component
  },
  locationCard: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 64,
  },
  locationContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  locationIcon: {
    marginRight: theme.spacing.md,
  },
  locationText: {
    flex: 1,
  },
  reminderCard: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 64,
  },
  reminderContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  reminderIcon: {
    marginRight: theme.spacing.md,
  },
  reminderText: {
    flex: 1,
  },
  editButton: {
    padding: theme.spacing.sm,
    minWidth: 44,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addReminderButton: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderStyle: 'dashed',
    minHeight: 56,
  },
  zoneCard: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    minHeight: 64,
  },
  zoneContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  zoneIcon: {
    marginRight: theme.spacing.md,
  },
  zoneText: {
    flex: 1,
  },
  addZoneButton: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderStyle: 'dashed',
    minHeight: 56,
  },
  addIcon: {
    marginRight: theme.spacing.md,
  },
});

export default CareHubScreen;