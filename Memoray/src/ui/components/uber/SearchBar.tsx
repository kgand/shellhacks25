// src/ui/components/uber/SearchBar.tsx
import React from 'react';
import { View, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../../../utils/theme';
import { Text } from '../../overrides/base';

interface SearchBarProps {
  placeholder?: string;
  onPress?: () => void;
  onLaterPress?: () => void;
}

export const SearchBar = ({ 
  placeholder = "Where to?", 
  onPress, 
  onLaterPress 
}: SearchBarProps) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.searchInput} onPress={onPress}>
        <Ionicons name="search" size={20} color={theme.colors.textSecondary} />
        <TextInput
          placeholder={placeholder}
          placeholderTextColor={theme.colors.textSecondary}
          style={styles.input}
          editable={false}
        />
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.laterButton} onPress={onLaterPress}>
        <Text size="sm" weight="semibold" color="textPrimary">Later</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.md,
    marginHorizontal: theme.spacing.lg,
    marginVertical: theme.spacing.lg,
  },
  searchInput: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.inputBg,
    borderColor: theme.colors.inputBorder,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    height: 52,
    paddingHorizontal: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  input: {
    flex: 1,
    fontSize: theme.fonts?.sizes?.md ?? 15,
    color: theme.colors.textPrimary,
    fontFamily: 'Inter-Regular',
  },
  laterButton: {
    backgroundColor: theme.colors.surface,
    borderColor: theme.colors.border,
    borderWidth: 1,
    borderRadius: theme.radii.lg,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.md,
    minHeight: 44,
    justifyContent: 'center',
  },
});
