// src/lib/api.ts
import { Platform } from 'react-native';
import Constants from 'expo-constants';
import * as SecureStore from 'expo-secure-store';
import { getRandomBytesAsync } from 'expo-crypto';

// Types
export interface ApiError extends Error {
  status?: number;
  code?: 'NETWORK' | 'TIMEOUT' | 'HTTP_4xx' | 'HTTP_5xx' | 'PARSE' | 'AUTH';
}

export interface ApiRequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  headers?: Record<string, string>;
  body?: any;
  timeout?: number;
  retries?: number;
  signal?: AbortSignal;
}

export interface ApiResponse<T = any> {
  data: T;
  status: number;
  headers: Headers;
}

// Platform-aware base URL configuration
function getApiBaseUrl(): string {
  // Allow explicit override via environment variable
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL;
  }

  // Get the development server host from Expo
  const hostUri = Constants.expoConfig?.hostUri;
  if (hostUri) {
    const [host] = hostUri.split(':');
    return `http://${host}:4000`;
  }

  // Platform-specific defaults
  switch (Platform.OS) {
    case 'android':
      return 'http://10.0.2.2:4000'; // Android emulator
    case 'ios':
      return 'http://localhost:4000'; // iOS simulator
    default:
      return 'http://localhost:4000'; // Web
  }
}

// Central logger
class ApiLogger {
  private static log(level: 'info' | 'warn' | 'error', message: string, data?: any) {
    const timestamp = new Date().toISOString();
    const logMessage = `[API ${level.toUpperCase()}] ${timestamp}: ${message}`;
    
    if (__DEV__) {
      console[level](logMessage, data || '');
      
      // Show toast in development for errors
      if (level === 'error' && typeof window !== 'undefined') {
        // Toast implementation would go here if needed
      }
    } else {
      // In production, only log errors
      if (level === 'error') {
        console.error(logMessage, data || '');
      }
    }
  }

  static info(message: string, data?: any) {
    this.log('info', message, data);
  }

  static warn(message: string, data?: any) {
    this.log('warn', message, data);
  }

  static error(message: string, data?: any) {
    this.log('error', message, data);
  }
}

// Generate random jitter for retry delays
async function getJitteredDelay(baseMs: number): Promise<number> {
  const jitter = await getRandomBytesAsync(1);
  const jitterFactor = jitter[0] / 255; // 0-1
  return baseMs + (jitterFactor * 600); // Add 0-600ms jitter
}

// Main API client class
export class ApiClient {
  private baseUrl: string;
  private defaultTimeout: number;
  private defaultRetries: number;

  constructor() {
    this.baseUrl = getApiBaseUrl();
    this.defaultTimeout = 10000; // 10 seconds
    this.defaultRetries = 3;
    
    ApiLogger.info(`API Client initialized with base URL: ${this.baseUrl}`);
  }

  // Get authentication token from SecureStore
  private async getAuthToken(): Promise<string | null> {
    try {
      return await SecureStore.getItemAsync('auth_token');
    } catch (error) {
      ApiLogger.warn('Failed to retrieve auth token', error);
      return null;
    }
  }

  // Handle 401 responses - refresh token or sign out
  private async handleAuthError(): Promise<void> {
    ApiLogger.warn('Authentication error - clearing token');
    try {
      await SecureStore.deleteItemAsync('auth_token');
      // In a real app, you might want to trigger a sign-out flow here
    } catch (error) {
      ApiLogger.error('Failed to clear auth token', error);
    }
  }

  // Create error with proper typing
  private createError(message: string, status?: number, code?: ApiError['code']): ApiError {
    const error = new Error(message) as ApiError;
    error.status = status;
    error.code = code;
    return error;
  }

  // Main request method with retry logic
  async request<T = any>(
    endpoint: string,
    options: ApiRequestOptions = {}
  ): Promise<ApiResponse<T>> {
    const {
      method = 'GET',
      headers = {},
      body,
      timeout = this.defaultTimeout,
      retries = this.defaultRetries,
      signal
    } = options;

    const url = `${this.baseUrl}${endpoint}`;
    const requestId = Math.random().toString(36).substring(7);
    
    ApiLogger.info(`[${requestId}] ${method} ${url}`, { headers, body });

    // Add authentication header if available
    const authToken = await this.getAuthToken();
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`;
    }

    // Set content type for JSON bodies
    if (body && typeof body === 'object') {
      headers['Content-Type'] = 'application/json';
    }

    let lastError: ApiError | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      // Combine abort signals if provided
      if (signal) {
        signal.addEventListener('abort', () => controller.abort());
      }

      try {
        const response = await fetch(url, {
          method,
          headers,
          body: body ? JSON.stringify(body) : undefined,
          signal: controller.signal,
        });

        clearTimeout(timeoutId);

        // Handle authentication errors
        if (response.status === 401) {
          await this.handleAuthError();
          throw this.createError('Authentication required', 401, 'AUTH');
        }

        // Handle HTTP errors
        if (!response.ok) {
          const errorCode = response.status >= 500 ? 'HTTP_5xx' : 'HTTP_4xx';
          throw this.createError(
            `HTTP ${response.status}: ${response.statusText}`,
            response.status,
            errorCode
          );
        }

        // Parse JSON response
        let data: T;
        try {
          data = await response.json();
        } catch (parseError) {
          throw this.createError('Failed to parse JSON response', response.status, 'PARSE');
        }

        ApiLogger.info(`[${requestId}] Success (${response.status})`, { data });

        return {
          data,
          status: response.status,
          headers: response.headers,
        };

      } catch (error) {
        clearTimeout(timeoutId);
        lastError = error as ApiError;

        // Determine error type
        if (error instanceof DOMException && error.name === 'AbortError') {
          lastError = this.createError('Request timeout', 408, 'TIMEOUT');
        } else if (error instanceof TypeError && error.message.includes('fetch')) {
          lastError = this.createError('Network error', 0, 'NETWORK');
        }

        ApiLogger.error(`[${requestId}] Attempt ${attempt + 1} failed`, {
          error: lastError.message,
          code: lastError.code,
          status: lastError.status,
        });

        // Don't retry on certain errors
        if (lastError.code === 'AUTH' || lastError.code === 'HTTP_4xx') {
          break;
        }

        // Add delay before retry (except on last attempt)
        if (attempt < retries) {
          const delay = await getJitteredDelay(200);
          ApiLogger.info(`[${requestId}] Retrying in ${delay}ms...`);
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }

    // All retries failed
    ApiLogger.error(`[${requestId}] All retries failed`, {
      error: lastError?.message,
      code: lastError?.code,
      status: lastError?.status,
    });

    throw lastError || this.createError('Request failed after all retries', 0, 'NETWORK');
  }

  // Convenience methods
  async get<T = any>(endpoint: string, options?: Omit<ApiRequestOptions, 'method'>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T = any>(endpoint: string, body?: any, options?: Omit<ApiRequestOptions, 'method' | 'body'>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'POST', body });
  }

  async put<T = any>(endpoint: string, body?: any, options?: Omit<ApiRequestOptions, 'method' | 'body'>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'PUT', body });
  }

  async delete<T = any>(endpoint: string, options?: Omit<ApiRequestOptions, 'method'>): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }

  // Revalidation method for retry buttons
  async revalidate(): Promise<void> {
    ApiLogger.info('Revalidating API connection...');
    try {
      await this.get('/health');
      ApiLogger.info('API connection revalidated successfully');
    } catch (error) {
      ApiLogger.error('API revalidation failed', error);
      throw error;
    }
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export types and utilities
export { ApiLogger };
export const API_BASE_URL = getApiBaseUrl();
