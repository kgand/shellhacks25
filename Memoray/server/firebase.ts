// server/firebase.ts
import path from "node:path";
import fs from "node:fs";
import { config } from "dotenv";
config({ path: path.resolve(process.cwd(), "server", ".env") });

import admin from "firebase-admin";

// Normalize GOOGLE_APPLICATION_CREDENTIALS to an absolute path if present
if (process.env.GOOGLE_APPLICATION_CREDENTIALS && !path.isAbsolute(process.env.GOOGLE_APPLICATION_CREDENTIALS)) {
  const abs = path.resolve(process.cwd(), process.env.GOOGLE_APPLICATION_CREDENTIALS);
  process.env.GOOGLE_APPLICATION_CREDENTIALS = abs;
}

function init() {
  // Prefer inline JSON
  const inline = process.env.FIREBASE_SERVICE_ACCOUNT_JSON;
  const adcPath = process.env.GOOGLE_APPLICATION_CREDENTIALS;

  if (inline) {
    const sa = JSON.parse(inline);
    admin.initializeApp({ credential: admin.credential.cert(sa) });
    console.log("Firebase Admin initialized with inline service account JSON. project_id:", sa.project_id);
    return admin.firestore();
  }

  if (adcPath) {
    if (!fs.existsSync(adcPath)) {
      throw new Error(`GOOGLE_APPLICATION_CREDENTIALS file not found at: ${adcPath}`);
    }
    admin.initializeApp(); // ADC will read the file
    console.log("Firebase Admin initialized with ADC file:", adcPath);
    return admin.firestore();
  }

  // Last resort (dev only)
  console.warn("No Firebase credentials found. Using applicationDefault() (dev only).");
  admin.initializeApp({ credential: admin.credential.applicationDefault() });
  return admin.firestore();
}

export const db = init();
