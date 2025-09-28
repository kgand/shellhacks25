import { useEffect, useState } from 'react';
import * as SplashScreen from 'expo-splash-screen';
import * as Font from 'expo-font';

// Keep the splash screen visible while we fetch resources
SplashScreen.preventAutoHideAsync();

interface UseSplashGateOptions {
  fonts?: { [key: string]: any };
  minDuration?: number;
  onAuthReady?: () => Promise<boolean>;
}

export const useSplashGate = (options: UseSplashGateOptions = {}) => {
  const { fonts = {}, minDuration = 2000, onAuthReady } = options;
  const [isReady, setIsReady] = useState(false);
  const [startTime] = useState(Date.now());

  useEffect(() => {
    const prepare = async () => {
      try {
        // Load fonts
        if (Object.keys(fonts).length > 0) {
          await Font.loadAsync(fonts);
        }

        // Check auth status if provided
        if (onAuthReady) {
          await onAuthReady();
        }

        // Ensure minimum duration
        const elapsed = Date.now() - startTime;
        const remaining = Math.max(0, minDuration - elapsed);
        
        if (remaining > 0) {
          await new Promise(resolve => setTimeout(resolve, remaining));
        }

        setIsReady(true);
      } catch (error) {
        console.warn('Error preparing app:', error);
        setIsReady(true);
      } finally {
        // Hide the splash screen
        await SplashScreen.hideAsync();
      }
    };

    prepare();
  }, [fonts, minDuration, onAuthReady, startTime]);

  return { isReady };
};
