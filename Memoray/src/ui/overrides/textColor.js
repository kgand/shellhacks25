// src/ui/overrides/textColor.js
import React from 'react';
import { Text as RNText } from 'react-native';

// Keep original render
const _render = RNText.render || RNText.prototype.render;

// Soft default text color (will NOT override an explicit style.color)
RNText.render = function render(...args) {
  const origin = _render.call(this, ...args);
  if (!origin) return origin;

  // If the child already has a color, keep it. Otherwise apply our default.
  const baseStyle = Array.isArray(origin.props.style)
    ? origin.props.style
    : [origin.props.style].filter(Boolean);

  const alreadyHasColor = baseStyle.some(
    s => s && typeof s === 'object' && s.color
  );

  return React.cloneElement(origin, {
    style: alreadyHasColor
      ? baseStyle
      : [{ color: '#C9CFD6' }, ...baseStyle],
  });
};
