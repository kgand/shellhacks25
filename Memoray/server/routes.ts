// server/routes.ts
import { Router } from 'express';
import { db } from './firebase';

const router = Router();

// Types
export type Relationship = {
  Relation: string;
  First_name: string;
  Last_name: string;
  Description: string;
  Image: string;
  isFamily: boolean;
  "Last Seen": string;
};

export type Highlight = {
  type: "food" | "car" | "home" | "landmark" | "photo";
  name: string;
  location?: string;
  url: string;
};

export type NamedPhoto = {
  name: string;
  url: string;
};

// Get relationships
router.get('/api/getRelationships', async (req, res) => {
  try {
    const snapshot = await db.collection('relationships').get();
    const relationships: Relationship[] = [];
    
    snapshot.forEach((doc) => {
      const data = doc.data();
      relationships.push({
        Relation: data.Relation || '',
        First_name: data.First_name || '',
        Last_name: data.Last_name || '',
        Description: data.Description || '',
        Image: data.Image || '',
        isFamily: data.isFamily || false,
        "Last Seen": data["Last Seen"] || '',
      });
    });
    
    res.json(relationships);
  } catch (error) {
    console.error('Error fetching relationships:', error);
    res.status(500).json({ error: 'Failed to fetch relationships' });
  }
});

// Get highlights by type
const getHighlightsByType = async (type: string): Promise<NamedPhoto[]> => {
  try {
    const snapshot = await db.collection('highlights')
      .where('type', '==', type)
      .get();
    
    const highlights: NamedPhoto[] = [];
    snapshot.forEach((doc) => {
      const data = doc.data();
      highlights.push({
        name: data.name || '',
        url: data.url || '',
      });
    });
    
    return highlights;
  } catch (error) {
    console.error(`Error fetching ${type} highlights:`, error);
    throw error;
  }
};

// Get food highlights
router.get('/api/get_food', async (req, res) => {
  try {
    const food = await getHighlightsByType('food');
    res.json(food);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch food highlights' });
  }
});

// Get car highlights
router.get('/api/get_car', async (req, res) => {
  try {
    const car = await getHighlightsByType('car');
    res.json(car);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch car highlights' });
  }
});

// Get home highlights
router.get('/api/get_home', async (req, res) => {
  try {
    const home = await getHighlightsByType('home');
    res.json(home);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch home highlights' });
  }
});

// Get landmark highlights
router.get('/api/get_landmarks', async (req, res) => {
  try {
    const landmarks = await getHighlightsByType('landmark');
    res.json(landmarks);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch landmark highlights' });
  }
});

// Get photo highlights
router.get('/api/get_photos', async (req, res) => {
  try {
    const photos = await getHighlightsByType('photo');
    res.json(photos);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch photo highlights' });
  }
});

export default router;
