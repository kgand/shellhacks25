// src/components/dashboard/reminders/DailyReminders.tsx
import React, { useState } from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../../ui/overrides/base';
import { useReminders } from '../../../state/reminders';
import ReminderItem from './ReminderItem';
import AddEditReminderDialog from './AddEditReminderDialog';

const DailyReminders: React.FC = () => {
  const { items, addReminder, updateReminder, removeReminder } = useReminders();
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [editingReminder, setEditingReminder] = useState<any>(null);
  
  // Filter reminders for patient audience
  const patientReminders = items.filter(reminder => reminder.audience === 'patient');

  const handleSaveReminder = async (reminderData: any) => {
    try {
      if (editingReminder) {
        await updateReminder(editingReminder.id, reminderData);
        setEditingReminder(null);
      } else {
        await addReminder(reminderData);
      }
    } catch (error) {
      console.error('Error saving reminder:', error);
    }
  };

  const handleEditReminder = (reminder: any) => {
    setEditingReminder(reminder);
    setShowAddDialog(true);
  };


  const handleReminderPress = (reminder: any) => {
    console.log('Reminder tapped', reminder.label);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text size="xl" weight="bold" color="textPrimary" style={styles.title}>
          Daily Reminders
        </Text>
        <TouchableOpacity 
          style={styles.addButton}
          onPress={() => setShowAddDialog(true)}
        >
          <Ionicons name="add" size={20} color={theme.colors.textPrimary} />
          <Text size="sm" weight="semibold" color="textPrimary" style={styles.addButtonText}>
            Add Reminder
          </Text>
        </TouchableOpacity>
      </View>

      {patientReminders.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons 
            name="alarm-outline" 
            size={48} 
            color={theme.colors.textSecondary} 
            style={styles.emptyIcon}
          />
          <Text size="md" color="textSecondary" style={styles.emptyTitle}>
            No reminders yet
          </Text>
          <Text size="sm" color="textSecondary" style={styles.emptySubtitle}>
            Add your first reminder to get started
          </Text>
          <TouchableOpacity 
            style={styles.emptyButton}
            onPress={() => setShowAddDialog(true)}
          >
            <Text size="sm" weight="semibold" color="textPrimary">
              Add your first reminder
            </Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.remindersList}>
          {patientReminders.map((reminder) => (
            <ReminderItem
              key={reminder.id}
              reminder={reminder}
              onPress={() => handleReminderPress(reminder)}
              onEdit={handleEditReminder}
              onDelete={removeReminder}
            />
          ))}
        </View>
      )}

      <AddEditReminderDialog
        visible={showAddDialog}
        onClose={() => {
          setShowAddDialog(false);
          setEditingReminder(null);
        }}
        onSave={handleSaveReminder}
        editingReminder={editingReminder}
        audience="patient"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  title: {
    // default from Text component
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    gap: theme.spacing.xs,
    minHeight: 40,
  },
  addButtonText: {
    // default from Text component
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: theme.spacing['2xl'],
    paddingHorizontal: theme.spacing.lg,
  },
  emptyIcon: {
    marginBottom: theme.spacing.lg,
  },
  emptyTitle: {
    marginBottom: theme.spacing.sm,
    textAlign: 'center',
  },
  emptySubtitle: {
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  emptyButton: {
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    minHeight: 48,
  },
  remindersList: {
    // Container for reminder items
  },
});

export default DailyReminders;
