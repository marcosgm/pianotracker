/**
 * Frontend Main Entry Point
 */

import { router } from './services/router';
import { appStore } from './services/store';

/**
 * Initialize application
 */
function initializeApp(): void {
  console.log('🎹 Piano Practice Session Tracker - Initializing application');

  // Set up DOM root
  const root = document.getElementById('root');
  if (!root) {
    console.error('Root element not found');
    return;
  }

  // Initialize router
  router.init(root);

  // Check authentication on app load
  const token = localStorage.getItem('pianotracker_token');
  if (token) {
    appStore.setState({
      isAuthenticated: true
    });
    router.navigate('/dashboard');
  } else {
    router.navigate('/login');
  }

  // Set up global error handler
  window.addEventListener('error', (event) => {
    console.error('Uncaught error:', event.error);
    appStore.dispatch({
      type: 'SET_ERROR',
      payload: 'An unexpected error occurred'
    });
  });

  // Handle unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    appStore.dispatch({
      type: 'SET_ERROR',
      payload: 'An unexpected error occurred'
    });
  });

  console.log('✅ Application initialized successfully');
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}
