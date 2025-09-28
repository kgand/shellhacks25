import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { theme } from '../../utils/theme';
import SkeletonLoader from './SkeletonLoader';

const DashboardSkeleton: React.FC = () => {
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Header Section */}
      <View style={styles.section}>
        <SkeletonLoader width={200} height={32} borderRadius={16} />
        <View style={styles.spacing} />
        <SkeletonLoader width={150} height={20} borderRadius={10} />
      </View>

      {/* Daily Reminders Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <SkeletonLoader width={120} height={24} borderRadius={12} />
          <SkeletonLoader width={80} height={32} borderRadius={16} />
        </View>
        
        {/* Reminder Cards */}
        {[1, 2, 3].map((index) => (
          <View key={index} style={styles.reminderCard}>
            <View style={styles.reminderContent}>
              <SkeletonLoader width={40} height={40} borderRadius={20} />
              <View style={styles.reminderText}>
                <SkeletonLoader width="80%" height={18} borderRadius={9} />
                <View style={styles.spacing} />
                <SkeletonLoader width="60%" height={14} borderRadius={7} />
              </View>
            </View>
            <SkeletonLoader width={24} height={24} borderRadius={12} />
          </View>
        ))}
      </View>

      {/* Things I Know Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <SkeletonLoader width={140} height={24} borderRadius={12} />
        </View>
        
        {/* Category Tiles */}
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          style={styles.categoriesContainer}
        >
          {[1, 2, 3, 4, 5, 6].map((index) => (
            <View key={index} style={styles.categoryTile}>
              <SkeletonLoader width={60} height={60} borderRadius={30} />
              <View style={styles.spacing} />
              <SkeletonLoader width={80} height={16} borderRadius={8} />
            </View>
          ))}
        </ScrollView>
      </View>

      {/* Gamification Section */}
      <View style={styles.section}>
        <View style={styles.gamificationCard}>
          <View style={styles.gamificationContent}>
            <SkeletonLoader width={80} height={80} borderRadius={40} />
            <View style={styles.gamificationText}>
              <SkeletonLoader width={120} height={20} borderRadius={10} />
              <View style={styles.spacing} />
              <SkeletonLoader width={200} height={16} borderRadius={8} />
            </View>
          </View>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  section: {
    marginBottom: theme.spacing.xl,
    paddingHorizontal: theme.spacing.lg,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  spacing: {
    height: theme.spacing.sm,
  },
  reminderCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  reminderContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  reminderText: {
    flex: 1,
    marginLeft: theme.spacing.md,
  },
  categoriesContainer: {
    marginTop: theme.spacing.md,
  },
  categoryTile: {
    alignItems: 'center',
    marginRight: theme.spacing.lg,
    width: 100,
  },
  gamificationCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.xl,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  gamificationContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  gamificationText: {
    flex: 1,
    marginLeft: theme.spacing.lg,
  },
});

export default DashboardSkeleton;
