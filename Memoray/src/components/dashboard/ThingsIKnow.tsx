// src/components/dashboard/ThingsIKnow.tsx
import React from 'react';
import { View, StyleSheet, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { theme } from '../../utils/theme';
import { Text } from '../../ui/overrides/base';
import { useThingsIKnow } from '../../hooks/useThingsIKnow';

const ThingsIKnow: React.FC = () => {
  const { data, loading, error, refetch, state } = useThingsIKnow();
  const navigation = useNavigation();

  const categories = [
    { 
      key: 'people', 
      title: 'People', 
      emoji: '👥', 
      count: data.people.length,
      route: 'PeopleScreen'
    },
    { 
      key: 'food', 
      title: 'Food', 
      emoji: '🍽️', 
      count: data.food.length,
      route: 'FoodGalleryScreen'
    },
    { 
      key: 'cars', 
      title: 'Cars', 
      emoji: '🚗', 
      count: data.cars.length,
      route: 'CarGalleryScreen'
    },
    { 
      key: 'home', 
      title: 'Home', 
      emoji: '🏠', 
      count: data.home.length,
      route: 'HomeGalleryScreen'
    },
    { 
      key: 'landmarks', 
      title: 'Landmarks', 
      emoji: '📍', 
      count: data.landmarks.length,
      route: 'LandmarksGalleryScreen'
    },
    { 
      key: 'photos', 
      title: 'Photos', 
      emoji: '🖼️', 
      count: data.photos.length,
      route: 'PhotosGalleryScreen'
    },
  ];

  const renderCategoryTile = (category: typeof categories[0], index: number) => {
    return (
      <TouchableOpacity
        key={category.key}
        style={styles.categoryTile}
        onPress={() => navigation.navigate(category.route as never)}
        activeOpacity={0.8}
      >
        <View style={styles.tileContent}>
          <Text style={styles.categoryEmoji}>{category.emoji}</Text>
          <Text size="sm" weight="semibold" color="textPrimary" style={styles.categoryTitle}>
            {category.title}
          </Text>
        </View>
      </TouchableOpacity>
    );
  };

  const renderSkeletonTiles = () => {
    return [1, 2, 3, 4, 5, 6].map((i) => (
      <View key={i} style={[styles.categoryTile, styles.skeletonTile]}>
        <View style={styles.skeletonContent} />
      </View>
    ));
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
      <Text size="xl" weight="bold" color="textPrimary" style={styles.title}>
        My Memories
      </Text>
        {state === 'stale' && (
          <TouchableOpacity style={styles.refreshButton} onPress={refetch}>
            <Ionicons name="refresh" size={20} color={theme.colors.textSecondary} />
          </TouchableOpacity>
        )}
      </View>
      
      {error && (
        <View style={styles.errorContainer}>
          <Ionicons name="alert-circle" size={20} color={theme.colors.error || '#FF4444'} />
          <Text size="sm" color="textSecondary" style={styles.errorText}>
            {error}
          </Text>
          <TouchableOpacity style={styles.retryButton} onPress={refetch}>
            <Text size="xs" weight="semibold" color="textPrimary">
              Retry
            </Text>
          </TouchableOpacity>
        </View>
      )}

      <ScrollView 
        horizontal 
        showsHorizontalScrollIndicator={false} 
        style={styles.categoriesContainer}
        contentContainerStyle={styles.categoriesContent}
      >
        {loading ? renderSkeletonTiles() : categories.map(renderCategoryTile)}
      </ScrollView>
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
  refreshButton: {
    padding: theme.spacing.sm,
  },
  categoriesContainer: {
    marginTop: theme.spacing.md,
  },
  categoriesContent: {
    paddingHorizontal: theme.spacing.md,
    gap: theme.spacing.md,
  },
  categoryTile: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    padding: theme.spacing.md,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 90,
    height: 90,
    borderWidth: 1,
    borderColor: theme.colors.border,
    marginHorizontal: theme.spacing.xs,
  },
  tileContent: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  categoryEmoji: {
    fontSize: 28,
    lineHeight: 32,
    marginBottom: theme.spacing.xs,
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  categoryTitle: {
    textAlign: 'center',
  },
  skeletonTile: {
    backgroundColor: theme.colors.surfaceAlt,
  },
  skeletonContent: {
    flex: 1,
    backgroundColor: theme.colors.border,
    borderRadius: theme.radii.lg,
    width: '100%',
  },
  errorContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: theme.spacing.md,
    gap: theme.spacing.sm,
    backgroundColor: theme.colors.surfaceAlt,
    borderRadius: theme.radii.lg,
    marginBottom: theme.spacing.lg,
  },
  errorText: {
    flex: 1,
    textAlign: 'center',
  },
  retryButton: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.xs,
    paddingHorizontal: theme.spacing.sm,
  },
});

export default ThingsIKnow;
