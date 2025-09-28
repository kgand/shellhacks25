// src/components/dashboard/reminders/AddEditReminderDialog.tsx
import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Modal, TouchableOpacity, ScrollView, TextInput as RNTextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../../ui/overrides/base';
import type { Reminder, Audience } from '../../../state/reminders/types';

interface AddEditReminderDialogProps {
  visible: boolean;
  onClose: () => void;
  onSave: (reminder: Omit<Reminder, 'id'>) => void;
  editingReminder?: Reminder;
  audience?: Audience;
}

const COMMON_ICONS = ['💊', '🚰', '📞', '🚶', '🍽️', '💤', '🏥', '📅', '⏰', '🏃', '🚗', '🏠'];

const HOURS = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));
const MINUTES = Array.from({ length: 12 }, (_, i) => (i * 5).toString().padStart(2, '0'));

const AddEditReminderDialog: React.FC<AddEditReminderDialogProps> = ({ 
  visible, 
  onClose, 
  onSave, 
  editingReminder,
  audience
}) => {
  const [icon, setIcon] = useState('💊');
  const [label, setLabel] = useState('');
  const [notes, setNotes] = useState('');
  const [scheduleType, setScheduleType] = useState<'time' | 'interval'>('time');
  const [selectedHour, setSelectedHour] = useState('08');
  const [selectedMinute, setSelectedMinute] = useState('00');
  const [intervalMinutes, setIntervalMinutes] = useState(120); // 2 hours in minutes
  const [errors, setErrors] = useState<{ label?: string }>({});

  useEffect(() => {
    if (editingReminder) {
      setIcon(editingReminder.icon || '💊');
      setLabel(editingReminder.label);
      setNotes(editingReminder.notes || '');
      setScheduleType(editingReminder.scheduleType);
      if (editingReminder.time) {
        const [hour, minute] = editingReminder.time.split(':');
        setSelectedHour(hour);
        setSelectedMinute(minute);
      }
      if (editingReminder.intervalMinutes) {
        setIntervalMinutes(editingReminder.intervalMinutes);
      }
    } else {
      // Reset form for new reminder
      setIcon('💊');
      setLabel('');
      setNotes('');
      setScheduleType('time');
      setSelectedHour('08');
      setSelectedMinute('00');
      setIntervalMinutes(120);
    }
    setErrors({});
  }, [editingReminder, visible]);

  const validateForm = () => {
    const newErrors: { label?: string } = {};
    
    if (!label.trim()) {
      newErrors.label = 'Label is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = () => {
    if (validateForm()) {
      const reminderData: Omit<Reminder, 'id'> = {
        icon,
        label: label.trim(),
        notes: notes.trim() || undefined,
        scheduleType,
        audience: audience || 'patient',
        ...(scheduleType === 'time' 
          ? { time: `${selectedHour}:${selectedMinute}` }
          : { intervalMinutes }
        ),
      };
      
      onSave(reminderData);
      handleClose();
    }
  };

  const handleClose = () => {
    setIcon('💊');
    setLabel('');
    setNotes('');
    setScheduleType('time');
    setSelectedHour('08');
    setSelectedMinute('00');
    setIntervalMinutes(120);
    setErrors({});
    onClose();
  };

  const renderTimePicker = () => (
    <View style={styles.timePickerContainer}>
      <View style={styles.timePicker}>
        <ScrollView 
          style={styles.timeScroll}
          showsVerticalScrollIndicator={false}
          snapToInterval={40}
          decelerationRate="fast"
        >
          {HOURS.map((hour) => (
            <TouchableOpacity
              key={hour}
              style={[
                styles.timeOption,
                selectedHour === hour && styles.selectedTimeOption
              ]}
              onPress={() => setSelectedHour(hour)}
            >
              <Text 
                size="lg" 
                color={selectedHour === hour ? "textPrimary" : "textSecondary"}
                weight={selectedHour === hour ? "semibold" : "regular"}
              >
                {hour}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
      
      <Text size="lg" color="textSecondary" style={styles.timeSeparator}>:</Text>
      
      <View style={styles.timePicker}>
        <ScrollView 
          style={styles.timeScroll}
          showsVerticalScrollIndicator={false}
          snapToInterval={40}
          decelerationRate="fast"
        >
          {MINUTES.map((minute) => (
            <TouchableOpacity
              key={minute}
              style={[
                styles.timeOption,
                selectedMinute === minute && styles.selectedTimeOption
              ]}
              onPress={() => setSelectedMinute(minute)}
            >
              <Text 
                size="lg" 
                color={selectedMinute === minute ? "textPrimary" : "textSecondary"}
                weight={selectedMinute === minute ? "semibold" : "regular"}
              >
                {minute}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </View>
  );

  const renderIntervalSelector = () => (
    <View style={styles.intervalContainer}>
      <Text size="md" color="textSecondary" style={styles.intervalLabel}>
        Every
      </Text>
      <View style={styles.intervalSelector}>
        <TouchableOpacity
          style={styles.intervalButton}
          onPress={() => setIntervalMinutes(Math.max(15, intervalMinutes - 15))}
        >
          <Ionicons name="remove" size={20} color={theme.colors.textPrimary} />
        </TouchableOpacity>
        <Text size="xl" weight="bold" color="textPrimary" style={styles.intervalValue}>
          {Math.floor(intervalMinutes / 60)}h {intervalMinutes % 60}m
        </Text>
        <TouchableOpacity
          style={styles.intervalButton}
          onPress={() => setIntervalMinutes(Math.min(720, intervalMinutes + 15))}
        >
          <Ionicons name="add" size={20} color={theme.colors.textPrimary} />
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <Modal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={handleClose}
    >
      <View style={styles.overlay}>
        <View style={styles.dialog}>
          <View style={styles.header}>
            <Text size="xl" weight="bold" color="textPrimary">
              {editingReminder ? 'Edit Reminder' : 'Add Reminder'}
            </Text>
            <TouchableOpacity onPress={handleClose} style={styles.closeButton}>
              <Ionicons name="close" size={24} color={theme.colors.textSecondary} />
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.content}>
            {/* Icon Selection */}
            <View style={styles.section}>
              <Text size="md" weight="semibold" color="textPrimary" style={styles.label}>
                Icon
              </Text>
              <View style={styles.iconGrid}>
                {COMMON_ICONS.map((emoji) => (
                  <TouchableOpacity
                    key={emoji}
                    style={[
                      styles.iconButton,
                      icon === emoji && styles.selectedIcon
                    ]}
                    onPress={() => setIcon(emoji)}
                  >
                    <Text style={styles.iconText}>{emoji}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Label Input */}
            <View style={styles.section}>
              <Text size="md" weight="semibold" color="textPrimary" style={styles.label}>
                Label *
              </Text>
              <RNTextInput
                value={label}
                onChangeText={setLabel}
                placeholder="e.g., Take your medicine"
                style={styles.input}
                placeholderTextColor={theme.colors.textSecondary}
              />
              {errors.label && (
                <Text size="sm" color="error" style={styles.errorText}>
                  {errors.label}
                </Text>
              )}
            </View>

            {/* Notes Input */}
            <View style={styles.section}>
              <Text size="md" weight="semibold" color="textPrimary" style={styles.label}>
                Notes (optional)
              </Text>
              <RNTextInput
                value={notes}
                onChangeText={setNotes}
                placeholder="Additional details..."
                style={styles.input}
                placeholderTextColor={theme.colors.textSecondary}
                multiline
                numberOfLines={2}
              />
            </View>

            {/* Schedule Type Pills */}
            <View style={styles.section}>
              <Text size="md" weight="semibold" color="textPrimary" style={styles.label}>
                Schedule
              </Text>
              <View style={styles.pillContainer}>
                <TouchableOpacity
                  style={[
                    styles.pill,
                    scheduleType === 'time' && styles.activePill
                  ]}
                  onPress={() => setScheduleType('time')}
                >
                  <Text 
                    size="sm" 
                    weight="semibold" 
                    color={scheduleType === 'time' ? "textPrimary" : "textSecondary"}
                  >
                    At a time
                  </Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[
                    styles.pill,
                    scheduleType === 'interval' && styles.activePill
                  ]}
                  onPress={() => setScheduleType('interval')}
                >
                  <Text 
                    size="sm" 
                    weight="semibold" 
                    color={scheduleType === 'interval' ? "textPrimary" : "textSecondary"}
                  >
                    Every X hours
                  </Text>
                </TouchableOpacity>
              </View>
            </View>

            {/* Time Picker or Interval Selector */}
            <View style={styles.section}>
              {scheduleType === 'time' ? renderTimePicker() : renderIntervalSelector()}
            </View>
          </ScrollView>

          <View style={styles.footer}>
            <TouchableOpacity style={styles.cancelButton} onPress={handleClose}>
              <Text size="md" weight="semibold" color="textPrimary">
                Cancel
              </Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.saveButton} onPress={handleSave}>
              <Text size="md" weight="semibold" color="textPrimary">
                {editingReminder ? 'Update' : 'Add'} Reminder
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
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.sm,
  },
  dialog: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    width: '100%',
    maxWidth: 400,
    maxHeight: '85%',
    marginHorizontal: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: theme.spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  closeButton: {
    padding: theme.spacing.xs,
  },
  content: {
    padding: theme.spacing.lg,
  },
  section: {
    marginBottom: theme.spacing.lg,
  },
  label: {
    marginBottom: theme.spacing.sm,
  },
  iconGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.sm,
  },
  iconButton: {
    width: 44,
    height: 44,
    borderRadius: theme.radii.md,
    backgroundColor: theme.colors.inputBg,
    borderColor: theme.colors.border,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
    margin: theme.spacing.xs,
  },
  selectedIcon: {
    backgroundColor: theme.colors.accent,
    borderColor: theme.colors.accent,
  },
  iconText: {
    fontSize: 20,
    lineHeight: 24,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  input: {
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.lg,
    borderColor: theme.colors.inputBorder,
    borderWidth: 1,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.md,
    color: theme.colors.textPrimary,
    fontSize: 16,
    minHeight: 48,
  },
  errorText: {
    marginTop: theme.spacing.xs,
  },
  pillContainer: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  pill: {
    flex: 1,
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.sm,
    paddingHorizontal: theme.spacing.md,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: theme.colors.border,
    minHeight: 44,
  },
  activePill: {
    backgroundColor: theme.colors.accent,
    borderColor: theme.colors.accent,
  },
  timePickerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
  },
  timePicker: {
    height: 120,
    width: 60,
  },
  timeScroll: {
    flex: 1,
  },
  timeOption: {
    height: 44,
    alignItems: 'center',
    justifyContent: 'center',
  },
  selectedTimeOption: {
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.md,
  },
  timeSeparator: {
    marginHorizontal: theme.spacing.sm,
  },
  intervalContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.colors.inputBg,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  intervalLabel: {
    // default from Text component
  },
  intervalSelector: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.sm,
    gap: theme.spacing.md,
  },
  intervalButton: {
    width: 36,
    height: 36,
    borderRadius: theme.radii.md,
    backgroundColor: theme.colors.inputBg,
    alignItems: 'center',
    justifyContent: 'center',
  },
  intervalValue: {
    minWidth: 40,
    textAlign: 'center',
  },
  footer: {
    flexDirection: 'row',
    padding: theme.spacing.lg,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
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
});

export default AddEditReminderDialog;
