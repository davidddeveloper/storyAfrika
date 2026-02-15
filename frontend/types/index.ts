/**
 * StoryAfrika TypeScript Types
 * Matching Django backend models
 */

// User Types
export interface User {
  id: string;
  email: string;
  full_name: string;
  username: string | null;
  biography: string;
  avatar: string | null;
  is_writer: boolean;
  is_editor: boolean;
  date_joined: string;
  published_stories_count?: number;
}

export interface WriterProfile {
  user: User;
  writing_sample: string;
  motivation: string;
  approved: boolean;
  approved_at: string | null;
  rejected_at: string | null;
}

// Taxonomy Types
export interface Country {
  id: string;
  name: string;
  slug: string;
  description: string;
  stories_count?: number;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  stories_count?: number;
}

export interface Theme {
  id: string;
  name: string;
  slug: string;
  description: string;
}

export interface Era {
  id: string;
  name: string;
  slug: string;
  description: string;
  time_period: string;
}

// Story Types
export interface Story {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  author: User;
  category: Category;
  country: Country;
  themes: Theme[];
  era: Era;
  status: 'draft' | 'submitted' | 'published' | 'archived';
  read_time: number;
  created_at: string;
  updated_at: string;
  published_at: string | null;
  is_bookmarked?: boolean;
}

export interface StoryCreate {
  title: string;
  excerpt: string;
  content: string;
  category_id: string;
  country_id: string;
  theme_ids: string[];
  era_id: string;
}

// Editorial Types
export interface FeaturedStory {
  id: string;
  story: Story;
  featured_at: string;
  featured_by: User;
  featured_until: string | null;
}

export interface ContentGuideline {
  id: string;
  title: string;
  slug: string;
  content: string;
  category: 'writing' | 'submission' | 'content_policy' | 'editorial';
  created_at: string;
  updated_at: string;
}

// Auth Types
export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  full_name: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}

// API Response Types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface APIError {
  detail: string;
  code?: string;
}

// Bookmark Type
export interface Bookmark {
  id: string;
  user: string;
  story: Story;
  created_at: string;
}
