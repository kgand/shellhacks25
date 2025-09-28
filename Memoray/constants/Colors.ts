// constants/Colors.ts
// Centralized, high-contrast dark palette with modern gradient + glassmorphism support

const purple = '#7A3EF5';
const purpleGlow = '#9B6CFF';
const bg = '#0B0E11';
const card = '#121418';

// Gradient backgrounds
const bgGradientStart = '#0A0C12';
const bgGradientEnd = '#0E111A';

// Glass surfaces
const glassSurface = 'rgba(255,255,255,0.08)';
const glassBorder = 'rgba(255,255,255,0.12)';

// Primary gradients
const primaryGradientStart = '#6366F1';
const primaryGradientEnd = '#A855F7';

// Domain-specific accents
const peopleAccent = '#22D3EE';      // Cyan
const zonesAccent = '#34D399';       // Emerald
const alertsAccent = '#F59E0B';      // Amber

const text = '#F2F4F7';
const textSecondary = '#C9CFD6';
const textMuted = '#8A93A3';

const border = '#23262D';

const success = '#22C55E';
const successBg = 'rgba(34,197,94,0.15)';  // green translucent
const successBorder = 'rgba(34,197,94,0.4)';

const danger = '#EF4444';
const warning = '#F59E0B';

export default {
  light: {
    text,
    textSecondary,
    textMuted,
    background: bg,
    card,
    tint: purple,
    tintGlow: purpleGlow,
    border,
    icon: textSecondary,

    // Gradient backgrounds
    backgroundGradientStart: bgGradientStart,
    backgroundGradientEnd: bgGradientEnd,
    
    // Glass surfaces
    glassSurface,
    glassBorder,
    
    // Primary gradients
    primaryGradientStart,
    primaryGradientEnd,
    
    // Domain-specific accents
    peopleAccent,
    zonesAccent,
    alertsAccent,

    success,
    successBg,
    successBorder,

    danger,
    warning,
  },
  dark: {
    text,
    textSecondary,
    textMuted,
    background: bg,
    card,
    tint: purple,
    tintGlow: purpleGlow,
    border,
    icon: textSecondary,

    // Gradient backgrounds
    backgroundGradientStart: bgGradientStart,
    backgroundGradientEnd: bgGradientEnd,
    
    // Glass surfaces
    glassSurface,
    glassBorder,
    
    // Primary gradients
    primaryGradientStart,
    primaryGradientEnd,
    
    // Domain-specific accents
    peopleAccent,
    zonesAccent,
    alertsAccent,

    success,
    successBg,
    successBorder,

    danger,
    warning,
  },
} as const;
