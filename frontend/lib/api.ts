/**
 * StoryAfrika API Client
 * Axios-based client for Django REST API
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  Story,
  Country,
  Category,
  Theme,
  Era,
  FeaturedStory,
  ContentGuideline,
  WriterProfile,
  Bookmark,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  AuthTokens,
  PaginatedResponse,
  StoryCreate,
} from '@/types';

// API Base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_STORAGE_KEY = 'storyafrika_tokens';

export const tokenStorage = {
  get: (): AuthTokens | null => {
    if (typeof window === 'undefined') return null;
    const tokens = localStorage.getItem(TOKEN_STORAGE_KEY);
    return tokens ? JSON.parse(tokens) : null;
  },

  set: (tokens: AuthTokens): void => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(TOKEN_STORAGE_KEY, JSON.stringify(tokens));
  },

  clear: (): void => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  },
};

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const tokens = tokenStorage.get();
    if (tokens?.access) {
      config.headers.Authorization = `Bearer ${tokens.access}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest: any = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const tokens = tokenStorage.get();
      if (tokens?.refresh) {
        try {
          // Try to refresh the token
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: tokens.refresh,
          });

          const newTokens: AuthTokens = {
            access: response.data.access,
            refresh: tokens.refresh,
          };

          tokenStorage.set(newTokens);
          originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;

          return apiClient(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear tokens
          tokenStorage.clear();
          if (typeof window !== 'undefined') {
            window.location.href = '/login';
          }
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// ============================================
// Authentication API
// ============================================

export const authAPI = {
  // Register new user
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/users/register/', data);
    tokenStorage.set(response.data.tokens);
    return response.data;
  },

  // Login
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/users/login/', credentials);
    tokenStorage.set(response.data.tokens);
    return response.data;
  },

  // Logout
  logout: async (): Promise<void> => {
    const tokens = tokenStorage.get();
    if (tokens?.refresh) {
      try {
        await apiClient.post('/users/logout/', { refresh: tokens.refresh });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }
    tokenStorage.clear();
  },

  // Get current user
  me: async (): Promise<User> => {
    const response = await apiClient.get<User>('/users/me/');
    return response.data;
  },
};

// ============================================
// Stories API
// ============================================

export const storiesAPI = {
  // List stories
  list: async (params?: {
    page?: number;
    search?: string;
    category?: string;
    country?: string;
    status?: string;
  }): Promise<PaginatedResponse<Story>> => {
    const response = await apiClient.get<PaginatedResponse<Story>>('/stories/', { params });
    return response.data;
  },

  // Get single story
  get: async (slug: string): Promise<Story> => {
    const response = await apiClient.get<Story>(`/stories/${slug}/`);
    return response.data;
  },

  // Create story (writers only)
  create: async (data: StoryCreate): Promise<Story> => {
    const response = await apiClient.post<Story>('/stories/', data);
    return response.data;
  },

  // Update story
  update: async (slug: string, data: Partial<StoryCreate>): Promise<Story> => {
    const response = await apiClient.patch<Story>(`/stories/${slug}/`, data);
    return response.data;
  },

  // Delete story
  delete: async (slug: string): Promise<void> => {
    await apiClient.delete(`/stories/${slug}/`);
  },

  // Submit story for review
  submit: async (slug: string): Promise<Story> => {
    const response = await apiClient.post<Story>(`/stories/${slug}/submit/`);
    return response.data;
  },

  // Search stories
  search: async (query: string): Promise<PaginatedResponse<Story>> => {
    const response = await apiClient.get<PaginatedResponse<Story>>('/stories/search/', {
      params: { q: query },
    });
    return response.data;
  },
};

// ============================================
// Taxonomy API
// ============================================

export const countriesAPI = {
  list: async (): Promise<PaginatedResponse<Country>> => {
    const response = await apiClient.get<PaginatedResponse<Country>>('/countries/');
    return response.data;
  },

  get: async (slug: string): Promise<Country> => {
    const response = await apiClient.get<Country>(`/countries/${slug}/`);
    return response.data;
  },
};

export const categoriesAPI = {
  list: async (): Promise<PaginatedResponse<Category>> => {
    const response = await apiClient.get<PaginatedResponse<Category>>('/categories/');
    return response.data;
  },

  get: async (slug: string): Promise<Category> => {
    const response = await apiClient.get<Category>(`/categories/${slug}/`);
    return response.data;
  },
};

export const themesAPI = {
  list: async (): Promise<PaginatedResponse<Theme>> => {
    const response = await apiClient.get<PaginatedResponse<Theme>>('/themes/');
    return response.data;
  },
};

export const erasAPI = {
  list: async (): Promise<PaginatedResponse<Era>> => {
    const response = await apiClient.get<PaginatedResponse<Era>>('/eras/');
    return response.data;
  },
};

// ============================================
// User Actions API
// ============================================

export const bookmarksAPI = {
  // List user's bookmarks
  list: async (): Promise<PaginatedResponse<Bookmark>> => {
    const response = await apiClient.get<PaginatedResponse<Bookmark>>('/bookmarks/');
    return response.data;
  },

  // Bookmark a story
  create: async (storyId: string): Promise<Bookmark> => {
    const response = await apiClient.post<Bookmark>('/bookmarks/', { story: storyId });
    return response.data;
  },

  // Remove bookmark
  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/bookmarks/${id}/`);
  },
};

export const writerApplicationsAPI = {
  // Apply to become a writer
  apply: async (data: {
    writing_sample: string;
    motivation: string;
  }): Promise<WriterProfile> => {
    const response = await apiClient.post<WriterProfile>('/writer-applications/', data);
    return response.data;
  },
};

// ============================================
// Featured & Editorial API
// ============================================

export const featuredAPI = {
  list: async (): Promise<PaginatedResponse<FeaturedStory>> => {
    const response = await apiClient.get<PaginatedResponse<FeaturedStory>>('/featured-stories/');
    return response.data;
  },
};

export const guidelinesAPI = {
  list: async (category?: string): Promise<PaginatedResponse<ContentGuideline>> => {
    const response = await apiClient.get<PaginatedResponse<ContentGuideline>>('/content-guidelines/', {
      params: category ? { category } : undefined,
    });
    return response.data;
  },

  get: async (slug: string): Promise<ContentGuideline> => {
    const response = await apiClient.get<ContentGuideline>(`/content-guidelines/${slug}/`);
    return response.data;
  },
};

// Export the client for custom requests
export default apiClient;
