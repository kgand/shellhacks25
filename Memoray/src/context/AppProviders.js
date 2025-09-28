// src/context/AppProviders.js
import React from 'react';

// make sure these named exports exist in each file:
import { AuthProvider } from './AuthContext';
import { PeopleProvider } from './PeopleContext';
import { SafeZonesProvider } from './SafeZonesContext';
import { AlertsProvider } from './AlertsContext';
import { RemindersProvider } from '../state/reminders';

export default function AppProviders({ children }) {
  return (
    <AuthProvider>
      <PeopleProvider>
        <SafeZonesProvider>
          <AlertsProvider>
            <RemindersProvider>{children}</RemindersProvider>
          </AlertsProvider>
        </SafeZonesProvider>
      </PeopleProvider>
    </AuthProvider>
  );
}
