/**
 * Application State Management (Pub/Sub Store Pattern)
 */

import type { AppState, StoreAction } from '../types';

const initialState: AppState = {
  currentUser: null,
  sessions: [],
  statistics: null,
  isLoading: false,
  error: null,
  isAuthenticated: false
};

class Store {
  private state: AppState = { ...initialState };
  private listeners: Array<(state: AppState) => void> = [];

  getState(): AppState {
    return { ...this.state };
  }

  setState(partial: Partial<AppState>): void {
    this.state = { ...this.state, ...partial };
    this.notifyListeners();
  }

  dispatch(action: StoreAction): void {
    switch (action.type) {
      case 'SET_USER':
        this.state = { ...this.state, currentUser: action.payload };
        break;
      case 'SET_SESSIONS':
        this.state = { ...this.state, sessions: action.payload };
        break;
      case 'SET_STATISTICS':
        this.state = { ...this.state, statistics: action.payload };
        break;
      case 'SET_LOADING':
        this.state = { ...this.state, isLoading: action.payload };
        break;
      case 'SET_ERROR':
        this.state = { ...this.state, error: action.payload };
        break;
      case 'SET_AUTHENTICATED':
        this.state = { ...this.state, isAuthenticated: action.payload };
        break;
      case 'CLEAR_USER':
        this.state = {
          ...this.state,
          currentUser: null,
          isAuthenticated: false,
          sessions: [],
          statistics: null
        };
        break;
      case 'ADD_SESSION':
        this.state = { ...this.state, sessions: [action.payload, ...this.state.sessions] };
        break;
      case 'UPDATE_SESSION':
        this.state = {
          ...this.state,
          sessions: this.state.sessions.map(s => 
            s.id === action.payload.id ? action.payload : s
          )
        };
        break;
      case 'DELETE_SESSION':
        this.state = {
          ...this.state,
          sessions: this.state.sessions.filter(s => s.id !== action.payload)
        };
        break;
    }
    this.notifyListeners();
  }

  subscribe(listener: (state: AppState) => void): () => void {
    this.listeners.push(listener);
    
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  private notifyListeners(): void {
    this.listeners.forEach(listener => {
      try {
        listener(this.getState());
      } catch (error) {
        console.error('Error in store listener:', error);
      }
    });
  }

  reset(): void {
    this.state = { ...initialState };
    this.notifyListeners();
  }
}

export const appStore = new Store();
