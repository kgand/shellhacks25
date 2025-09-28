import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity, Image, Dimensions } from 'react-native';
import { Text, Avatar, Searchbar, Button, Surface, FAB, Chip, ActivityIndicator } from 'react-native-paper';
import { useRelationships } from '../hooks/useThingsIKnow';
import { theme } from '../utils/theme';

const PeopleScreen = ({ navigation }) => {
  const { data: people, loading, error, refetch } = useRelationships();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState('all');
  
  const { width } = Dimensions.get('window');
  const numColumns = width > 768 ? 1 : 2;
  
  // Memoized relationships options
  const relationshipsOptions = useMemo(
    () => ['all', ...new Set((people ?? []).map(p => p.Relation))],
    [people]
  );

  // Memoized filtered people
  const filteredPeople = useMemo(() => {
    const list = people ?? [];
    const q = searchQuery.trim().toLowerCase();
    return list.filter(p => {
      const matchQ = !q || `${p.First_name} ${p.Last_name}`.toLowerCase().includes(q) || p.Relation.toLowerCase().includes(q);
      const matchF = activeFilter === 'all' || p.Relation.toLowerCase() === activeFilter.toLowerCase();
      return matchQ && matchF;
    });
  }, [people, searchQuery, activeFilter]);
  
  // Format the last interaction date
  const formatLastInteraction = (dateString) => {
    if (!dateString) return 'No interactions';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    
    if (diffInDays === 0) return 'Today';
    if (diffInDays === 1) return 'Yesterday';
    if (diffInDays < 7) return `${diffInDays} days ago`;
    if (diffInDays < 30) return `${Math.floor(diffInDays / 7)} weeks ago`;
    return `${Math.floor(diffInDays / 30)} months ago`;
  };
  
  // Memoized key extractor
  const keyExtractor = useCallback((item, index) => 
    `${item.First_name}-${item.Last_name}-${index}`, []);

  // PersonCard component
  const PersonCard = useCallback(({ person, onPress }) => {
    const AVATAR_SIZE = 48;
    
    return (
      <TouchableOpacity
        style={styles.cardContainer}
        onPress={onPress}
        activeOpacity={0.8}
      >
        <View style={styles.personCard}>
          {/* Avatar */}
          <View style={[styles.avatarContainer, { width: AVATAR_SIZE, height: AVATAR_SIZE }]}>
            {person.Image ? (
              <Image source={{ uri: person.Image }} style={styles.avatarImage} />
            ) : (
              <Text style={styles.avatarText}>
                {`${person.First_name[0]}${person.Last_name[0]}`}
              </Text>
            )}
          </View>
          
          {/* Content */}
          <Text style={styles.personName} numberOfLines={1} ellipsizeMode="tail">
            {`${person.First_name} ${person.Last_name}`}
          </Text>
          <Text style={styles.personRelationship} numberOfLines={1} ellipsizeMode="tail">
            ({person.Relation})
          </Text>
          <Text style={styles.lastInteraction} numberOfLines={1} ellipsizeMode="tail">
            Last seen: {person["Last Seen"] || 'Unknown'}
          </Text>
        </View>
      </TouchableOpacity>
    );
  }, []);

  // Render a single person card
  const renderPersonItem = useCallback(({ item }) => (
    <PersonCard
      person={item}
      onPress={() => navigation.navigate('PersonDetail', { personId: item.id })}
    />
  ), [navigation, PersonCard]);

  // Header component for FlatList (moved above early returns)
  const ListHeader = useCallback(() => (
    <View>
      <Searchbar
        placeholder="Search people..."
        onChangeText={setSearchQuery}
        value={searchQuery}
        style={styles.searchBar}
        iconColor={theme.colors.accent}
        inputStyle={{ color: theme.colors.textPrimary }}
        placeholderTextColor={theme.colors.textSecondary}
        textColor={theme.colors.textPrimary}
        theme={{ colors: { primary: theme.colors.accent } }}
      />
      
      <View style={styles.filterContainer}>
        <FlatList
          horizontal
          data={relationshipsOptions}
          keyExtractor={(item) => item}
          renderItem={({ item }) => (
            <Chip
              selected={item === activeFilter}
              onPress={() => setActiveFilter(item)}
              style={[
                styles.filterChip,
                item === activeFilter && styles.activeFilterChip
              ]}
              textStyle={[
                styles.filterChipText,
                item === activeFilter && styles.activeFilterChipText
              ]}
            >
              {item === 'all' ? 'All' : item}
            </Chip>
          )}
          showsHorizontalScrollIndicator={false}
        />
      </View>
      
      <View style={styles.divider} />
    </View>
  ), [searchQuery, activeFilter, relationshipsOptions]);
  
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={styles.loadingText}>Loading people...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Failed to load people: {error}</Text>
        <Button onPress={refetch} style={styles.retryButton}>
          Retry
        </Button>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {filteredPeople.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyText}>No people yet</Text>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('AddPerson')}
            style={styles.addButton}
          >
            Add Person
          </Button>
        </View>
      ) : (
        <FlatList
          data={filteredPeople}
          keyExtractor={keyExtractor}
          renderItem={renderPersonItem}
          numColumns={numColumns}
          ListHeaderComponent={ListHeader}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
        />
      )}
      
      <FAB
        style={styles.fab}
        icon="plus"
        color="#fff"
        onPress={() => navigation.navigate('AddPerson')}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.pageBg,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.pageBg,
  },
  loadingText: {
    marginTop: theme.spacing.lg,
    color: theme.colors.textPrimary,
    fontSize: theme.fonts.sizes.md,
  },
  searchBar: {
    margin: theme.spacing.md,
    backgroundColor: theme.colors.cardBg,
    elevation: 2,
  },
  filterContainer: {
    paddingHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.md,
  },
  filterChip: {
    marginRight: theme.spacing.sm,
    backgroundColor: theme.colors.cardBg,
  },
  activeFilterChip: {
    backgroundColor: theme.colors.accent,
  },
  filterChipText: {
    color: theme.colors.textPrimary,
  },
  activeFilterChipText: {
    color: theme.colors.textPrimary,
  },
  divider: {
    height: 1,
    backgroundColor: theme.colors.cardBorder,
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.lg,
  },
  listContent: {
    paddingHorizontal: theme.spacing.md,
    paddingBottom: 24, // Space for FAB
  },
  cardContainer: {
    flex: 1,
    margin: theme.spacing.xs,
    maxWidth: '48%',
    minHeight: 120,
  },
  personCard: {
    padding: theme.spacing.sm,
    borderRadius: 14,
    backgroundColor: theme.colors.cardBg,
    borderColor: theme.colors.cardBorder,
    borderWidth: 1,
    alignItems: 'center',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    gap: 4,
    flex: 1,
    justifyContent: 'center',
  },
  avatarContainer: {
    borderRadius: 24,
    backgroundColor: '#262A2F',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: theme.spacing.xs,
    overflow: 'hidden',
  },
  avatarImage: {
    width: '100%',
    height: '100%',
  },
  avatarText: {
    fontSize: 24,
    lineHeight: 28,
    color: theme.colors.textPrimary,
    fontWeight: '600',
    textAlign: 'center',
    includeFontPadding: false,
    textAlignVertical: 'center',
  },
  personName: {
    fontSize: theme.fonts.sizes.md,
    fontWeight: 'bold',
    color: theme.colors.textPrimary,
    textAlign: 'center',
  },
  personRelationship: {
    fontSize: theme.fonts.sizes.sm,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  lastInteraction: {
    fontSize: theme.fonts.sizes.xs,
    color: theme.colors.textTertiary,
    textAlign: 'center',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
  },
  emptyText: {
    fontSize: theme.fonts.sizes.lg,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.xl,
    textAlign: 'center',
  },
  addButton: {
    backgroundColor: theme.colors.accent,
  },
  retryButton: {
    backgroundColor: theme.colors.accent,
    marginTop: theme.spacing.lg,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.accent,
  },
});

export default PeopleScreen;