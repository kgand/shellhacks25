// src/screens/ProfileScreen.js
import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Switch, TouchableOpacity } from 'react-native';
import { Avatar, TextInput } from 'react-native-paper';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { theme } from '../utils/theme';
import { Screen, Text } from '../ui/overrides/base';

const ProfileScreen = () => {
  const { user, logout } = useAuth();
  const [firstName, setFirstName] = useState(user?.firstName || '');
  const [lastName, setLastName] = useState(user?.lastName || '');
  const [email, setEmail] = useState(user?.email || '');
  const [phone, setPhone] = useState(user?.phone || '');
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [notifications, setNotifications] = useState({
    allNotifications: true,
    safeZoneAlerts: true,
    medicationReminders: true,
    systemAlerts: true,
  });

  useEffect(() => {
    if (user) {
      setFirstName(user.firstName || '');
      setLastName(user.lastName || '');
      setEmail(user.email || '');
      setPhone(user.phone || '');
    }
  }, [user]);

  const handleSaveProfile = async () => {
    setIsSaving(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const toggleNotification = (key) => {
    setNotifications(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleLogout = async () => {
    logout();
  };

  const getInitials = () => {
    if (!user) return '?';
    return `${(user.firstName || '?').charAt(0)}${(user.lastName || '').charAt(0)}`;
  };
  
  return (
    <Screen scrollable>
      {/* Subtitle */}
      <View style={styles.subtitleContainer}>
        <Text size="md" color="textSecondary" style={styles.subtitle}>
          Your personal space
        </Text>
      </View>

      {/* Profile Card */}
      <View style={styles.profileCard}>
        <Avatar.Text
          size={72}
          label={getInitials()}
          backgroundColor={theme.colors.surfaceAlt}
          labelStyle={{ color: theme.colors.textPrimary, fontSize: 28 }}
        />
        <Text size="xl" weight="bold" color="textPrimary" style={styles.userName}>
          {`${firstName} ${lastName}`}
        </Text>
        <Text size="md" color="textSecondary" style={styles.userEmail}>
          {email}
        </Text>
        <Text size="sm" color="textSecondary" style={styles.userRole}>
          Patient • Memory Care
        </Text>
      </View>
      
      {/* Profile Information */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            My Information
          </Text>
        </View>
        
        {isEditing ? (
          <View style={styles.editForm}>
            <TextInput
              label="First Name"
              value={firstName}
              onChangeText={setFirstName}
              style={styles.input}
              textColor={theme.colors.textPrimary}
              theme={{ colors: { primary: theme.colors.accent, text: theme.colors.textPrimary, placeholder: theme.colors.textSecondary } }}
              mode="flat"
              underlineColor="transparent"
              activeUnderlineColor={theme.colors.accent}
              placeholderTextColor={theme.colors.textSecondary}
            />
            
            <TextInput
              label="Last Name"
              value={lastName}
              onChangeText={setLastName}
              style={styles.input}
              textColor={theme.colors.textPrimary}
              theme={{ colors: { primary: theme.colors.accent, text: theme.colors.textPrimary, placeholder: theme.colors.textSecondary } }}
              mode="flat"
              underlineColor="transparent"
              activeUnderlineColor={theme.colors.accent}
              placeholderTextColor={theme.colors.textSecondary}
            />
            
            <TextInput
              label="Phone Number"
              value={phone}
              onChangeText={setPhone}
              keyboardType="phone-pad"
              style={styles.input}
              textColor={theme.colors.textPrimary}
              theme={{ colors: { primary: theme.colors.accent, text: theme.colors.textPrimary, placeholder: theme.colors.textSecondary } }}
              mode="flat"
              underlineColor="transparent"
              activeUnderlineColor={theme.colors.accent}
              placeholderTextColor={theme.colors.textSecondary}
            />
            
            <View style={styles.editButtons}>
              <TouchableOpacity
                style={[styles.pillButton, styles.cancelButton]}
                onPress={() => setIsEditing(false)}
                activeOpacity={0.8}
              >
                <Text size="md" weight="semibold" color="textPrimary">
                  Cancel
                </Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.pillButton, styles.saveButton, isSaving && styles.disabledButton]}
                onPress={handleSaveProfile}
                disabled={isSaving}
                activeOpacity={0.8}
              >
                <Text size="md" weight="semibold" color="textPrimary">
                  Save
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View>
            <View style={styles.listItem}>
              <Text size="sm" color="textSecondary" style={styles.listItemTitle}>First Name</Text>
              <Text size="md" color="textPrimary">{firstName || 'Not set'}</Text>
            </View>
            
            <View style={styles.listItem}>
              <Text size="sm" color="textSecondary" style={styles.listItemTitle}>Last Name</Text>
              <Text size="md" color="textPrimary">{lastName || 'Not set'}</Text>
            </View>
            
            <View style={styles.listItem}>
              <Text size="sm" color="textSecondary" style={styles.listItemTitle}>Email</Text>
              <Text size="md" color="textPrimary">{email || 'Not set'}</Text>
            </View>
            
            <View style={styles.listItem}>
              <Text size="sm" color="textSecondary" style={styles.listItemTitle}>Phone</Text>
              <Text size="md" color="textPrimary">{phone || 'Not set'}</Text>
            </View>
            
            <TouchableOpacity
              style={[styles.pillButton, styles.editProfileButton]}
              onPress={() => setIsEditing(true)}
              activeOpacity={0.8}
            >
              <Text size="md" weight="semibold" color="textPrimary">
                Edit My Info
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </View>
      
      {/* Notification Settings */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            Notifications
          </Text>
        </View>
        
        <View style={styles.listItem}>
          <View style={styles.notificationItem}>
            <Ionicons
              name="notifications-outline"
              size={24}
              color={theme.colors.textSecondary}
              style={styles.notificationIcon}
            />
            <Text size="md" color="textPrimary">All Notifications</Text>
          </View>
          <Switch
            value={notifications.allNotifications}
            onValueChange={() => toggleNotification('allNotifications')}
            trackColor={{ false: theme.colors.border, true: theme.colors.accent }}
            thumbColor={theme.colors.textPrimary}
          />
        </View>
        
        <View style={styles.listItem}>
          <View style={styles.notificationItem}>
            <Ionicons
              name="shield-checkmark-outline"
              size={24}
              color={theme.colors.textSecondary}
              style={styles.notificationIcon}
            />
            <View>
              <Text size="md" color="textPrimary">Safe Zone Alerts</Text>
              <Text size="sm" color="textSecondary">When I enter/leave safe places</Text>
            </View>
          </View>
          <Switch
            value={notifications.safeZoneAlerts}
            onValueChange={() => toggleNotification('safeZoneAlerts')}
            trackColor={{ false: theme.colors.border, true: theme.colors.accent }}
            thumbColor={theme.colors.textPrimary}
          />
        </View>
        
        <View style={styles.listItem}>
          <View style={styles.notificationItem}>
            <Ionicons
              name="medical-outline"
              size={24}
              color={theme.colors.textSecondary}
              style={styles.notificationIcon}
            />
            <View>
              <Text size="md" color="textPrimary">Medication Reminders</Text>
              <Text size="sm" color="textSecondary">Take medicine on time</Text>
            </View>
          </View>
          <Switch
            value={notifications.medicationReminders}
            onValueChange={() => toggleNotification('medicationReminders')}
            trackColor={{ false: theme.colors.border, true: theme.colors.accent }}
            thumbColor={theme.colors.textPrimary}
          />
        </View>
      </View>
      
      {/* About Section */}
      <View style={styles.sectionCard}>
        <View style={styles.sectionHeader}>
          <Text size="lg" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
            About
          </Text>
        </View>
        
        <View style={styles.listItem}>
          <Text size="md" color="textPrimary">App Version</Text>
          <Text size="md" color="textSecondary">Memoray v1.0.0</Text>
        </View>
        
        <TouchableOpacity style={styles.listItem}>
          <Text size="md" color="textPrimary">Help & Support</Text>
          <Ionicons
            name="chevron-forward"
            size={20}
            color={theme.colors.textSecondary}
          />
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.listItem}>
          <Text size="md" color="textPrimary">Privacy Policy</Text>
          <Ionicons
            name="chevron-forward"
            size={20}
            color={theme.colors.textSecondary}
          />
        </TouchableOpacity>
      </View>
        
      <TouchableOpacity
        style={[styles.pillButton, styles.logoutButton]}
        onPress={handleLogout}
        activeOpacity={0.8}
      >
        <Text size="md" weight="semibold" color="textPrimary">
          Sign Out
        </Text>
      </TouchableOpacity>
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
  profileCard: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
    alignItems: 'center',
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
  },
  userName: {
    marginTop: theme.spacing.lg,
    marginBottom: theme.spacing.xs,
  },
  userEmail: {
    marginBottom: theme.spacing.sm,
  },
  userRole: {
    textAlign: 'center',
  },
  sectionCard: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
  },
  sectionHeader: {
    marginBottom: theme.spacing.lg,
  },
  sectionTitle: {
    // default from Text component
  },
  editForm: {
    marginTop: theme.spacing.md,
  },
  input: {
    marginBottom: theme.spacing.lg,
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.lg,
    borderTopLeftRadius: theme.radii.lg,
    borderTopRightRadius: theme.radii.lg,
    borderColor: theme.colors.inputBorder,
    borderWidth: 1,
    paddingHorizontal: theme.spacing.md,
  },
  editButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: theme.spacing.md,
  },
  pillButton: {
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    alignItems: 'center',
    flex: 1,
    minHeight: 48,
  },
  cancelButton: {
    backgroundColor: theme.colors.surfaceAlt,
    marginRight: theme.spacing.md,
  },
  saveButton: {
    backgroundColor: theme.colors.accent,
    marginLeft: theme.spacing.md,
  },
  disabledButton: {
    opacity: 0.6,
  },
  editProfileButton: {
    backgroundColor: theme.colors.surfaceAlt,
    marginTop: theme.spacing.lg,
  },
  listItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
    minHeight: 56,
  },
  listItemTitle: {
    // default from Text component
  },
  notificationItem: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  notificationIcon: {
    marginRight: theme.spacing.md,
  },
  logoutButton: {
    backgroundColor: theme.colors.surfaceAlt,
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing['3xl'],
  },
});

export default ProfileScreen;