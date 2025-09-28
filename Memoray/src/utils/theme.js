// src/utils/theme.js
const palette = {
  // Uber-style charcoal palette
  background: '#0F1113',           // App root (darker for better contrast)
  surface: '#1A1D1F',              // Cards
  surfaceAlt: '#232629',           // Alternative surfaces
  border: '#2C3136',               // Borders
  
  // New Uber-like card colors
  pageBg: '#0F1113',               // Page background
  cardBg: '#1B1E22',               // Card background
  cardBorder: '#2A2E33',           // Card border
  
  // Text colors
  textPrimary: '#FFFFFF',          // Primary text
  textSecondary: '#B5BAC1',        // Secondary text (lighter for better contrast)
  textTertiary: '#8A9099',         // Tertiary text (muted)
  
  // Accent colors
  accent: '#6E7CF6',               // Blue accent
  tabInactive: '#7C838C',          // Inactive tab color
  
  // Input colors
  inputBg: '#171A1D',              // Input background
  inputBorder: '#2C3136',          // Input border
  
  // Status colors
  success: '#2EE98A',
  warning: '#F59E0B',
  error: '#EF4444',
};

const fontSizes = {
  xs: 12,
  sm: 14,
  md: 16,
  lg: 18,
  xl: 20,
  '2xl': 24,
  '3xl': 28,
  '4xl': 32,
  '5xl': 36,
};

const fontWeights = {
  light: '300',
  regular: '400',
  medium: '500',
  semibold: '600',
  bold: '700',
  extrabold: '800',
};

export const theme = {
  colors: {
    // Backgrounds
    background: palette.background,
    surface: palette.surface,
    surfaceAlt: palette.surfaceAlt,
    border: palette.border,
    
    // New Uber-like colors
    pageBg: palette.pageBg,
    cardBg: palette.cardBg,
    cardBorder: palette.cardBorder,
    
    // Text colors
    textPrimary: palette.textPrimary,
    textSecondary: palette.textSecondary,
    textTertiary: palette.textTertiary,
    
    // Accent colors
    accent: palette.accent,
    tabInactive: palette.tabInactive,
    
    // Input colors
    inputBg: palette.inputBg,
    inputBorder: palette.inputBorder,
    
    // Status colors
    success: palette.success,
    warning: palette.warning,
    error: palette.error,

    // Navigation
    navBg: palette.background,
    navBorder: palette.border,
    navActive: palette.textPrimary,
    navInactive: palette.tabInactive,
    headerBg: palette.background,
    headerText: palette.textPrimary,
  },

  fonts: {
    regular: { 
      fontFamily: 'Inter-Regular', 
      fontWeight: fontWeights.regular,
      letterSpacing: 0.1,
    },
    semibold: { 
      fontFamily: 'Inter-SemiBold', 
      fontWeight: fontWeights.semibold,
      letterSpacing: 0.1,
    },
    bold: { 
      fontFamily: 'Inter-Bold', 
      fontWeight: fontWeights.bold,
      letterSpacing: 0.2,
    },
    sizes: fontSizes,
    weights: fontWeights,
  },

  spacing: { 
    xs: 4, 
    sm: 8, 
    md: 12, 
    lg: 16, 
    xl: 20, 
    '2xl': 24, 
    '3xl': 32,
    '4xl': 40,
    '5xl': 48,
    '6xl': 64
  },
  
  radii: { 
    sm: 8, 
    md: 12, 
    lg: 16, 
    xl: 20, 
    round: 999 
  },

  shadows: {
    subtle: {
      shadowColor: 'rgba(0,0,0,0.1)',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 1,
    },
    medium: {
      shadowColor: 'rgba(0,0,0,0.15)',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.15,
      shadowRadius: 4,
      elevation: 3,
    },
    large: {
      shadowColor: 'rgba(0,0,0,0.2)',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.2,
      shadowRadius: 8,
      elevation: 6,
    },
    glow: {
      shadowColor: palette.accent,
      shadowOffset: { width: 0, height: 0 },
      shadowOpacity: 0.3,
      shadowRadius: 8,
      elevation: 4,
    },
  },
};

// Convenience helpers
export const color = (key) => theme.colors[key] ?? key;
export const fontSize = (key, fallback = 15) => fontSizes[key] ?? fallback;
export const shadow = (key) => theme.shadows[key];
export const spacing = (key) => theme.spacing[key];
export const radius = (key) => theme.radii[key];
