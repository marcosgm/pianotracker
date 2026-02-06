/**
 * TypeScript type definitions for Piano Practice Session Tracker
 */

// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface UserRegister {
  email: string;
  password: string;
  name: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Practice Session Types
export type PracticeType = 'chords' | 'scales' | 'course' | 'songs';

export interface PracticeSession {
  id: string;
  user_id: string;
  date: string;
  practice_type: PracticeType;
  tempo: number | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface SessionCreate {
  practice_type: PracticeType;
  tempo?: number;
  notes?: string;
}

export interface SessionUpdate {
  notes?: string | null;
}

export interface SessionsPage {
  sessions: PracticeSession[];
  total: number;
  limit: number;
  offset: number;
}

// Statistics Types
export interface TypeStatistics {
  count: number;
  percentage: number;
}

export interface Statistics {
  total_sessions: number;
  by_type: {
    chords?: TypeStatistics;
    scales?: TypeStatistics;
    course?: TypeStatistics;
    songs?: TypeStatistics;
  };
  average_tempo: {
    chords?: number;
    scales?: number;
  };
  recent_activity: Record<string, number>;
  period: 'week' | 'month' | 'year' | 'all';
}

// API Error Types
export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

// Application State Types
export interface AppState {
  currentUser: User | null;
  sessions: PracticeSession[];
  statistics: Statistics | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

// Store Action Types
export type StoreAction =
  | { type: 'SET_USER'; payload: User }
  | { type: 'CLEAR_USER' }
  | { type: 'SET_SESSIONS'; payload: PracticeSession[] }
  | { type: 'ADD_SESSION'; payload: PracticeSession }
  | { type: 'UPDATE_SESSION'; payload: PracticeSession }
  | { type: 'DELETE_SESSION'; payload: string }
  | { type: 'SET_STATISTICS'; payload: Statistics }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_ERROR' }
  | { type: 'SET_AUTHENTICATED'; payload: boolean };

// Store Listener Type
export type StoreListener = (state: AppState) => void;
