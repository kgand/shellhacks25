# Network Fix Summary: "Failed to fetch" Resolution

## Overview
Fixed "Failed to fetch" errors in Memoray app by implementing a robust API client with retry logic, platform-aware base URLs, and comprehensive error handling.

## Changes Made

### 1. New API Client (`src/lib/api.ts`)
- **Platform-aware base URL**: Automatically detects iOS simulator, Android emulator, and physical devices
- **Retry logic**: 3 retries with exponential backoff and jitter (200-800ms)
- **Timeout handling**: 10-second timeout with AbortController
- **Authentication**: Automatic token injection from SecureStore
- **Error classification**: NETWORK, TIMEOUT, HTTP_4xx, HTTP_5xx, AUTH, PARSE
- **Central logging**: Request/response logging with request IDs

### 2. Environment Configuration
- **`.env.example`**: Added environment variable examples
- **`app.json`**: Added Android cleartext traffic and iOS ATS exceptions for development
- **Platform-specific URLs**: 
  - iOS Simulator: `http://localhost:4000`
  - Android Emulator: `http://10.0.2.2:4000`
  - Physical Device: `http://<LAN_IP>:4000`

### 3. Hook Refactoring (`src/hooks/useThingsIKnow.ts`)
- **New API client integration**: Replaced `fetchJSON` with `apiClient.get`
- **Unmount protection**: Added `isMountedRef` to prevent setState after unmount
- **Enhanced error handling**: User-friendly error messages based on error type
- **Retry functionality**: `refetch` now calls `apiClient.revalidate()` first

### 4. Error Handling Improvements
- **Network errors**: "Network error - check your connection"
- **Timeout errors**: "Request timeout - please try again"
- **Server errors**: "Server error - please try again later"
- **Authentication errors**: Automatic token cleanup and sign-out flow

## Key Features

### Retry Logic
```typescript
// 3 retries with jittered delays
for (let attempt = 0; attempt <= retries; attempt++) {
  try {
    // Make request
  } catch (error) {
    if (attempt < retries) {
      const delay = await getJitteredDelay(200); // 200-800ms
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Platform Detection
```typescript
function getApiBaseUrl(): string {
  if (process.env.EXPO_PUBLIC_API_URL) return process.env.EXPO_PUBLIC_API_URL;
  
  const hostUri = Constants.expoConfig?.hostUri;
  if (hostUri) {
    const [host] = hostUri.split(':');
    return `http://${host}:4000`;
  }
  
  switch (Platform.OS) {
    case 'android': return 'http://10.0.2.2:4000';
    case 'ios': return 'http://localhost:4000';
    default: return 'http://localhost:4000';
  }
}
```

### Error Classification
```typescript
export interface ApiError extends Error {
  status?: number;
  code?: 'NETWORK' | 'TIMEOUT' | 'HTTP_4xx' | 'HTTP_5xx' | 'PARSE' | 'AUTH';
}
```

## Testing Instructions

### 1. iOS Simulator
```bash
npm run ios
```
- Should connect to `http://localhost:4000`
- Check console for API logs

### 2. Android Emulator
```bash
npm run android
```
- Should connect to `http://10.0.2.2:4000`
- Check console for API logs

### 3. Physical Device
```bash
npm start
# Scan QR code with Expo Go
```
- Should connect to `http://<YOUR_LAN_IP>:4000`
- Ensure device and computer are on same network

## Verification Checklist

- [ ] Dashboard loads without "Failed to fetch" error
- [ ] People screen loads without "Failed to load people" error
- [ ] Retry buttons work correctly
- [ ] Network errors show user-friendly messages
- [ ] Offline mode shows appropriate messages
- [ ] No setState after unmount warnings
- [ ] Console shows detailed API request logs

## Environment Variables

Create `.env` file:
```bash
# Development
EXPO_PUBLIC_API_URL=http://localhost:4000

# Production
# EXPO_PUBLIC_API_URL=https://api.memoray.com
```

## CORS Configuration

If using Next.js API routes, add CORS middleware:
```javascript
// pages/api/_middleware.js
import Cors from 'cors';

const cors = Cors({
  origin: [
    'http://localhost:8081', // Expo dev server
    'http://10.0.2.2:8081',  // Android emulator
    'exp://192.168.x.x:8081' // Physical device
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  credentials: true
});
```

## Commit Message
```
fix(network): stabilize fetch for Dashboard/People with retry, timeout, env-aware baseURL

- Add robust API client with 3-retry logic and jittered backoff
- Implement platform-aware base URL detection (iOS/Android/Device)
- Add comprehensive error handling with user-friendly messages
- Prevent setState after unmount with isMountedRef
- Add central logging with request IDs for debugging
- Configure Android cleartext and iOS ATS for development
- Update useThingsIKnow hooks to use new API client
- Add environment variable examples and documentation
```

## Files Modified
- `src/lib/api.ts` (new)
- `src/hooks/useThingsIKnow.ts`
- `app.json`
- `env.example` (new)
- `NETWORK_FIX_SUMMARY.md` (new)
