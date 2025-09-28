import React from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { Text } from '../../ui/overrides/base';
import { theme } from '../../utils/theme';
import Card from '../ui/Card';
import AccessibilityWrapper from '../ui/AccessibilityWrapper';

interface QuickActionsProps {
  onQuickAddReminder?: () => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onQuickAddReminder }) => {
  const navigation = useNavigation();

  const actions = [
    {
      id: 'add-reminder',
      title: 'Add Reminder',
      icon: 'alarm-outline',
      color: theme.colors.accent,
      onPress: () => {
        onQuickAddReminder?.();
      },
    },
    {
      id: 'add-person',
      title: 'Add Person',
      icon: 'person-add-outline',
      color: theme.colors.success,
      onPress: () => {
        navigation.navigate('AddPerson' as never);
      },
    },
    {
      id: 'take-photo',
      title: 'Take Photo',
      icon: 'camera-outline',
      color: theme.colors.warning,
      onPress: () => {
        navigation.navigate('Camera' as never);
      },
    },
  ];

  return (
    <View style={styles.container}>
      <Text size="lg" weight="semibold" color="textPrimary" style={styles.title}>
        Quick Actions
      </Text>
      
      <View style={styles.actionsGrid}>
        {actions.map((action) => (
          <AccessibilityWrapper
            key={action.id}
            onPress={action.onPress}
            accessibilityLabel={action.title}
            accessibilityHint={`Double tap to ${action.title.toLowerCase()}`}
            accessibilityRole="button"
          >
            <Card variant="elevated" style={styles.actionCard}>
              <View style={[styles.iconContainer, { backgroundColor: action.color }]}>
                <Ionicons name={action.icon as any} size={20} color={theme.colors.textPrimary} />
              </View>
              <Text size="sm" weight="medium" color="textPrimary" style={styles.actionTitle}>
                {action.title}
              </Text>
            </Card>
          </AccessibilityWrapper>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: theme.spacing.md,
    marginBottom: theme.spacing.xl,
  },
  title: {
    marginBottom: theme.spacing.md,
  },
  actionsGrid: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  actionCard: {
    flex: 1,
    alignItems: 'center',
    padding: theme.spacing.md,
    minHeight: 80,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: theme.spacing.sm,
  },
  actionTitle: {
    textAlign: 'center',
  },
});

export default QuickActions;
