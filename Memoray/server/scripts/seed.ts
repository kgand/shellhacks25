// server/scripts/seed.ts
import path from "node:path";
import { config } from "dotenv";
config({ path: path.resolve(process.cwd(), "server", ".env") });

import { db } from "../firebase";

// ===== Types (must match your routes.ts) =====
type Relationship = {
  Relation: string;
  First_name: string;
  Last_name: string;
  Description: string;
  Image: string;
  isFamily: boolean;
  "Last Seen": string;
};

type Highlight = {
  type: "food" | "car" | "home" | "landmark" | "photo";
  name: string;
  location?: string;
  url: string;
};

// ===== Sample Data =====
const relationships: Relationship[] = [
  // Parents (both Black)
  {
    Relation: "Mother",
    First_name: "Monica",
    Last_name: "Carter",
    Description: "Enjoys gardening and puzzles. Calls on Sunday evenings.",
    Image: "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?q=80&w=600",
    isFamily: true,
    "Last Seen": "2025-09-27T18:10:00Z",
  },
  {
    Relation: "Father",
    First_name: "David",
    Last_name: "Carter",
    Description: "Loves jazz and weekend barbecues. Drives a blue SUV.",
    Image: "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=600",
    isFamily: true,
    "Last Seen": "2025-09-27T17:42:00Z",
  },

  // Multicultural friends
  {
    Relation: "Friend",
    First_name: "Aarav",
    Last_name: "Bejjinki",
    Description: "College friend; codes a lot. Gym on weeknights.",
    Image: "https://images.unsplash.com/photo-1607746882042-944635dfe10e?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-25T21:30:00Z",
  },
  {
    Relation: "Friend",
    First_name: "Camila",
    Last_name: "Reyes",
    Description: "Speaks Spanish and English. Loves salsa nights.",
    Image: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-26T15:05:00Z",
  },
  {
    Relation: "Friend",
    First_name: "Jae",
    Last_name: "Park",
    Description: "Coffee enthusiast. Plays pickup soccer on Saturdays.",
    Image: "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-24T12:10:00Z",
  },
  {
    Relation: "Friend",
    First_name: "Marcus",
    Last_name: "Hill",
    Description: "Runs 5Ks. Big Dolphins fan.",
    Image: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-26T09:40:00Z",
  },
  {
    Relation: "Friend",
    First_name: "Olivia",
    Last_name: "Bennett",
    Description: "Teacher. Book club on Thursdays.",
    Image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-22T19:55:00Z",
  },

  // Others
  {
    Relation: "Neighbor",
    First_name: "Morgan",
    Last_name: "Lee",
    Description: "Walks a golden retriever named Sunny around 6 pm.",
    Image: "https://images.unsplash.com/photo-1544005316-04ceae3b71a3?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-23T16:22:00Z",
  },
  {
    Relation: "Nurse",
    First_name: "Ana",
    Last_name: "Lopez",
    Description: "Clinic nurse; appointment check-ins on Mondays.",
    Image: "https://images.unsplash.com/photo-1582750433449-648ed127bb54?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-27T11:00:00Z",
  },
  {
    Relation: "Doctor",
    First_name: "Samuel",
    Last_name: "Nguyen",
    Description: "Primary care physician at Jupiter Medical.",
    Image: "https://images.unsplash.com/photo-1550831107-1553da8c8464?q=80&w=600",
    isFamily: false,
    "Last Seen": "2025-09-26T08:20:00Z",
  },
];

const highlights: Highlight[] = [
  // food
  {
    type: "food",
    name: "Blueberry Pancakes",
    location: "Jupiter Diner",
    url: "https://images.unsplash.com/photo-1516100882582-96c3a05fe590?q=80&w=600",
  },
  {
    type: "food",
    name: "Cuban Coffee",
    location: "Subculture Coffee",
    url: "https://images.unsplash.com/photo-1511920170033-f8396924c348?q=80&w=600",
  },

  // car
  {
    type: "car",
    name: "White Ford F-150",
    location: "Home Driveway",
    url: "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?q=80&w=600",
  },
  {
    type: "car",
    name: "Black Model Y",
    location: "Office Garage P3",
    url: "https://images.unsplash.com/photo-1619767886558-cd16b89b0a3b?q=80&w=600",
  },

  // home
  {
    type: "home",
    name: "Front Door",
    location: "123 Ocean Blvd",
    url: "https://images.unsplash.com/photo-1560185008-b033106af2d0?q=80&w=600",
  },
  {
    type: "home",
    name: "Kitchen Island",
    location: "123 Ocean Blvd",
    url: "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?q=80&w=600",
  },

  // landmark
  {
    type: "landmark",
    name: "Jupiter Inlet Lighthouse",
    location: "Jupiter, FL",
    url: "https://images.unsplash.com/photo-1579547621113-e4bb2a19bdd6?q=80&w=600",
  },
  {
    type: "landmark",
    name: "Wynwood Walls",
    location: "Miami, FL",
    url: "https://images.unsplash.com/photo-1496317556649-f930d733eea3?q=80&w=600",
  },

  // photo (generic names so they fit any dataset)
  {
    type: "photo",
    name: "Mom smiling",
    url: "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=600",
  },
  {
    type: "photo",
    name: "Conference talk",
    url: "https://images.unsplash.com/photo-1544005313-3bb4e8e68d18?q=80&w=600",
  },
  {
    type: "photo",
    name: "Coding at laptop",
    url: "https://images.unsplash.com/photo-1522252234503-e356532cafd5?q=80&w=600",
  },
];

// ===== Helpers =====
async function clearCollection(name: string) {
  const snap = await db.collection(name).get();
  const batch = db.batch();
  snap.forEach((doc) => batch.delete(doc.ref));
  if (!snap.empty) await batch.commit();
}

async function seedRelationships() {
  const col = db.collection("relationships");
  const batch = db.batch();

  relationships.forEach((r, idx) => {
    const docRef = col.doc(
      `${r.First_name.toLowerCase()}-${r.Last_name.toLowerCase()}-${idx}`
    );
    batch.set(docRef, r, { merge: true });
  });

  await batch.commit();
  return relationships.length;
}

async function seedHighlights() {
  const col = db.collection("highlights");
  const batch = db.batch();

  highlights.forEach((h, idx) => {
    const idBase = `${h.type}-${h.name.toLowerCase().replace(/\s+/g, "-")}-${idx}`;
    const docRef = col.doc(idBase);
    batch.set(docRef, h, { merge: true });
  });

  await batch.commit();
  return highlights.length;
}

// ===== Main =====
(async () => {
  const reset = process.argv.includes("--reset");
  if (reset) {
    console.log("Clearing collections: relationships, highlights...");
    await Promise.all([
      clearCollection("relationships"),
      clearCollection("highlights"),
    ]);
  }

  const [relCount, hiCount] = await Promise.all([
    seedRelationships(),
    seedHighlights(),
  ]);
  console.log(`Seed complete ✅  relationships: ${relCount}, highlights: ${hiCount}`);
  process.exit(0);
})().catch((err) => {
  console.error("Seeder failed:", err);
  process.exit(1);
});
