// src/api/client.ts
import AsyncStorage from "@react-native-async-storage/async-storage";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export async function fetchJSON<T>(path: string): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10_000); // 10s timeout

  try {
    const response = await fetch(path, {
      signal: controller.signal,
      headers: { "Content-Type": "application/json" },
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new ApiError(`HTTP ${response.status}: ${response.statusText}`, response.status);
    }

    return (await response.json()) as T;
  } catch (err: unknown) {
    clearTimeout(timeoutId);

    // Re-throw our own ApiError unchanged
    if (err instanceof ApiError) {
      throw err;
    }

    // Abort/timeout handling (works whether DOMException exists or not)
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new ApiError("Request timeout", 408, "TIMEOUT");
    }

    const message = err instanceof Error ? err.message : "Unknown error";
    throw new ApiError(message, 0, "NETWORK_ERROR");
  }
}

// Cache utilities
export async function readCache<T>(key: string): Promise<T | null> {
  try {
    const stored = await AsyncStorage.getItem(key);
    return stored ? (JSON.parse(stored) as T) : null;
  } catch (err) {
    console.error(`Error reading cache for key ${key}:`, err);
    return null;
  }
}

export async function writeCache<T>(key: string, data: T): Promise<void> {
  try {
    await AsyncStorage.setItem(key, JSON.stringify(data));
  } catch (err) {
    console.error(`Error writing cache for key ${key}:`, err);
  }
}

export async function clearCache(key: string): Promise<void> {
  try {
    await AsyncStorage.removeItem(key);
  } catch (err) {
    console.error(`Error clearing cache for key ${key}:`, err);
  }
}
