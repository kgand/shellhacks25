// src/utils/__tests__/remindersStorage.test.ts
import { loadReminders, saveReminders, addReminder, deleteReminder, Reminder } from '../remindersStorage';

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () => ({
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
}));

// Mock expo-crypto
jest.mock('expo-crypto', () => ({
  randomUUID: jest.fn(() => 'test-uuid-123'),
}));

describe('remindersStorage', () => {
  const AsyncStorage = require('@react-native-async-storage/async-storage');
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('loadReminders', () => {
    it('should return empty array when no data in AsyncStorage', async () => {
      AsyncStorage.getItem.mockResolvedValue(null);
      const result = await loadReminders();
      expect(result).toEqual([]);
    });

    it('should return parsed reminders from AsyncStorage', async () => {
      const mockReminders: Reminder[] = [
        { id: '1', icon: '💊', label: 'Take medicine', scheduleType: 'time', time: '8:00', audience: 'patient' },
      ];
      AsyncStorage.getItem.mockResolvedValue(JSON.stringify(mockReminders));
      const result = await loadReminders();
      expect(result).toEqual(mockReminders);
    });

    it('should return empty array on parse error', async () => {
      AsyncStorage.getItem.mockResolvedValue('invalid json');
      const result = await loadReminders();
      expect(result).toEqual([]);
    });
  });

  describe('saveReminders', () => {
    it('should save reminders to AsyncStorage', async () => {
      const reminders: Reminder[] = [
        { id: '1', icon: '💊', label: 'Take medicine', scheduleType: 'time', time: '8:00', audience: 'patient' },
      ];
      await saveReminders(reminders);
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        '@daily_reminders',
        JSON.stringify(reminders)
      );
    });
  });

  describe('addReminder', () => {
    it('should add new reminder to the beginning of the list', async () => {
      const existingReminders: Reminder[] = [
        { id: '1', icon: '💊', label: 'Take medicine', scheduleType: 'time', time: '8:00', audience: 'patient' },
      ];
      AsyncStorage.getItem.mockResolvedValue(JSON.stringify(existingReminders));
      
      const newReminder = await addReminder({ icon: '🚰', label: 'Drink water', scheduleType: 'interval', intervalMinutes: 120, audience: 'patient' });
      
      expect(newReminder.id).toBe('test-uuid-123');
      expect(newReminder.icon).toBe('🚰');
      expect(newReminder.label).toBe('Drink water');
      expect(AsyncStorage.setItem).toHaveBeenCalled();
    });
  });

  describe('deleteReminder', () => {
    it('should remove reminder with given id', async () => {
      const reminders: Reminder[] = [
        { id: '1', icon: '💊', label: 'Take medicine', scheduleType: 'time', time: '8:00', audience: 'patient' },
        { id: '2', icon: '🚰', label: 'Drink water', scheduleType: 'interval', intervalMinutes: 120, audience: 'patient' },
      ];
      AsyncStorage.getItem.mockResolvedValue(JSON.stringify(reminders));
      
      await deleteReminder('1');
      
      expect(AsyncStorage.setItem).toHaveBeenCalledWith(
        '@daily_reminders',
        JSON.stringify([{ id: '2', icon: '🚰', label: 'Drink water', scheduleType: 'interval', intervalMinutes: 120, audience: 'patient' }])
      );
    });
  });
});
