// hooks/useThemeColor.ts
import { useColorScheme } from './useColorScheme';
import Colors from '../constants/Colors';

type PaletteKey = keyof typeof Colors['dark'];

/**
 * Reads a palette key from Colors using the current color scheme.
 * If a color prop is passed in props, that wins.
 */
export function useThemeColor(
  props: { light?: string; dark?: string },
  colorName: PaletteKey
) {
  const theme = useColorScheme() ?? 'dark';
  if (props[theme]) {
    return props[theme]!;
  }
  const palette = Colors[theme];
  return palette[colorName] as string;
}
