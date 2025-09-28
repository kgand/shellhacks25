// src/utils/remindersStorage.ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Crypto from 'expo-crypto';
import type { Reminder } from '../state/reminders/types';

const STORAGE_KEY = '@daily_reminders';

async function read(): Promise<Reminder[]> {
  try {
    const raw = await AsyncStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Reminder[]) : [];
  } catch (e) {
    console.error('remindersStorage.read error', e);
    return [];
  }
}

async function write(list: Reminder[]): Promise<void> {
  try {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  } catch (e) {
    console.error('remindersStorage.write error', e);
  }
}

export async function getAllReminders(): Promise<Reminder[]> {
  return read();
}

export async function setReminders(list: Reminder[]): Promise<void> {
  return write(list);
}

export async function addReminder(reminder: Omit<Reminder, 'id'>): Promise<Reminder> {
  const newReminder: Reminder = { 
    ...reminder, 
    id: (Crypto as any).randomUUID?.() ?? String(Date.now()),
    // Normalize scheduleType to ensure it's a valid union type
    scheduleType: reminder.scheduleType === 'interval' ? 'interval' : 'time'
  };
  const list = await read();
  const next = [newReminder, ...list];
  await write(next);
  return newReminder;
}

export async function updateReminder(id: string, updates: Partial<Omit<Reminder, 'id'>>): Promise<Reminder | null> {
  const list = await read();
  const idx = list.findIndex(r => r.id === id);
  if (idx === -1) return null;
  const updated: Reminder = { 
    ...list[idx], 
    ...updates,
    // Normalize scheduleType if it's being updated
    scheduleType: updates.scheduleType === 'interval' ? 'interval' : 'time'
  };
  const next = [...list];
  next[idx] = updated;
  await write(next);
  return updated;
}

export async function deleteReminder(id: string): Promise<void> {
  const list = await read();
  const next = list.filter(r => r.id !== id);
  await write(next);
}

// Legacy aliases (if other code imports these names)
export const loadReminders = getAllReminders;
export const saveReminders = setReminders;

// Re-export the Reminder type for backward compatibility
export type { Reminder } from '../state/reminders/types';
