// src/components/dashboard/reminders/ReminderItem.tsx
import React, { useState } from 'react';
import { View, StyleSheet, Alert, TouchableOpacity, Pressable, Platform } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../../ui/overrides/base';
import type { Reminder } from '../../../state/reminders/types';

interface ReminderItemProps {
  reminder: Reminder;
  onPress?: () => void;
  onEdit?: (reminder: Reminder) => void;
  onDelete?: (id: string) => void;
}

const ReminderItem: React.FC<ReminderItemProps> = ({ reminder, onPress, onEdit, onDelete }) => {
  const [dragOffset, setDragOffset] = useState(0);
  const [showDelete, setShowDelete] = useState(false);
  const [showMenu, setShowMenu] = useState(false);

  // --- Helpers -------------------------------------------------------------
  const confirmDelete = () => {
    if (Platform.OS === 'web') {
      // RN web Alert with multiple buttons doesn't execute callbacks.
      const ok = (globalThis as any).confirm?.('Delete reminder? This cannot be undone.') ?? true;
      if (ok && onDelete) onDelete(reminder.id);
      return;
    }
    Alert.alert(
      'Delete reminder?',
      'This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Delete', style: 'destructive', onPress: () => onDelete?.(reminder.id) },
      ]
    );
  };

  const handleDeletePress = () => {
    setShowMenu(false);
    confirmDelete();
  };

  const handleLongPress = () => {
    if (Platform.OS === 'web') {
      // Use a simple confirm on web; long-press isn’t natural there.
      confirmDelete();
      return;
    }
    Alert.alert(
      'Reminder Options',
      'What would you like to do?',
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Edit', onPress: () => onEdit?.(reminder) },
        { text: 'Delete', style: 'destructive', onPress: () => onDelete?.(reminder.id) },
      ]
    );
  };

  const getScheduleText = () => {
    if (reminder.scheduleType === 'time' && reminder.time) return reminder.time;
    if (reminder.scheduleType === 'interval' && reminder.intervalMinutes) return `Every ${reminder.intervalMinutes} minutes`;
    return '';
  };

  // --- UI ------------------------------------------------------------------
  return (
    <View style={styles.container}>
      {showDelete && (
        <View style={styles.deleteBackground}>
          <Ionicons name="trash" size={24} color="#fff" />
        </View>
      )}

      <TouchableOpacity
        style={[styles.reminderCard, { transform: [{ translateX: dragOffset }] }]}
        onLongPress={handleLongPress}
        delayLongPress={500}
        activeOpacity={0.85}
        onPress={onPress}
      >
        <View style={styles.reminderContent}>
          <Text style={styles.emoji}>{reminder.icon || '💊'}</Text>
          <View style={styles.reminderText}>
            <Text size="lg" weight="semibold" color="textPrimary">
              {reminder.label}
            </Text>
            <Text size="sm" color="textSecondary">{getScheduleText()}</Text>
            {!!reminder.notes && (
              <Text size="xs" color="textSecondary" style={styles.notes}>{reminder.notes}</Text>
            )}
          </View>
        </View>

        <View style={styles.actions}>
                  <Pressable
                    style={styles.deleteButton}
                    onPress={(e) => { e?.stopPropagation?.(); handleDeletePress(); }}
                    hitSlop={10}
                    accessibilityLabel="Delete reminder"
                    accessibilityRole="button"
                    accessibilityHint="Double tap to delete this reminder"
                  >
            <Ionicons name="trash-outline" size={20} color={theme.colors.error || '#e45858'} />
          </Pressable>

          <View style={styles.menuContainer}>
                    <TouchableOpacity
                      style={styles.moreButton}
                      onPress={(e) => { e?.stopPropagation?.(); setShowMenu(v => !v); }}
                      accessibilityLabel="More options"
                      accessibilityRole="button"
                      accessibilityHint="Double tap to open more options"
                    >
              <Ionicons name="ellipsis-vertical" size={20} color={theme.colors.textSecondary} />
            </TouchableOpacity>

            {showMenu && (
              <View style={styles.menu}>
                {onEdit && (
                  <TouchableOpacity style={styles.menuItem} onPress={() => onEdit(reminder)}>
                    <Ionicons name="create-outline" size={16} color={theme.colors.textPrimary || '#FFF'} />
                    <Text size="sm" color="textPrimary" style={styles.menuText}>Edit</Text>
                  </TouchableOpacity>
                )}
                {onDelete && (
                  <TouchableOpacity style={styles.menuItem} onPress={confirmDelete}>
                    <Ionicons name="trash-outline" size={16} color={theme.colors.error || '#FF4444'} />
                    <Text size="sm" color="error" style={styles.menuText}>Delete</Text>
                  </TouchableOpacity>
                )}
              </View>
            )}
          </View>

          <Ionicons name="chevron-forward" size={20} color={theme.colors.textSecondary || '#A7AFB8'} />
        </View>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { position: 'relative', marginBottom: theme.spacing.md },
  deleteBackground: {
    position: 'absolute', right: 0, top: 0, bottom: 0, width: 96,
    backgroundColor: theme.colors.error || '#FF4444',
    borderRadius: theme.radii.lg, alignItems: 'center', justifyContent: 'center', zIndex: 1,
  },
  reminderCard: {
    flexDirection: 'row', 
    alignItems: 'center',
    backgroundColor: theme.colors.surface, 
    borderColor: theme.colors.border, 
    borderWidth: 1,
    borderRadius: theme.radii.lg, 
    padding: theme.spacing.md, 
    zIndex: 2,
    minHeight: 64,
  },
  reminderContent: { flexDirection: 'row', alignItems: 'center', flex: 1 },
  emoji: { 
    fontSize: 22, 
    lineHeight: 26,
    marginRight: theme.spacing.md,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  reminderText: { flex: 1 },
  actions: { flexDirection: 'row', alignItems: 'center' },
  deleteButton: { marginRight: theme.spacing.sm || 8, padding: theme.spacing.xs || 4 },
  moreButton: { marginRight: theme.spacing.sm || 8, padding: theme.spacing.xs || 4 },
  menuContainer: { position: 'relative' },
  menu: {
    position: 'absolute', top: 40, right: 0,
    backgroundColor: theme.colors.surface || '#1A1D1F',
    borderRadius: theme.radii.lg || 16, borderWidth: 1, borderColor: theme.colors.border || '#2C3136',
    paddingVertical: theme.spacing.xs || 4, minWidth: 120, zIndex: 10,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.25, shadowRadius: 4, elevation: 5,
  },
  menuItem: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: theme.spacing.md || 12, paddingVertical: theme.spacing.sm || 8, gap: theme.spacing.sm || 8 },
  menuText: {},
  notes: { marginTop: theme.spacing.xs || 4, fontStyle: 'italic' },
});

export default ReminderItem;
