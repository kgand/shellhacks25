// src/components/caregiver/CaregiverReminders.tsx
import React, { useState } from "react";
import { View, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { theme } from "../../utils/theme";
import { Text } from "../../ui/overrides/base";
import { useReminders } from "../../state/reminders";
import ReminderItem from "../dashboard/reminders/ReminderItem";
import AddEditReminderDialog from "../dashboard/reminders/AddEditReminderDialog";
import type { Reminder, ScheduleType, Audience } from "../../state/reminders/types";

const CaregiverReminders: React.FC = () => {
  const { items, addReminder, updateReminder, removeReminder } = useReminders();

  const [showAddDialog, setShowAddDialog] = useState(false);
  const [editingReminder, setEditingReminder] = useState<Reminder | null>(null);

  // Only caregiver reminders
  const caregiverReminders: Reminder[] = items.filter(
    (reminder: Reminder) => reminder.audience === "caregiver"
  );

  const handleSaveReminder = async (reminderData: Omit<Reminder, 'id'>) => {
    try {
      if (editingReminder) {
        await updateReminder(editingReminder.id, reminderData);
        setEditingReminder(null);
      } else {
        await addReminder(reminderData);
      }
    } catch (error) {
      console.error("Error saving reminder:", error);
    }
  };

  const handleEditReminder = (reminder: Reminder) => {
    setEditingReminder(reminder);
    setShowAddDialog(true);
  };

  const handleDeleteReminder = async (id: string) => {
    try {
      await removeReminder(id);
    } catch (error) {
      console.error("Error deleting reminder:", error);
    }
  };

  const handleReminderPress = (reminder: Reminder) => {
    console.log("Caregiver reminder tapped", reminder.label);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text size="xl" weight="bold" color="textPrimary" style={styles.title}>
          Caregiver Reminders
        </Text>
        <TouchableOpacity style={styles.addButton} onPress={() => setShowAddDialog(true)}>
          <Ionicons name="add" size={20} color={theme.colors.textPrimary} />
          <Text size="sm" weight="semibold" color="textPrimary" style={styles.addButtonText}>
            Add Reminder
          </Text>
        </TouchableOpacity>
      </View>

      {caregiverReminders.length === 0 ? (
        <View style={styles.emptyState}>
          <Ionicons
            name="alarm-outline"
            size={48}
            color={theme.colors.textSecondary}
            style={styles.emptyIcon}
          />
          <Text size="md" color="textSecondary" style={styles.emptyTitle}>
            No caregiver reminders yet
          </Text>
          <Text size="sm" color="textSecondary" style={styles.emptySubtitle}>
            Add reminders to help care for your loved one
          </Text>
          <TouchableOpacity style={styles.emptyButton} onPress={() => setShowAddDialog(true)}>
            <Text size="sm" weight="semibold" color="textPrimary">
              Add your first reminder
            </Text>
          </TouchableOpacity>
        </View>
      ) : (
        <View style={styles.remindersList}>
          {caregiverReminders.map((reminder: Reminder) => (
            <ReminderItem
              key={reminder.id}
              reminder={reminder}
              onPress={() => handleReminderPress(reminder)}
              onEdit={handleEditReminder}
              onDelete={handleDeleteReminder}
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
        editingReminder={editingReminder ?? undefined}
        audience="caregiver"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing["2xl"],
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: theme.spacing.lg,
  },
  title: {},
  addButton: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    gap: theme.spacing.xs,
  },
  addButtonText: {},
  emptyState: {
    alignItems: "center",
    paddingVertical: theme.spacing["2xl"],
    paddingHorizontal: theme.spacing.lg,
  },
  emptyIcon: { marginBottom: theme.spacing.lg },
  emptyTitle: { marginBottom: theme.spacing.sm, textAlign: "center" },
  emptySubtitle: { marginBottom: theme.spacing.lg, textAlign: "center" },
  emptyButton: {
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
  },
  remindersList: {},
});

export default CaregiverReminders;
