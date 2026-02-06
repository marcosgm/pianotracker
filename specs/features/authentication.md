# Feature: User Authentication

**Status:** Not Started  
**Priority:** P0 (Blocking)  
**Effort:** Medium (3-5 days)

---

## Description

Secure user authentication system allowing users to register, log in, and manage their account to access private practice data.

---

## User Stories

- As a new user, I want to register with email/password so I can create an account
- As a returning user, I want to log in so I can access my practice data
- As a user, I want to reset my password if I forget it
- As a user, I want to stay logged in across sessions so I don't have to log in repeatedly
- As a user, I want to log out so I can secure my account on shared devices

---

## Acceptance Criteria

### Registration
- [ ] Email validation (valid format, unique)
- [ ] Password requirements (min 8 chars, contains number + letter)
- [ ] Password confirmation field matches
- [ ] Success: redirect to dashboard
- [ ] Error: display validation messages

### Login
- [ ] Accept email + password
- [ ] Show error for invalid credentials (generic message for security)
- [ ] Create session token (JWT)
- [ ] Remember me option (longer token expiry)
- [ ] Success: redirect to dashboard

### Password Reset
- [ ] Email input to request reset
- [ ] Send reset link to email (with expiring token)
- [ ] Reset form with new password + confirmation
- [ ] Token validation (valid, not expired, one-time use)
- [ ] Success: redirect to login with confirmation message

### Session Management
- [ ] Persist auth state in localStorage/cookie
- [ ] Auto-logout after token expiry
- [ ] Refresh token mechanism for extended sessions
- [ ] Protected routes redirect to login if not authenticated

---

## Technical Details

**Frontend:**
- Forms: React Hook Form + Zod validation
- Auth state: Context API or Zustand
- Protected routes: React Router loader/guard
- Token storage: localStorage (access) + httpOnly cookie (refresh)

**Backend:**
- Password hashing: bcrypt (cost 12)
- JWT tokens: access (15min), refresh (7d)
- Endpoints: `/api/auth/{register, login, logout, refresh, forgot-password, reset-password}`
- Rate limiting: 5 requests/min on auth endpoints

**Database:**
- Users table with email (unique), password_hash
- Optional: refresh_tokens table for revocation

---

## UI/UX Notes

- Clean, minimal forms
- Inline validation feedback
- Loading states on submit
- Clear error messages
- Link to switch between login/register
- Password visibility toggle

---

## Testing

**Unit:**
- Validation schemas (email format, password strength)
- Password hashing/verification

**Integration:**
- Registration flow (create user → hash password → store → return token)
- Login flow (verify credentials → generate token)
- Token refresh flow

**E2E:**
- Complete registration → login → access protected page → logout
- Password reset flow
- Invalid credentials handling

---

## Dependencies

- JWT library (jsonwebtoken)
- bcrypt
- Email service (for password reset)

---

## Open Questions

- Email verification required on registration?
- Social auth (Google, GitHub) in future?
- Two-factor authentication?
