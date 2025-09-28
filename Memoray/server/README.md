# MetaSense Server

Express server with Firestore integration for the MetaSense app.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up Firebase credentials:

Option A - Service Account JSON (recommended):
```bash
export FIREBASE_SERVICE_ACCOUNT_JSON='{"type":"service_account","project_id":"shellhacks25-f7a64",...}'
```

Option B - Application Default Credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

3. Start the server:
```bash
npm run dev:server
```

The server will start on port 4000 (or PORT environment variable).

## Endpoints

- `GET /health` - Health check
- `GET /api/getRelationships` - Get all relationships
- `GET /api/get_food` - Get food highlights
- `GET /api/get_car` - Get car highlights  
- `GET /api/get_home` - Get home highlights
- `GET /api/get_landmarks` - Get landmark highlights
- `GET /api/get_photos` - Get photo highlights

## Firestore Collections

- `relationships` - People and their relationships
- `highlights` - Photos organized by type (food, car, home, landmark, photo)

## Environment Variables

- `PORT` - Server port (default: 4000)
- `FIREBASE_SERVICE_ACCOUNT_JSON` - Firebase service account JSON string
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to service account key file
