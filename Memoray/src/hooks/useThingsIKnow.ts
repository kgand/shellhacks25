// src/hooks/useThingsIKnow.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { apiClient, ApiError } from '../lib/api';
import { readCache, writeCache } from '../api/client';
import { API, CACHE_KEYS } from '../api/endpoints';
import { Relationship, NamedPhoto } from '../api/types';

export type HookState = 'loading' | 'stale' | 'ready' | 'error';

export type ThingsIKnowData = {
  people: Relationship[];
  food: NamedPhoto[];
  cars: NamedPhoto[];
  home: NamedPhoto[];
  landmarks: NamedPhoto[];
  photos: NamedPhoto[];
};

export interface UseThingsIKnowResult {
  data: ThingsIKnowData;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  state: HookState;
}

export interface UseRelationshipsResult {
  data: Relationship[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  state: HookState;
}

export interface UseNamedPhotosResult {
  data: NamedPhoto[];
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  state: HookState;
}

export function useThingsIKnow(): UseThingsIKnowResult {
  const [data, setData] = useState<ThingsIKnowData>({
    people: [],
    food: [],
    cars: [],
    home: [],
    landmarks: [],
    photos: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [state, setState] = useState<HookState>('loading');
  const isMountedRef = useRef(true);

  const fetchData = useCallback(async (isRefresh = false) => {
    if (!isMountedRef.current) return;
    
    if (!isRefresh) {
      setLoading(true);
      setError(null);
    }

    try {
      // Try cache first
      const cachedData = await readCache<ThingsIKnowData>('metasense.thingsIKnow.v1');
      if (cachedData && !isRefresh && isMountedRef.current) {
        setData(cachedData);
        setState('stale');
        setLoading(false);
      }

      // Fetch all endpoints concurrently using new API client
      const [peopleRes, foodRes, carsRes, homeRes, landmarksRes, photosRes] = await Promise.all([
        apiClient.get<Relationship[]>('/api/getRelationships'),
        apiClient.get<NamedPhoto[]>('/api/get_food'),
        apiClient.get<NamedPhoto[]>('/api/get_car'),
        apiClient.get<NamedPhoto[]>('/api/get_home'),
        apiClient.get<NamedPhoto[]>('/api/get_landmarks'),
        apiClient.get<NamedPhoto[]>('/api/get_photos'),
      ]);

      if (!isMountedRef.current) return;

      const groupedData: ThingsIKnowData = {
        people: peopleRes.data.slice(0, 6), // Limit to 6 items for dashboard
        food: foodRes.data.slice(0, 6),
        cars: carsRes.data.slice(0, 6),
        home: homeRes.data.slice(0, 6),
        landmarks: landmarksRes.data.slice(0, 6),
        photos: photosRes.data.slice(0, 6),
      };

      setData(groupedData);
      await writeCache('metasense.thingsIKnow.v1', groupedData);
      setState('ready');
      setError(null);
    } catch (err) {
      if (!isMountedRef.current) return;
      
      const apiError = err as ApiError;
      let errorMessage = 'Failed to fetch data';
      
      if (apiError.code === 'NETWORK') {
        errorMessage = 'Network error - check your connection';
      } else if (apiError.code === 'TIMEOUT') {
        errorMessage = 'Request timeout - please try again';
      } else if (apiError.code === 'HTTP_4xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.code === 'HTTP_5xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.message) {
        errorMessage = apiError.message;
      }
      
      setError(errorMessage);
      setState('error');
      
      // If we have cached data, keep it and mark as stale
      if (data.people.length > 0 || data.food.length > 0) {
        setState('stale');
      }
    } finally {
      if (isMountedRef.current) {
        setLoading(false);
      }
    }
  }, [data.people.length, data.food.length]);

  const refetch = useCallback(async () => {
    try {
      await apiClient.revalidate();
      await fetchData(true);
    } catch (err) {
      // Error handling is done in fetchData
    }
  }, [fetchData]);

  useEffect(() => {
    fetchData();
    
    return () => {
      isMountedRef.current = false;
    };
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch,
    state,
  };
}

export function useRelationships(): UseRelationshipsResult {
  const [data, setData] = useState<Relationship[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [state, setState] = useState<HookState>('loading');
  const isMountedRef = useRef(true);

  const fetchData = useCallback(async (isRefresh = false) => {
    if (!isMountedRef.current) return;
    
    if (!isRefresh) {
      setLoading(true);
      setError(null);
    }

    try {
      // Try cache first
      const cachedData = await readCache<Relationship[]>(CACHE_KEYS.relationships);
      if (cachedData && !isRefresh && isMountedRef.current) {
        setData(cachedData);
        setState('stale');
        setLoading(false);
      }

      // Fetch from network using new API client
      const response = await apiClient.get<Relationship[]>('/api/getRelationships');
      
      if (!isMountedRef.current) return;
      
      setData(response.data);
      await writeCache(CACHE_KEYS.relationships, response.data);
      setState('ready');
      setError(null);
    } catch (err) {
      if (!isMountedRef.current) return;
      
      const apiError = err as ApiError;
      let errorMessage = 'Failed to fetch relationships';
      
      if (apiError.code === 'NETWORK') {
        errorMessage = 'Network error - check your connection';
      } else if (apiError.code === 'TIMEOUT') {
        errorMessage = 'Request timeout - please try again';
      } else if (apiError.code === 'HTTP_4xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.code === 'HTTP_5xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.message) {
        errorMessage = apiError.message;
      }
      
      setError(errorMessage);
      setState('error');
      
      // If we have cached data, keep it and mark as stale
      if (data.length > 0) {
        setState('stale');
      }
    } finally {
      if (isMountedRef.current) {
        setLoading(false);
      }
    }
  }, [data.length]);

  const refetch = useCallback(async () => {
    try {
      await apiClient.revalidate();
      await fetchData(true);
    } catch (err) {
      // Error handling is done in fetchData
    }
  }, [fetchData]);

  useEffect(() => {
    fetchData();
    
    return () => {
      isMountedRef.current = false;
    };
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch,
    state,
  };
}

export function useNamedPhotos(endpoint: string, cacheKey: string): UseNamedPhotosResult {
  const [data, setData] = useState<NamedPhoto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [state, setState] = useState<HookState>('loading');
  const isMountedRef = useRef(true);

  const fetchData = useCallback(async (isRefresh = false) => {
    if (!isMountedRef.current) return;
    
    if (!isRefresh) {
      setLoading(true);
      setError(null);
    }

    try {
      // Try cache first
      const cachedData = await readCache<NamedPhoto[]>(cacheKey);
      if (cachedData && !isRefresh && isMountedRef.current) {
        setData(cachedData);
        setState('stale');
        setLoading(false);
      }

      // Fetch from network using new API client
      const response = await apiClient.get<NamedPhoto[]>(endpoint);
      
      if (!isMountedRef.current) return;
      
      setData(response.data);
      await writeCache(cacheKey, response.data);
      setState('ready');
      setError(null);
    } catch (err) {
      if (!isMountedRef.current) return;
      
      const apiError = err as ApiError;
      let errorMessage = 'Failed to fetch photos';
      
      if (apiError.code === 'NETWORK') {
        errorMessage = 'Network error - check your connection';
      } else if (apiError.code === 'TIMEOUT') {
        errorMessage = 'Request timeout - please try again';
      } else if (apiError.code === 'HTTP_4xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.code === 'HTTP_5xx') {
        errorMessage = 'Server error - please try again later';
      } else if (apiError.message) {
        errorMessage = apiError.message;
      }
      
      setError(errorMessage);
      setState('error');
      
      // If we have cached data, keep it and mark as stale
      if (data.length > 0) {
        setState('stale');
      }
    } finally {
      if (isMountedRef.current) {
        setLoading(false);
      }
    }
  }, [endpoint, cacheKey, data.length]);

  const refetch = useCallback(async () => {
    try {
      await apiClient.revalidate();
      await fetchData(true);
    } catch (err) {
      // Error handling is done in fetchData
    }
  }, [fetchData]);

  useEffect(() => {
    fetchData();
    
    return () => {
      isMountedRef.current = false;
    };
  }, [fetchData]);

  return {
    data,
    loading,
    error,
    refetch,
    state,
  };
}

// Named wrapper hooks
export function useFood(): UseNamedPhotosResult {
  return useNamedPhotos('/api/get_food', CACHE_KEYS.food);
}

export function useCar(): UseNamedPhotosResult {
  return useNamedPhotos('/api/get_car', CACHE_KEYS.car);
}

export function useHome(): UseNamedPhotosResult {
  return useNamedPhotos('/api/get_home', CACHE_KEYS.home);
}

export function useLandmarks(): UseNamedPhotosResult {
  return useNamedPhotos('/api/get_landmarks', CACHE_KEYS.landmarks);
}

export function usePhotos(): UseNamedPhotosResult {
  return useNamedPhotos('/api/get_photos', CACHE_KEYS.photos);
}
