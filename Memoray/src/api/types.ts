// src/api/types.ts

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

export type ApiResponse<T> = {
  data: T;
  success: boolean;
  message?: string;
};
