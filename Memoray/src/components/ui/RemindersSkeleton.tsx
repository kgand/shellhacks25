import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { theme } from '../../utils/theme';
import SkeletonLoader from './SkeletonLoader';

const RemindersSkeleton: React.FC = () => {
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header */}
      <View style={styles.header}>
        <SkeletonLoader width={180} height={28} borderRadius={14} />
        <SkeletonLoader width={100} height={36} borderRadius={18} />
      </View>

      {/* Reminder Items */}
      {[1, 2, 3, 4, 5].map((index) => (
        <View key={index} style={styles.reminderItem}>
          <View style={styles.reminderContent}>
            {/* Icon */}
            <SkeletonLoader width={48} height={48} borderRadius={24} />
            
            {/* Text Content */}
            <View style={styles.textContent}>
              <SkeletonLoader width="85%" height={20} borderRadius={10} />
              <View style={styles.spacing} />
              <SkeletonLoader width="70%" height={16} borderRadius={8} />
              <View style={styles.spacing} />
              <SkeletonLoader width="60%" height={14} borderRadius={7} />
            </View>
          </View>

          {/* Actions */}
          <View style={styles.actions}>
            <SkeletonLoader width={24} height={24} borderRadius={12} />
            <View style={styles.actionSpacing} />
            <SkeletonLoader width={24} height={24} borderRadius={12} />
          </View>
        </View>
      ))}

      {/* Empty State Placeholder */}
      <View style={styles.emptyState}>
        <SkeletonLoader width={80} height={80} borderRadius={40} />
        <View style={styles.spacing} />
        <SkeletonLoader width={200} height={20} borderRadius={10} />
        <View style={styles.spacing} />
        <SkeletonLoader width={250} height={16} borderRadius={8} />
        <View style={styles.spacing} />
        <SkeletonLoader width={150} height={40} borderRadius={20} />
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.lg,
    marginBottom: theme.spacing.md,
  },
  reminderItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    marginHorizontal: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  reminderContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  textContent: {
    flex: 1,
    marginLeft: theme.spacing.md,
  },
  actions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  actionSpacing: {
    width: theme.spacing.sm,
  },
  spacing: {
    height: theme.spacing.sm,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: theme.spacing['2xl'],
    paddingHorizontal: theme.spacing.lg,
  },
});

export default RemindersSkeleton;
