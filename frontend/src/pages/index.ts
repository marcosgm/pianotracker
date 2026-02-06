/**
 * Page Components
 */
import { router } from '../services/router';
import { appStore } from '../services/store';

class BasePage {
  render(): HTMLElement {
    const div = document.createElement('div');
    div.className = 'page';
    return div;
  }
}

export class LoginPage extends BasePage {
  render(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'container';
    container.style.cssText = 'max-width: 400px; margin: 80px auto; padding: 20px;';

    container.innerHTML = `
      <div class="card">
        <h1 style="text-align: center; margin-bottom: 30px; color: #2C3E50;">🎹 Piano Tracker</h1>
        <h2 style="text-align: center; margin-bottom: 30px; color: #7F8C8D;">Login</h2>
        
        <form id="loginForm">
          <div class="form-group" style="margin-bottom: 20px;">
            <label for="email" style="display: block; margin-bottom: 8px; font-weight: 500;">Email</label>
            <input 
              type="email" 
              id="email" 
              name="email" 
              required
              placeholder="your@email.com"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
          </div>
          
          <div class="form-group" style="margin-bottom: 20px;">
            <label for="password" style="display: block; margin-bottom: 8px; font-weight: 500;">Password</label>
            <input 
              type="password" 
              id="password" 
              name="password" 
              required
              placeholder="Enter your password"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
          </div>

          <div id="error" style="color: #E74C3C; margin-bottom: 15px; display: none;"></div>
          
          <button 
            type="submit" 
            class="btn btn-primary"
            style="width: 100%; padding: 14px; background: #4A90E2; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;"
          >
            Login
          </button>
        </form>

        <div style="text-align: center; margin-top: 20px; color: #7F8C8D;">
          Don't have an account? 
          <a href="#" id="registerLink" style="color: #4A90E2; text-decoration: none; font-weight: 500;">Register here</a>
        </div>
      </div>
    `;

    // Handle form submission
    const form = container.querySelector('#loginForm') as HTMLFormElement;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const errorDiv = container.querySelector('#error') as HTMLDivElement;
      errorDiv.style.display = 'none';

      const formData = new FormData(form);
      const email = formData.get('email') as string;
      const password = formData.get('password') as string;

      // TODO: Implement actual API call in Phase 3
      console.log('Login attempt:', { email, password });
      errorDiv.textContent = 'Backend API not yet implemented. Coming in Phase 3!';
      errorDiv.style.display = 'block';
    });

    // Handle register link
    const registerLink = container.querySelector('#registerLink');
    registerLink?.addEventListener('click', (e) => {
      e.preventDefault();
      router.navigate('/register');
    });

    return container;
  }
}

export class RegisterPage extends BasePage {
  render(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'container';
    container.style.cssText = 'max-width: 400px; margin: 80px auto; padding: 20px;';

    container.innerHTML = `
      <div class="card">
        <h1 style="text-align: center; margin-bottom: 30px; color: #2C3E50;">🎹 Piano Tracker</h1>
        <h2 style="text-align: center; margin-bottom: 30px; color: #7F8C8D;">Create Account</h2>
        
        <form id="registerForm">
          <div class="form-group" style="margin-bottom: 20px;">
            <label for="name" style="display: block; margin-bottom: 8px; font-weight: 500;">Name</label>
            <input 
              type="text" 
              id="name" 
              name="name" 
              required
              placeholder="Your name"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
          </div>

          <div class="form-group" style="margin-bottom: 20px;">
            <label for="email" style="display: block; margin-bottom: 8px; font-weight: 500;">Email</label>
            <input 
              type="email" 
              id="email" 
              name="email" 
              required
              placeholder="your@email.com"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
          </div>
          
          <div class="form-group" style="margin-bottom: 20px;">
            <label for="password" style="display: block; margin-bottom: 8px; font-weight: 500;">Password</label>
            <input 
              type="password" 
              id="password" 
              name="password" 
              required
              placeholder="Min 8 characters, 1 digit + 1 letter"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
            <small style="color: #7F8C8D; font-size: 12px;">Must be at least 8 characters with 1 digit and 1 letter</small>
          </div>

          <div class="form-group" style="margin-bottom: 20px;">
            <label for="passwordConfirm" style="display: block; margin-bottom: 8px; font-weight: 500;">Confirm Password</label>
            <input 
              type="password" 
              id="passwordConfirm" 
              name="passwordConfirm" 
              required
              placeholder="Re-enter your password"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
          </div>

          <div id="error" style="color: #E74C3C; margin-bottom: 15px; display: none;"></div>
          
          <button 
            type="submit" 
            class="btn btn-primary"
            style="width: 100%; padding: 14px; background: #27AE60; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;"
          >
            Create Account
          </button>
        </form>

        <div style="text-align: center; margin-top: 20px; color: #7F8C8D;">
          Already have an account? 
          <a href="#" id="loginLink" style="color: #4A90E2; text-decoration: none; font-weight: 500;">Login here</a>
        </div>
      </div>
    `;

    // Handle form submission
    const form = container.querySelector('#registerForm') as HTMLFormElement;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const errorDiv = container.querySelector('#error') as HTMLDivElement;
      errorDiv.style.display = 'none';

      const formData = new FormData(form);
      const name = formData.get('name') as string;
      const email = formData.get('email') as string;
      const password = formData.get('password') as string;
      const passwordConfirm = formData.get('passwordConfirm') as string;

      // Client-side validation
      if (password !== passwordConfirm) {
        errorDiv.textContent = 'Passwords do not match';
        errorDiv.style.display = 'block';
        return;
      }

      if (password.length < 8) {
        errorDiv.textContent = 'Password must be at least 8 characters';
        errorDiv.style.display = 'block';
        return;
      }

      if (!/[0-9]/.test(password)) {
        errorDiv.textContent = 'Password must contain at least one digit';
        errorDiv.style.display = 'block';
        return;
      }

      if (!/[a-zA-Z]/.test(password)) {
        errorDiv.textContent = 'Password must contain at least one letter';
        errorDiv.style.display = 'block';
        return;
      }

      // TODO: Implement actual API call in Phase 3
      console.log('Registration attempt:', { name, email, password });
      errorDiv.textContent = 'Backend API not yet implemented. Coming in Phase 3!';
      errorDiv.style.display = 'block';
    });

    // Handle login link
    const loginLink = container.querySelector('#loginLink');
    loginLink?.addEventListener('click', (e) => {
      e.preventDefault();
      router.navigate('/login');
    });

    return container;
  }
}

export class DashboardPage extends BasePage {
  render(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'container';
    container.style.cssText = 'max-width: 1200px; margin: 40px auto; padding: 20px;';

    container.innerHTML = `
      <div class="card">
        <h1 style="color: #2C3E50; margin-bottom: 20px;">🎹 Dashboard</h1>
        <p style="color: #7F8C8D; margin-bottom: 30px;">Welcome to Piano Practice Session Tracker!</p>
        
        <div style="display: grid; gap: 20px; margin-bottom: 30px;">
          <button 
            id="logSessionBtn"
            style="padding: 20px; background: #4A90E2; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer;"
          >
            ➕ Log New Practice Session
          </button>
          
          <button 
            id="historyBtn"
            style="padding: 20px; background: #27AE60; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer;"
          >
            📊 View History & Statistics
          </button>
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <a href="#" id="logoutLink" style="color: #E74C3C; text-decoration: none;">Logout</a>
        </div>
      </div>
    `;

    // Handle navigation
    container.querySelector('#logSessionBtn')?.addEventListener('click', () => {
      router.navigate('/log-session');
    });

    container.querySelector('#historyBtn')?.addEventListener('click', () => {
      router.navigate('/history');
    });

    container.querySelector('#logoutLink')?.addEventListener('click', (e) => {
      e.preventDefault();
      localStorage.removeItem('pianotracker_token');
      appStore.setState({ isAuthenticated: false, currentUser: null });
      router.navigate('/login');
    });

    return container;
  }
}

export class LogSessionPage extends BasePage {
  render(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'container';
    container.style.cssText = 'max-width: 600px; margin: 40px auto; padding: 20px;';

    container.innerHTML = `
      <div class="card">
        <h1 style="color: #2C3E50; margin-bottom: 30px;">Log Practice Session</h1>
        
        <form id="sessionForm">
          <div class="form-group" style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 12px; font-weight: 500; font-size: 16px;">Practice Type</label>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
              <button type="button" class="practice-type-btn" data-type="chords" style="padding: 15px; border: 2px solid #ddd; background: white; border-radius: 8px; cursor: pointer; font-size: 16px;">🎵 Chords</button>
              <button type="button" class="practice-type-btn" data-type="scales" style="padding: 15px; border: 2px solid #ddd; background: white; border-radius: 8px; cursor: pointer; font-size: 16px;">🎼 Scales</button>
              <button type="button" class="practice-type-btn" data-type="course" style="padding: 15px; border: 2px solid #ddd; background: white; border-radius: 8px; cursor: pointer; font-size: 16px;">📚 Course</button>
              <button type="button" class="practice-type-btn" data-type="songs" style="padding: 15px; border: 2px solid #ddd; background: white; border-radius: 8px; cursor: pointer; font-size: 16px;">🎹 Songs</button>
            </div>
          </div>

          <div id="tempoGroup" class="form-group" style="margin-bottom: 20px; display: none;">
            <label for="tempo" style="display: block; margin-bottom: 8px; font-weight: 500;">Tempo (BPM)</label>
            <input 
              type="number" 
              id="tempo" 
              name="tempo" 
              min="90" 
              max="120" 
              placeholder="90-120"
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px;"
            />
            <small style="color: #7F8C8D; font-size: 12px;">Required for Chords and Scales (90-120 BPM)</small>
          </div>

          <div class="form-group" style="margin-bottom: 20px;">
            <label for="notes" style="display: block; margin-bottom: 8px; font-weight: 500;">Notes (Optional)</label>
            <textarea 
              id="notes" 
              name="notes" 
              rows="4"
              maxlength="500"
              placeholder="Add any notes about this practice session..."
              style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; resize: vertical;"
            ></textarea>
            <small id="charCount" style="color: #7F8C8D; font-size: 12px;">0/500 characters</small>
          </div>

          <div id="error" style="color: #E74C3C; margin-bottom: 15px; display: none;"></div>
          
          <div style="display: flex; gap: 10px;">
            <button 
              type="submit" 
              style="flex: 1; padding: 14px; background: #4A90E2; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;"
            >
              Save Session
            </button>
            <button 
              type="button" 
              id="cancelBtn"
              style="padding: 14px 30px; background: #95A5A6; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    `;

    let selectedType: string | null = null;

    // Handle practice type selection
    const typeButtons = container.querySelectorAll('.practice-type-btn');
    const tempoGroup = container.querySelector('#tempoGroup') as HTMLDivElement;
    const tempoInput = container.querySelector('#tempo') as HTMLInputElement;

    typeButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        typeButtons.forEach(b => {
          (b as HTMLElement).style.borderColor = '#ddd';
          (b as HTMLElement).style.background = 'white';
        });
        (btn as HTMLElement).style.borderColor = '#4A90E2';
        (btn as HTMLElement).style.background = '#E8F4FD';
        
        selectedType = (btn as HTMLElement).dataset.type || null;
        
        // Show tempo field for chords and scales
        if (selectedType === 'chords' || selectedType === 'scales') {
          tempoGroup.style.display = 'block';
          tempoInput.required = true;
        } else {
          tempoGroup.style.display = 'none';
          tempoInput.required = false;
          tempoInput.value = '';
        }
      });
    });

    // Character counter
    const notesTextarea = container.querySelector('#notes') as HTMLTextAreaElement;
    const charCount = container.querySelector('#charCount') as HTMLElement;
    notesTextarea.addEventListener('input', () => {
      charCount.textContent = `${notesTextarea.value.length}/500 characters`;
    });

    // Handle form submission
    const form = container.querySelector('#sessionForm') as HTMLFormElement;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const errorDiv = container.querySelector('#error') as HTMLDivElement;
      errorDiv.style.display = 'none';

      if (!selectedType) {
        errorDiv.textContent = 'Please select a practice type';
        errorDiv.style.display = 'block';
        return;
      }

      const tempo = tempoInput.value ? parseInt(tempoInput.value) : null;
      const notes = notesTextarea.value || null;

      console.log('Session data:', { practice_type: selectedType, tempo, notes });
      errorDiv.textContent = 'Backend API not yet implemented. Coming in Phase 4!';
      errorDiv.style.display = 'block';
    });

    // Handle cancel
    container.querySelector('#cancelBtn')?.addEventListener('click', () => {
      router.navigate('/dashboard');
    });

    return container;
  }
}

export class HistoryPage extends BasePage {
  render(): HTMLElement {
    const container = document.createElement('div');
    container.className = 'container';
    container.style.cssText = 'max-width: 1200px; margin: 40px auto; padding: 20px;';

    container.innerHTML = `
      <div class="card">
        <h1 style="color: #2C3E50; margin-bottom: 30px;">Practice History & Statistics</h1>
        
        <div style="background: #F8F9FA; padding: 30px; border-radius: 8px; text-align: center; margin-bottom: 30px;">
          <h2 style="color: #7F8C8D; margin-bottom: 20px;">📊 Your Practice Stats</h2>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 20px; border-radius: 8px;">
              <div style="font-size: 36px; font-weight: bold; color: #4A90E2;">0</div>
              <div style="color: #7F8C8D; margin-top: 5px;">Total Sessions</div>
            </div>
            <div style="background: white; padding: 20px; border-radius: 8px;">
              <div style="font-size: 36px; font-weight: bold; color: #27AE60;">0</div>
              <div style="color: #7F8C8D; margin-top: 5px;">This Week</div>
            </div>
            <div style="background: white; padding: 20px; border-radius: 8px;">
              <div style="font-size: 36px; font-weight: bold; color: #E67E22;">-</div>
              <div style="color: #7F8C8D; margin-top: 5px;">Avg Tempo</div>
            </div>
          </div>
        </div>

        <h2 style="color: #2C3E50; margin-bottom: 20px;">Recent Sessions</h2>
        <div style="background: #F8F9FA; padding: 40px; border-radius: 8px; text-align: center; color: #7F8C8D;">
          <div style="font-size: 48px; margin-bottom: 20px;">🎹</div>
          <p style="font-size: 18px;">No practice sessions logged yet.</p>
          <p style="margin-top: 10px;">Start tracking your piano practice to see your progress!</p>
          <button 
            id="logFirstBtn"
            style="margin-top: 30px; padding: 14px 30px; background: #4A90E2; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: 600; cursor: pointer;"
          >
            Log Your First Session
          </button>
        </div>

        <div style="text-align: center; margin-top: 30px;">
          <a href="#" id="backLink" style="color: #4A90E2; text-decoration: none; font-weight: 500;">← Back to Dashboard</a>
        </div>
      </div>
    `;

    // Handle navigation
    container.querySelector('#logFirstBtn')?.addEventListener('click', () => {
      router.navigate('/log-session');
    });

    container.querySelector('#backLink')?.addEventListener('click', (e) => {
      e.preventDefault();
      router.navigate('/dashboard');
    });

    return container;
  }
}
