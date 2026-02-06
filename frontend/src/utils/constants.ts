/**
 * Application Constants
 */

// API Configuration
export const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';
export const API_TIMEOUT = 30000; // 30 seconds

// Storage Keys
export const JWT_STORAGE_KEY = 'pianotracker_token';
export const USER_STORAGE_KEY = 'pianotracker_user';

// Practice Types
export const PRACTICE_TYPES = ['chords', 'scales', 'course', 'songs'] as const;
export const PRACTICE_TYPE_LABELS: Record<string, string> = {
  chords: 'Chords',
  scales: 'Scales',
  course: 'Course',
  songs: 'Songs'
};

// Tempo Constraints
export const TEMPO_MIN = 90;
export const TEMPO_MAX = 120;
export const TEMPO_DEFAULT_CHORDS = 105;
export const TEMPO_DEFAULT_SCALES = 105;

// Session Pagination
export const SESSIONS_PER_PAGE = 20;
export const MAX_SESSIONS_PER_PAGE = 100;

// Notes Constraints
export const MAX_NOTES_LENGTH = 500;

// Statistics Periods
export const STATS_PERIODS = ['week', 'month', 'year', 'all'] as const;
export const DEFAULT_STATS_PERIOD = 'month';

// Form Constraints
export const MIN_PASSWORD_LENGTH = 8;
export const MAX_NAME_LENGTH = 100;

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_SERVER_ERROR: 500
} as const;

// Routes
export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  LOG_SESSION: '/log-session',
  HISTORY: '/history',
  LOGOUT: '/logout'
} as const;

// Messages
export const MESSAGES = {
  SUCCESS_LOGIN: 'Successfully logged in',
  SUCCESS_REGISTER: 'Account created successfully',
  SUCCESS_SESSION_CREATED: 'Session logged successfully',
  SUCCESS_SESSION_UPDATED: 'Session updated successfully',
  SUCCESS_SESSION_DELETED: 'Session deleted successfully',
  SUCCESS_LOGOUT: 'Logged out successfully',
  ERROR_GENERIC: 'An error occurred. Please try again.',
  ERROR_NETWORK: 'Network error. Please check your connection.',
  ERROR_AUTH_FAILED: 'Invalid email or password',
  ERROR_AUTH_REQUIRED: 'You must be logged in to access this page',
  ERROR_EMAIL_TAKEN: 'Email already registered',
  CONFIRM_DELETE_SESSION: 'Are you sure you want to delete this session?'
} as const;
