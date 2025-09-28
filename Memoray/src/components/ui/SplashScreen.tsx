import React, { useEffect, useState } from 'react';
import { View, StyleSheet, Animated, Dimensions } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Text } from '../ui/overrides/base';
import { theme } from '../../utils/theme';

const { width, height } = Dimensions.get('window');

interface SplashScreenProps {
  onFinish: () => void;
  duration?: number;
}

const SplashScreen: React.FC<SplashScreenProps> = ({ 
  onFinish, 
  duration = 2500 
}) => {
  const [fadeAnim] = useState(new Animated.Value(0));
  const [scaleAnim] = useState(new Animated.Value(0.8));
  const [logoOpacity] = useState(new Animated.Value(0));

  useEffect(() => {
    // Entrance animation sequence
    Animated.sequence([
      // Logo fade in
      Animated.timing(logoOpacity, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      // Scale up
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      // Hold for a moment
      Animated.delay(800),
      // Fade out
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 500,
        useNativeDriver: true,
      }),
    ]).start(() => {
      onFinish();
    });
  }, [fadeAnim, scaleAnim, logoOpacity, onFinish]);

  return (
    <Animated.View 
      style={[
        styles.container,
        {
          opacity: fadeAnim.interpolate({
            inputRange: [0, 1],
            outputRange: [1, 0],
          }),
        },
      ]}
    >
      <LinearGradient
        colors={['#0F1113', '#1A1D1F', '#2A2E33']}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <Animated.View
          style={[
            styles.logoContainer,
            {
              opacity: logoOpacity,
              transform: [{ scale: scaleAnim }],
            },
          ]}
        >
          {/* Memoray Logo */}
          <View style={styles.logo}>
            <Text style={styles.logoText}>Memoray</Text>
            <View style={styles.logoAccent} />
          </View>
          
          {/* Tagline */}
          <Animated.View
            style={[
              styles.taglineContainer,
              {
                opacity: logoOpacity,
              },
            ]}
          >
            <Text style={styles.tagline}>
              Memory assistance for everyday life
            </Text>
          </Animated.View>
        </Animated.View>

        {/* Subtle animated dots */}
        <View style={styles.dotsContainer}>
          {[0, 1, 2].map((index) => (
            <Animated.View
              key={index}
              style={[
                styles.dot,
                {
                  opacity: logoOpacity,
                  transform: [
                    {
                      scale: logoOpacity.interpolate({
                        inputRange: [0, 1],
                        outputRange: [0.5, 1],
                      }),
                    },
                  ],
                },
              ]}
            />
          ))}
        </View>
      </LinearGradient>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 9999,
  },
  gradient: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo: {
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  logoText: {
    fontSize: 48,
    fontWeight: '700',
    color: theme.colors.textPrimary,
    letterSpacing: 2,
    textAlign: 'center',
  },
  logoAccent: {
    width: 60,
    height: 3,
    backgroundColor: theme.colors.accent,
    marginTop: theme.spacing.sm,
    borderRadius: 2,
  },
  taglineContainer: {
    marginTop: theme.spacing.md,
  },
  tagline: {
    fontSize: 16,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    fontWeight: '400',
    letterSpacing: 0.5,
  },
  dotsContainer: {
    position: 'absolute',
    bottom: 100,
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.colors.accent,
  },
});

export default SplashScreen;
