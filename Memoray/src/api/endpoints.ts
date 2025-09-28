// src/api/endpoints.ts
import { Platform } from "react-native";
import Constants from "expo-constants";

function getHostFromExpo(): string | null {
  // Works for Expo dev: "192.168.x.x:8081" → "192.168.x.x"
  const uri = (Constants as any)?.expoConfig?.hostUri ?? (Constants as any)?.executionEnvironment;
  if (typeof uri === "string" && uri.includes(":")) return uri.split(":")[0];
  return null;
}

export function getApiBase(): string {
  // Allow explicit override
  if (process.env.EXPO_PUBLIC_API_BASE) return process.env.EXPO_PUBLIC_API_BASE;

  const host = getHostFromExpo();
  if (host) return `http://${host}:4000`;

  if (Platform.OS === "android") return "http://10.0.2.2:4000"; // Android emulator ↔ host
  if (Platform.OS === "ios") return "http://127.0.0.1:4000";    // iOS simulator
  return "http://localhost:4000";                               // web
}

export const API_BASE = getApiBase();
export const API = {
  relationships: `${API_BASE}/api/getRelationships`,
  food: `${API_BASE}/api/get_food`,
  car: `${API_BASE}/api/get_car`,
  home: `${API_BASE}/api/get_home`,
  landmarks: `${API_BASE}/api/get_landmarks`,
  photos: `${API_BASE}/api/get_photos`,
} as const;

export const CACHE_KEYS = {
  relationships: 'metasense.relationships.v1',
  food: 'metasense.food.v1',
  car: 'metasense.car.v1',
  home: 'metasense.home.v1',
  landmarks: 'metasense.landmarks.v1',
  photos: 'metasense.photos.v1',
} as const;
