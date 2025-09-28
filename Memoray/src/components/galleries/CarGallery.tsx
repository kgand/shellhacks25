// src/components/galleries/CarGallery.tsx
import React from 'react';
import { View, StyleSheet, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../utils/theme';
import { Text } from '../../ui/overrides/base';
import { useCar } from '../../hooks/useThingsIKnow';

const CarGallery: React.FC = () => {
  const { data, loading, error, refetch, state } = useCar();

  const renderPhotoCard = (item: any, index: number) => (
    <TouchableOpacity
      key={index}
      style={styles.photoCard}
      onPress={() => console.log('View photo:', item.name)}
    >
      <View style={styles.imageContainer}>
        <Image
          source={{ uri: item.url }}
          style={styles.image}
          resizeMode="cover"
        />
        {state === 'stale' && (
          <View style={styles.staleIndicator}>
            <Ionicons name="refresh" size={12} color={theme.colors.textSecondary} />
          </View>
        )}
      </View>
      <Text size="sm" color="textPrimary" style={styles.photoName} numberOfLines={2}>
        {item.name}
      </Text>
    </TouchableOpacity>
  );

  if (loading && data.length === 0) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.accent} />
        <Text size="md" color="textSecondary" style={styles.loadingText}>
          Loading car photos...
        </Text>
      </View>
    );
  }

  if (error && data.length === 0) {
    return (
      <View style={styles.errorContainer}>
        <Ionicons name="alert-circle" size={48} color={theme.colors.error || '#FF4444'} />
        <Text size="md" color="textPrimary" style={styles.errorTitle}>
          Failed to load photos
        </Text>
        <Text size="sm" color="textSecondary" style={styles.errorMessage}>
          {error}
        </Text>
        <TouchableOpacity style={styles.retryButton} onPress={refetch}>
          <Text size="sm" weight="semibold" color="textPrimary">
            Try Again
          </Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (data.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Ionicons name="car" size={48} color={theme.colors.textSecondary} />
        <Text size="md" color="textPrimary" style={styles.emptyTitle}>
          No car photos yet
        </Text>
        <Text size="sm" color="textSecondary" style={styles.emptyMessage}>
          Add some car photos to get started
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text size="xl" weight="bold" color="textPrimary">
          Car Gallery
        </Text>
        {state === 'stale' && (
          <TouchableOpacity style={styles.refreshButton} onPress={refetch}>
            <Ionicons name="refresh" size={20} color={theme.colors.textSecondary} />
          </TouchableOpacity>
        )}
      </View>
      
      <View style={styles.grid}>
        {data.map(renderPhotoCard)}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  refreshButton: {
    padding: theme.spacing.sm,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: theme.spacing.md,
  },
  photoCard: {
    width: '48%',
    backgroundColor: theme.colors.surface,
    borderRadius: theme.radii.lg,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  imageContainer: {
    position: 'relative',
    aspectRatio: 1,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  staleIndicator: {
    position: 'absolute',
    top: theme.spacing.xs,
    right: theme.spacing.xs,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: theme.radii.round,
    padding: theme.spacing.xs,
  },
  photoName: {
    padding: theme.spacing.sm,
    textAlign: 'center',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  loadingText: {
    marginTop: theme.spacing.md,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  errorTitle: {
    marginTop: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },
  errorMessage: {
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  retryButton: {
    backgroundColor: theme.colors.accent,
    borderRadius: theme.radii.round,
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  emptyTitle: {
    marginTop: theme.spacing.md,
    marginBottom: theme.spacing.sm,
  },
  emptyMessage: {
    textAlign: 'center',
  },
});

export default CarGallery;
