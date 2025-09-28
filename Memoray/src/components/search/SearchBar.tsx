import React, { useState, useCallback } from 'react';
import { View, StyleSheet, TextInput, TouchableOpacity, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';
import { useRelationships } from '../../hooks/useThingsIKnow';
import Input from '../ui/Input';
import Card from '../ui/Card';

interface SearchResult {
  id: string;
  type: 'reminder' | 'person' | 'place' | 'photo';
  title: string;
  subtitle?: string;
  icon: string;
  route?: string;
}

const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const navigation = useNavigation();
  const { data: relationships } = useRelationships();

  const searchData = useCallback((searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    const searchResults: SearchResult[] = [];

    // Search people
    relationships.forEach((person) => {
      const fullName = `${person.First_name} ${person.Last_name}`.toLowerCase();
      if (fullName.includes(searchQuery.toLowerCase()) || 
          person.Relation.toLowerCase().includes(searchQuery.toLowerCase())) {
        searchResults.push({
          id: `person-${person.First_name}-${person.Last_name}`,
          type: 'person',
          title: `${person.First_name} ${person.Last_name}`,
          subtitle: person.Relation,
          icon: 'person',
          route: 'PeopleScreen',
        });
      }
    });

    // Add more search categories as needed
    // For now, we'll add some mock results for demonstration
    if (searchQuery.toLowerCase().includes('reminder')) {
      searchResults.push({
        id: 'reminder-medicine',
        type: 'reminder',
        title: 'Take Medicine',
        subtitle: 'Daily reminder',
        icon: 'alarm',
        route: 'Dashboard',
      });
    }

    if (searchQuery.toLowerCase().includes('photo')) {
      searchResults.push({
        id: 'photo-gallery',
        type: 'photo',
        title: 'Photo Gallery',
        subtitle: 'View all photos',
        icon: 'images',
        route: 'PhotosGalleryScreen',
      });
    }

    setResults(searchResults.slice(0, 5)); // Limit to 5 results
  }, [relationships]);

  const handleSearchChange = (text: string) => {
    setQuery(text);
    searchData(text);
  };

  const handleResultPress = (result: SearchResult) => {
    if (result.route) {
      navigation.navigate(result.route as never);
    }
    setQuery('');
    setResults([]);
    setIsFocused(false);
  };

  const handleFocus = () => {
    setIsFocused(true);
    if (query) {
      searchData(query);
    }
  };

  const handleBlur = () => {
    // Delay blur to allow result selection
    setTimeout(() => setIsFocused(false), 150);
  };

  const renderSearchResult = ({ item }: { item: SearchResult }) => (
    <TouchableOpacity
      style={styles.resultItem}
      onPress={() => handleResultPress(item)}
      activeOpacity={0.7}
    >
      <Ionicons 
        name={item.icon as any} 
        size={20} 
        color={theme.colors.textSecondary} 
        style={styles.resultIcon}
      />
      <View style={styles.resultContent}>
        <Text size="md" color="textPrimary" weight="medium">
          {item.title}
        </Text>
        {item.subtitle && (
          <Text size="sm" color="textSecondary">
            {item.subtitle}
          </Text>
        )}
      </View>
      <Ionicons 
        name="chevron-forward" 
        size={16} 
        color={theme.colors.textSecondary} 
      />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Input
        placeholder="Search people, places, photos..."
        value={query}
        onChangeText={handleSearchChange}
        leftIcon="search"
        rightIcon={query.length > 0 ? "close-circle" : undefined}
        onRightIconPress={() => {
          setQuery('');
          setResults([]);
        }}
        onFocus={handleFocus}
        onBlur={handleBlur}
        accessibilityLabel="Search"
        accessibilityHint="Search for people, places, and photos"
      />

      {/* Search Results */}
      {isFocused && results.length > 0 && (
        <Card variant="elevated" style={styles.resultsContainer}>
          <FlatList
            data={results}
            renderItem={renderSearchResult}
            keyExtractor={(item) => item.id}
            style={styles.resultsList}
            showsVerticalScrollIndicator={false}
          />
        </Card>
      )}

      {/* No Results */}
      {isFocused && query.length > 0 && results.length === 0 && (
        <Card variant="outlined" style={styles.noResultsContainer}>
          <Text size="sm" color="textSecondary" style={styles.noResultsText}>
            No results found for "{query}"
          </Text>
        </Card>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'relative',
    zIndex: 10,
    marginBottom: theme.spacing.md,
  },
  resultsContainer: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    maxHeight: 300,
    zIndex: 1000,
  },
  resultsList: {
    maxHeight: 300,
  },
  resultItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  resultIcon: {
    marginRight: theme.spacing.sm,
  },
  resultContent: {
    flex: 1,
  },
  noResultsContainer: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    padding: theme.spacing.lg,
    alignItems: 'center',
  },
  noResultsText: {
    textAlign: 'center',
  },
});

export default SearchBar;
