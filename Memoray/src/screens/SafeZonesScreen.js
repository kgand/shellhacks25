// src/screens/SafeZonesScreen.js
import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../utils/theme';
import { Screen, Text } from '../ui/overrides/base';

const SafeZonesScreen = () => {
  const [safeZones] = useState([
    { icon: 'home-outline', label: 'Home', status: 'Active', radius: '100m' },
    { icon: 'leaf-outline', label: 'Park', status: 'Active', radius: '200m' },
    { icon: 'cafe-outline', label: 'Café', status: 'Inactive', radius: '50m' },
    { icon: 'medical-outline', label: 'Hospital', status: 'Active', radius: '150m' },
    { icon: 'storefront-outline', label: 'Grocery Store', status: 'Inactive', radius: '75m' },
  ]);

  return (
    <Screen scrollable>
      {/* Subtitle */}
      <View style={styles.subtitleContainer}>
        <Text size="md" color="textSecondary" style={styles.subtitle}>
          Your safe places with friendly reminders
        </Text>
      </View>

      {/* Safe Zones List */}
      <View style={styles.section}>
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
                <Text size="lg" weight="semibold" color="textPrimary" style={styles.zoneLabel}>
                  {zone.label}
                </Text>
                <Text size="sm" color="textSecondary" style={styles.zoneRadius}>
                  Radius: {zone.radius}
                </Text>
                <View style={styles.statusContainer}>
                  <Ionicons
                    name={zone.status === 'Active' ? 'checkmark-circle-outline' : 'pause-circle-outline'}
                    size={16}
                    color={theme.colors.textSecondary}
                    style={styles.statusIcon}
                  />
                  <Text size="sm" color="textSecondary" style={styles.zoneStatus}>
                    {zone.status}
                  </Text>
                </View>
              </View>
            </View>
            <Ionicons
              name="chevron-forward"
              size={20}
              color={theme.colors.textSecondary}
            />
          </TouchableOpacity>
        ))}
      </View>

      {/* Add New Zone Button */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.addZoneButton}>
          <Ionicons
            name="add-outline"
            size={24}
            color={theme.colors.textSecondary}
            style={styles.addIcon}
          />
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.addZoneText}>
            Add New Safe Zone
          </Text>
          <Text size="sm" color="textSecondary" style={styles.addZoneSubtext}>
            Tap to create a new safe place
          </Text>
        </TouchableOpacity>
      </View>

      {/* Help Section */}
      <View style={styles.section}>
        <View style={styles.helpCard}>
          <Ionicons
            name="bulb-outline"
            size={24}
            color={theme.colors.textSecondary}
            style={styles.helpIcon}
          />
          <View style={styles.helpText}>
            <Text size="md" weight="semibold" color="textPrimary" style={styles.helpTitle}>
              How Safe Zones Work
            </Text>
            <Text size="sm" color="textSecondary" style={styles.helpDescription}>
              When you enter or leave a safe zone, your caregivers will get a friendly notification. 
              This helps everyone stay connected and safe!
            </Text>
          </View>
        </View>
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
  zoneLabel: {
    marginBottom: theme.spacing.xs,
  },
  zoneRadius: {
    marginBottom: theme.spacing.sm,
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusIcon: {
    marginRight: theme.spacing.xs,
  },
  zoneStatus: {
    // default from Text component
  },
  addZoneButton: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    alignItems: 'center',
    borderStyle: 'dashed',
    minHeight: 80,
  },
  addIcon: {
    marginBottom: theme.spacing.md,
  },
  addZoneText: {
    marginBottom: theme.spacing.xs,
  },
  addZoneSubtext: {
    textAlign: 'center',
  },
  helpCard: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    flexDirection: 'row',
    alignItems: 'flex-start',
    minHeight: 80,
  },
  helpIcon: {
    marginRight: theme.spacing.md,
  },
  helpText: {
    flex: 1,
  },
  helpTitle: {
    marginBottom: theme.spacing.sm,
  },
  helpDescription: {
    lineHeight: 20,
  },
});

export default SafeZonesScreen;