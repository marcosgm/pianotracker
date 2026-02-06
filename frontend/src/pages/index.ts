// Placeholder page components

class BasePage {
  render(): HTMLElement {
    const div = document.createElement('div');
    div.className = 'page';
    return div;
  }
}

export class LoginPage extends BasePage {
  render(): HTMLElement {
    const div = super.render();
    div.innerHTML = '<p>Login Page</p>';
    return div;
  }
}

export class RegisterPage extends BasePage {
  render(): HTMLElement {
    const div = super.render();
    div.innerHTML = '<p>Register Page</p>';
    return div;
  }
}

export class DashboardPage extends BasePage {
  render(): HTMLElement {
    const div = super.render();
    div.innerHTML = '<p>Dashboard Page</p>';
    return div;
  }
}

export class LogSessionPage extends BasePage {
  render(): HTMLElement {
    const div = super.render();
    div.innerHTML = '<p>Log Session Page</p>';
    return div;
  }
}

export class HistoryPage extends BasePage {
  render(): HTMLElement {
    const div = super.render();
    div.innerHTML = '<p>History Page</p>';
    return div;
  }
}
