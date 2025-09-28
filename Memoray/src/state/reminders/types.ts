export type Audience = 'caregiver' | 'patient' | 'both';
export type ScheduleType = 'time' | 'interval';

export interface Reminder {
  id: string;
  label: string;
  audience: Audience;
  scheduleType: ScheduleType;      // <-- union, not string
  time?: string;                   // when scheduleType === 'time'
  intervalMinutes?: number;        // when scheduleType === 'interval'
  icon?: string;
  notes?: string;
}

export interface RemindersContextType {
  reminders: Reminder[];
  addReminder: (data: Omit<Reminder, 'id'>) => Promise<void> | void;
  updateReminder: (id: string, patch: Partial<Reminder>) => Promise<void> | void;
  removeReminder: (id: string) => Promise<void> | void;
}

// Helper function to normalize scheduleType from string to union type
export const toScheduleType = (s: string): ScheduleType =>
  s === 'interval' ? 'interval' : 'time';

// Helper function to normalize a reminder object
export const normalizeReminder = (r: any): Reminder => ({
  ...r,
  scheduleType: toScheduleType(r.scheduleType),
  audience: r.audience || 'patient',
  icon: r.icon || '💊',
});