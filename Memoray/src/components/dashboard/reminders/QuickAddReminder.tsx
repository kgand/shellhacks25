import React, { useState } from 'react';
import { View, StyleSheet, Modal, TouchableOpacity, TextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../../ui/overrides/base';
import { useReminders } from '../../../state/reminders';

interface QuickAddReminderProps {
  visible: boolean;
  onClose: () => void;
}

const QuickAddReminder: React.FC<QuickAddReminderProps> = ({ visible, onClose }) => {
  const [reminderText, setReminderText] = useState('');
  const [selectedTime, setSelectedTime] = useState('08:00');
  const { addReminder } = useReminders();

  const quickTimes = ['08:00', '12:00', '18:00', '20:00'];
  const quickReminders = [
    { text: 'Take medicine', icon: '💊' },
    { text: 'Drink water', icon: '🚰' },
    { text: 'Call family', icon: '📞' },
    { text: 'Go for a walk', icon: '🚶' },
  ];

  const handleSave = async () => {
    if (!reminderText.trim()) return;

    try {
      await addReminder({
        label: reminderText.trim(),
        icon: '⏰',
        scheduleType: 'time',
        time: selectedTime,
        audience: 'patient',
      });
      
      setReminderText('');
      onClose();
    } catch (error) {
      console.error('Error adding reminder:', error);
    }
  };

  const handleQuickReminder = (reminder: typeof quickReminders[0]) => {
    setReminderText(reminder.text);
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="slide"
      onRequestClose={onClose}
    >
      <View style={styles.overlay}>
        <View style={styles.modal}>
          {/* Header */}
          <View style={styles.header}>
            <Text size="xl" weight="bold" color="textPrimary">
              Quick Add Reminder
            </Text>
            <TouchableOpacity onPress={onClose} style={styles.closeButton}>
              <Ionicons name="close" size={24} color={theme.colors.textSecondary} />
            </TouchableOpacity>
          </View>

          {/* Quick Reminders */}
          <View style={styles.section}>
            <Text size="md" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
              Quick Options
            </Text>
            <View style={styles.quickReminders}>
              {quickReminders.map((reminder, index) => (
                <TouchableOpacity
                  key={index}
                  style={styles.quickReminderButton}
                  onPress={() => handleQuickReminder(reminder)}
                >
                  <Text style={styles.quickReminderIcon}>{reminder.icon}</Text>
                  <Text size="sm" color="textPrimary" style={styles.quickReminderText}>
                    {reminder.text}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Custom Reminder Input */}
          <View style={styles.section}>
            <Text size="md" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
              Custom Reminder
            </Text>
            <TextInput
              style={styles.textInput}
              placeholder="What do you want to be reminded about?"
              placeholderTextColor={theme.colors.textSecondary}
              value={reminderText}
              onChangeText={setReminderText}
              multiline
              maxLength={100}
            />
          </View>

          {/* Time Selection */}
          <View style={styles.section}>
            <Text size="md" weight="semibold" color="textPrimary" style={styles.sectionTitle}>
              Remind me at
            </Text>
            <View style={styles.timeOptions}>
              {quickTimes.map((time) => (
                <TouchableOpacity
                  key={time}
                  style={[
                    styles.timeButton,
                    selectedTime === time && styles.timeButtonSelected,
                  ]}
                  onPress={() => setSelectedTime(time)}
                >
                  <Text
                    size="md"
                    color={selectedTime === time ? "textPrimary" : "textSecondary"}
                    weight={selectedTime === time ? "semibold" : "regular"}
                  >
                    {time}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Actions */}
          <View style={styles.actions}>
            <TouchableOpacity style={styles.cancelButton} onPress={onClose}>
              <Text size="md" weight="semibold" color="textPrimary">
                Cancel
              </Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.saveButton, !reminderText.trim() && styles.saveButtonDisabled]}
              onPress={handleSave}
              disabled={!reminderText.trim()}
            >
              <Text size="md" weight="semibold" color="textPrimary">
                Add Reminder
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },
  modal: {
    backgroundColor: theme.colors.surface,
    borderTopLeftRadius: theme.radii.xl,
    borderTopRightRadius: theme.radii.xl,
    paddingTop: theme.spacing.lg,
    paddingBottom: 40,
    maxHeight: '85%',
    marginHorizontal: theme.spacing.xs,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.xl,
    paddingBottom: theme.spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  closeButton: {
    padding: theme.spacing.xs,
  },
  section: {
    paddingHorizontal: theme.spacing.xl,
    paddingVertical: theme.spacing.lg,
  },
  sectionTitle: {
    marginBottom: theme.spacing.md,
  },
  quickReminders: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },
  quickReminderButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.lg,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    gap: theme.spacing.xs,
    minHeight: 36,
  },
  quickReminderIcon: {
    fontSize: 14,
    lineHeight: 18,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  quickReminderText: {
    flex: 1,
  },
  textInput: {
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.lg,
    borderWidth: 1,
    borderColor: theme.colors.inputBorder,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
    color: theme.colors.textPrimary,
    fontSize: 16,
    minHeight: 70,
    textAlignVertical: 'top',
    maxHeight: 120,
  },
  timeOptions: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  timeButton: {
    flex: 1,
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.lg,
    paddingVertical: theme.spacing.sm,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: theme.colors.border,
    minHeight: 40,
  },
  timeButtonSelected: {
    backgroundColor: theme.colors.accent,
    borderColor: theme.colors.accent,
  },
  actions: {
    flexDirection: 'row',
    paddingHorizontal: theme.spacing.xl,
    paddingTop: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  cancelButton: {
    flex: 1,
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    alignItems: 'center',
    minHeight: 48,
  },
  saveButton: {
    flex: 1,
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    alignItems: 'center',
    minHeight: 48,
  },
  saveButtonDisabled: {
    opacity: 0.5,
  },
});

export default QuickAddReminder;
