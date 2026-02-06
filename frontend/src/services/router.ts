/**
 * Simple Router for Single Page Application
 */

import { LoginPage, RegisterPage, DashboardPage, LogSessionPage, HistoryPage } from '../pages/index';

type RouteHandler = (root: HTMLElement) => void;

const routes: Record<string, RouteHandler> = {
  '/login': (root) => {
    const page = new LoginPage();
    root.appendChild(page.render());
  },
  '/register': (root) => {
    const page = new RegisterPage();
    root.appendChild(page.render());
  },
  '/dashboard': (root) => {
    const page = new DashboardPage();
    root.appendChild(page.render());
  },
  '/log-session': (root) => {
    const page = new LogSessionPage();
    root.appendChild(page.render());
  },
  '/history': (root) => {
    const page = new HistoryPage();
    root.appendChild(page.render());
  }
};

class Router {
  private currentPath: string = '/login';
  private root: HTMLElement | null = null;

  init(root: HTMLElement): void {
    this.root = root;
    
    // Handle browser back/forward
    window.addEventListener('popstate', () => {
      this.renderPage();
    });

    // Handle initial route
    const path = window.location.pathname || '/login';
    this.navigate(path, false);
  }

  navigate(path: string, pushState: boolean = true): void {
    this.currentPath = path;
    
    if (pushState) {
      window.history.pushState({ path }, '', path);
    }
    
    this.renderPage();
  }

  private renderPage(): void {
    if (!this.root) return;

    const handler = routes[this.currentPath];
    if (!handler) {
      console.warn(`No route found for ${this.currentPath}`);
      this.navigate('/login');
      return;
    }

    try {
      this.root.innerHTML = '';
      handler(this.root);
    } catch (error) {
      console.error('Error rendering page:', error);
      this.root.innerHTML = '<p>Error loading page. Please refresh.</p>';
    }
  }

  getCurrentPath(): string {
    return this.currentPath;
  }
}

export const router = new Router();
