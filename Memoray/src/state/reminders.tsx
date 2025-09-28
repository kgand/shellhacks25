// src/state/reminders.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import {
  getAllReminders,
  setReminders,
  addReminder as storageAdd,
  updateReminder as storageUpdate,
  deleteReminder as storageDelete,
} from '../utils/remindersStorage';
import type { Reminder } from './reminders/types';

interface RemindersContextType {
  items: Reminder[];
  loading: boolean;
  addReminder: (reminder: Omit<Reminder, 'id'>) => Promise<Reminder>;
  updateReminder: (id: string, updates: Partial<Omit<Reminder, 'id'>>) => Promise<void>;
  removeReminder: (id: string) => Promise<void>;
  refreshReminders: () => Promise<void>;
}

const RemindersContext = createContext<RemindersContextType | undefined>(undefined);

export const useReminders = () => {
  const ctx = useContext(RemindersContext);
  if (!ctx) throw new Error('useReminders must be used within a RemindersProvider');
  return ctx;
};

interface RemindersProviderProps { children: ReactNode; }

export const RemindersProvider: React.FC<RemindersProviderProps> = ({ children }) => {
  const [items, setItems] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);

  const refreshReminders = async () => {
    setLoading(true);
    try {
      const loaded = await getAllReminders();
      setItems(loaded);
    } catch (e) {
      console.error('Error loading reminders:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { refreshReminders(); }, []);

  const addReminder = async (reminder: Omit<Reminder, 'id'>): Promise<Reminder> => {
    const created = await storageAdd(reminder);
    // optimistic insert + persist (storageAdd already persisted; this keeps state in sync)
    setItems(prev => [created, ...prev]);
    return created;
  };

  const updateReminder = async (id: string, updates: Partial<Omit<Reminder, 'id'>>) => {
    await storageUpdate(id, updates);
    setItems(prev => prev.map(r => (r.id === id ? { ...r, ...updates } : r)));
  };

  const removeReminder = async (id: string) => {
    // OPTIMISTIC: compute next list from current state, set it, then persist.
    // Use functional update to avoid stale closures.
    let snapshot: Reminder[] = [];
    setItems(prev => {
      snapshot = prev; // keep for rollback if needed
      const next = prev.filter(r => r.id !== id);
      // Fire-and-forget persistence (best-effort); we still call storageDelete below.
      setReminders(next).catch(err => console.error('persist after delete failed', err));
      return next;
    });

    try {
      // Also run storage delete for compatibility with any other readers of AsyncStorage.
      await storageDelete(id);
    } catch (e) {
      console.error('Error deleting reminder (rolling back):', e);
      // Rollback if persistence failed
      setItems(snapshot);
    }
  };

  const value: RemindersContextType = {
    items,
    loading,
    addReminder,
    updateReminder,
    removeReminder,
    refreshReminders,
  };

  return <RemindersContext.Provider value={value}>{children}</RemindersContext.Provider>;
};
