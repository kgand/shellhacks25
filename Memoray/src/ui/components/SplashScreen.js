// src/ui/components/SplashScreen.js
import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { theme } from '../../utils/theme';

const SplashScreen = () => {
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const letterAnims = useRef(
    Array.from({ length: 9 }, () => ({
      translateX: new Animated.Value(0),
      translateY: new Animated.Value(0),
      opacity: new Animated.Value(1),
    }))
  ).current;

  useEffect(() => {
    // Show full word for 400ms, then start disperse animation
    const timer = setTimeout(() => {
      // Create staggered animation for each letter
      const animations = letterAnims.map((letterAnim, index) => {
        const delay = index * 40; // 40ms stagger between letters
        
        return Animated.parallel([
          Animated.timing(letterAnim.translateX, {
            toValue: (index - 4) * 8, // Spread horizontally around center
            duration: 1400,
            delay,
            useNativeDriver: true,
          }),
          Animated.timing(letterAnim.translateY, {
            toValue: -6, // Slight upward movement
            duration: 1400,
            delay,
            useNativeDriver: true,
          }),
          Animated.timing(letterAnim.opacity, {
            toValue: 0.85, // Fade to 85% opacity
            duration: 1400,
            delay,
            useNativeDriver: true,
          }),
        ]);
      });

      Animated.parallel(animations).start();
    }, 400);

    return () => clearTimeout(timer);
  }, []);

  const letters = 'MetaSense'.split('');

  return (
    <View style={styles.container}>
      <Animated.View style={styles.wordContainer}>
        {letters.map((letter, index) => (
          <Animated.Text
            key={index}
            style={[
              styles.letter,
              {
                transform: [
                  { translateX: letterAnims[index].translateX },
                  { translateY: letterAnims[index].translateY },
                ],
                opacity: letterAnims[index].opacity,
              },
            ]}
          >
            {letter}
          </Animated.Text>
        ))}
      </Animated.View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  wordContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  letter: {
    fontSize: 30,
    fontWeight: '600',
    color: theme.colors.textPrimary,
    fontFamily: 'Inter-SemiBold',
    letterSpacing: 0.2,
  },
});

export default SplashScreen;
