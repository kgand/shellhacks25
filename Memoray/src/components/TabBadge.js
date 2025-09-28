// src/components/TabBadge.js
import React, { useMemo } from 'react';
import { View, Text } from 'react-native';

/**
 * Resolve AlertsContext safely regardless of how it's exported:
 * - named export:   export const AlertsContext = createContext(...)
 * - default value:  export default AlertsProvider; export const AlertsContext = ...
 * - default ctx:    export default createContext(...)
 */
function resolveAlertsContext() {
  try {
    // Require dynamically to avoid import-time crashes if the module shape changes
    // or the file temporarily fails to load during fast refresh.
    // eslint-disable-next-line @typescript-eslint/no-var-requires, global-require
    const mod = require('../context/AlertsContext');

    // Common cases:
    if (mod?.AlertsContext) return mod.AlertsContext;    // named export
    if (mod?.default?.AlertsContext) return mod.default.AlertsContext; // nested on default
    if (mod?.default?._context || mod?._context) return mod.default || mod; // exported the context itself

    return null;
  } catch {
    return null;
  }
}

export default function TabBadge() {
  const AlertsContext = resolveAlertsContext();

  // If the context module isn't ready or isn't exported, just render nothing (no crash).
  const ctx = AlertsContext ? React.useContext(AlertsContext) : null;

  const count = useMemo(() => {
    try {
      if (!ctx) return 0;
      // support method or number field
      if (typeof ctx.getUnresolvedCount === 'function') {
        const n = ctx.getUnresolvedCount();
        return Number.isFinite(n) ? n : 0;
      }
      if (typeof ctx.unresolvedCount === 'number') {
        return ctx.unresolvedCount;
      }
      // support array of alerts with "resolved" field
      if (Array.isArray(ctx.alerts)) {
        return ctx.alerts.filter(a => !a?.resolved).length;
      }
      return 0;
    } catch {
      return 0;
    }
  }, [ctx]);

  if (!count) return null;

  return (
    <View
      style={{
        minWidth: 18,
        height: 18,
        borderRadius: 9,
        paddingHorizontal: 5,
        backgroundColor: '#7A3EF5',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      accessibilityLabel={`${count} unresolved alerts`}
      accessibilityRole="text"
    >
      <Text style={{ color: 'white', fontSize: 12, fontWeight: '700' }}>{count}</Text>
    </View>
  );
}
