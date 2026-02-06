# Quickstart: Piano Practice Session Tracker

**Feature Branch**: `001-practice-tracker`  
**Estimated Time**: 5 minutes to setup, 4-6 weeks to complete  
**Prerequisites**: Python 3.11+, Node.js 18+, Azure CLI, Git

---

## 📋 Overview

This quickstart guide helps you set up your local development environment and begin implementing the Piano Practice Session Tracker feature. You'll set up both the backend (Python/FastAPI) and frontend (TypeScript), configure the database (CosmosDB emulator), and run your first tests.

---

## 🚀 Quick Setup (5 minutes)

### 1. Clone and Branch

```bash
# Already on feature branch from /speckit.specify
git checkout 001-practice-tracker
git pull origin 001-practice-tracker
```

### 2. Backend Setup (Python/FastAPI)

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# COSMOSDB_ENDPOINT, COSMOSDB_KEY, SECRET_KEY, etc.
```

**requirements.txt** (create if doesn't exist):
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-jose[cryptography]==3.3.0
bcrypt==4.1.1
azure-cosmos==4.5.1
python-multipart==0.0.6
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.1
```

### 3. Frontend Setup (TypeScript)

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env
# REACT_APP_API_URL=http://localhost:8000
```

**package.json** (create if doesn't exist):
```json
{
  "name": "pianotracker-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "webpack serve --mode development",
    "build": "webpack --mode production",
    "test": "jest",
    "test:e2e": "playwright test",
    "lint": "eslint src/**/*.ts",
    "analyze": "webpack-bundle-analyzer dist/stats.json"
  },
  "devDependencies": {
    "@types/jest": "^29.5.8",
    "@typescript-eslint/eslint-plugin": "^6.11.0",
    "@typescript-eslint/parser": "^6.11.0",
    "eslint": "^8.54.0",
    "jest": "^29.7.0",
    "playwright": "^1.40.0",
    "ts-jest": "^29.1.1",
    "ts-loader": "^9.5.1",
    "typescript": "^5.3.2",
    "webpack": "^5.89.0",
    "webpack-bundle-analyzer": "^4.10.1",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.1"
  },
  "dependencies": {
    "chart.js": "^4.4.0",
    "zod": "^3.22.4"
  }
}
```

### 4. Database Setup (CosmosDB Emulator)

**Option A: Azure CosmosDB Emulator (Windows/Linux)**

```bash
# Install CosmosDB Emulator
# Windows: Download from https://aka.ms/cosmosdb-emulator
# Linux: Use Docker (see below)

# Linux Docker:
docker run -p 8081:8081 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254 \
  -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 \
  -e AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=true \
  --name cosmos-emulator \
  mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:latest

# Get emulator certificate (for HTTPS)
curl -k https://localhost:8081/_explorer/emulator.pem > emulatorcert.crt
```

**Option B: Azure CosmosDB (Cloud)**

```bash
# Create resource group
az group create --name pianotracker-dev --location eastus

# Create CosmosDB account
az cosmosdb create \
  --name pianotracker-cosmos-dev \
  --resource-group pianotracker-dev \
  --default-consistency-level Session \
  --locations regionName=eastus failoverPriority=0

# Get connection string
az cosmosdb keys list \
  --name pianotracker-cosmos-dev \
  --resource-group pianotracker-dev \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" -o tsv
```

**Create Database and Containers**:

```bash
# Using Azure CLI
az cosmosdb sql database create \
  --account-name pianotracker-cosmos-dev \
  --resource-group pianotracker-dev \
  --name pianotracker

# Create users container
az cosmosdb sql container create \
  --account-name pianotracker-cosmos-dev \
  --resource-group pianotracker-dev \
  --database-name pianotracker \
  --name users \
  --partition-key-path "/partition_key" \
  --throughput 400

# Create practice_sessions container
az cosmosdb sql container create \
  --account-name pianotracker-cosmos-dev \
  --resource-group pianotracker-dev \
  --database-name pianotracker \
  --name practice_sessions \
  --partition-key-path "/partition_key" \
  --throughput 400
```

---

## 🏃 Run Development Servers

### Terminal 1: Backend

```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Server starts at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Terminal 2: Frontend

```bash
cd frontend
npm run dev

# Dev server starts at http://localhost:3000
```

### Terminal 3: Database (if using Docker)

```bash
# CosmosDB emulator runs in Docker
docker start cosmos-emulator
```

---

## ✅ Verify Setup

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "database": "connected"}
```

### 2. Check API Documentation

Open browser: http://localhost:8000/docs

You should see Swagger UI with all endpoints listed.

### 3. Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "name": "Test User"
  }'

# Expected: 201 Created with access_token
```

### 4. Check Frontend

Open browser: http://localhost:3000

You should see the login page.

---

## 🛠️ Development Workflow

### Step 1: Implement Backend (Week 1-2)

**Day 1-2: Models and Database**
```bash
# Create Pydantic models
touch backend/src/models/user.py
touch backend/src/models/practice_session.py

# Create CosmosDB client
touch backend/src/db/cosmos_client.py

# Write unit tests
touch backend/tests/unit/test_models.py
pytest backend/tests/unit/test_models.py
```

**Day 3-4: Authentication**
```bash
# Implement auth service
touch backend/src/services/auth_service.py

# Implement auth endpoints
touch backend/src/api/auth.py

# Write tests
touch backend/tests/integration/test_auth_api.py
pytest backend/tests/integration/
```

**Day 5-7: Session CRUD**
```bash
# Implement session service
touch backend/src/services/session_service.py
touch backend/src/services/stats_service.py

# Implement session endpoints
touch backend/src/api/sessions.py

# Write tests
touch backend/tests/integration/test_sessions_api.py
pytest backend/tests/
```

**Day 8-10: Security and Middleware**
```bash
# Implement JWT middleware
touch backend/src/api/middleware.py

# Add rate limiting
# Add CORS configuration
# Add error handling

# Run all tests
pytest backend/tests/ --cov=backend/src --cov-report=html
```

### Step 2: Implement Frontend (Week 3-4)

**Day 11-13: API Client and Auth**
```bash
# Create TypeScript types
touch frontend/src/types/index.ts

# Create API client
touch frontend/src/services/api.ts
touch frontend/src/services/auth.ts

# Create validation schemas
touch frontend/src/utils/validation.ts

# Create auth components
touch frontend/src/components/auth/LoginForm.ts
touch frontend/src/components/auth/RegisterForm.ts
```

**Day 14-16: Session Logging**
```bash
# Create session components
touch frontend/src/components/sessions/SessionForm.ts
touch frontend/src/pages/LogSessionPage.ts

# Implement validation
# Add optimistic updates

# Write unit tests
npm test -- --testPathPattern=SessionForm
```

**Day 17-19: History and Statistics**
```bash
# Create history components
touch frontend/src/components/sessions/SessionList.ts
touch frontend/src/components/stats/StatsCard.ts
touch frontend/src/pages/HistoryPage.ts

# Integrate Chart.js
# Implement pagination

# Write tests
npm test
```

**Day 20-22: E2E Tests**
```bash
# Create Playwright tests
touch frontend/tests/e2e/auth.spec.ts
touch frontend/tests/e2e/sessions.spec.ts
touch frontend/tests/e2e/history.spec.ts

# Run E2E tests
npm run test:e2e
```

### Step 3: Integration and Polish (Week 5-6)

**Day 23-25: Full Integration**
```bash
# Test complete user flow
# Fix integration issues
# Verify constitution compliance

# Run all tests
pytest backend/tests/ && npm test && npm run test:e2e
```

**Day 26-28: Performance Optimization**
```bash
# Run Lighthouse
npm run build
npx lighthouse http://localhost:3000 --view

# Optimize bundle size
npm run analyze

# Test Core Web Vitals
# Verify < 200KB bundle
```

**Day 29-30: Documentation and Cleanup**
```bash
# Update ARCHITECTURE.md
# Add JSDoc comments
# Update README
# Prepare for PR
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_auth_service.py

# Watch mode (install pytest-watch)
ptw
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch

# E2E tests
npm run test:e2e

# Specific test file
npm test -- --testPathPattern=SessionForm
```

### Contract Testing

```bash
# Validate OpenAPI spec
npx @stoplight/spectral-cli lint specs/001-practice-tracker/contracts/openapi.yaml

# Test API against contract
pip install schemathesis
schemathesis run specs/001-practice-tracker/contracts/openapi.yaml \
  --base-url http://localhost:8000 \
  --checks all
```

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| [spec.md](spec.md) | Feature requirements and user stories |
| [plan.md](plan.md) | Technical architecture and structure |
| [research.md](research.md) | Technology decisions and best practices |
| [data-model.md](data-model.md) | Entity schemas and validation rules |
| [contracts/openapi.yaml](contracts/openapi.yaml) | API contract (OpenAPI 3.0) |
| [contracts/README.md](contracts/README.md) | API usage guide |

---

## 🔍 Debugging Tips

### Backend Debugging

**Enable Debug Logging**:
```python
# src/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Use VSCode Debugger**:
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["src.main:app", "--reload"],
      "jinja": true
    }
  ]
}
```

**Check CosmosDB Queries**:
```python
# Enable query logging
from azure.cosmos import diagnostics
diagnostics.enable_http_logging()
```

### Frontend Debugging

**Enable Verbose Logging**:
```typescript
// src/services/api.ts
console.log('API Request:', endpoint, options);
console.log('API Response:', response);
```

**Use Browser DevTools**:
- Network tab: Check API requests/responses
- Console: Check for JavaScript errors
- Application tab: Check JWT token in localStorage

**Webpack Dev Server Logs**:
```bash
npm run dev -- --verbose
```

---

## 🚨 Common Issues

### Issue: CosmosDB Connection Failed

**Solution**:
```bash
# Check if emulator is running
curl -k https://localhost:8081/_explorer/index.html

# Verify connection string in .env
# Make sure COSMOSDB_ENDPOINT and COSMOSDB_KEY are set

# Linux: May need to install certificate
sudo cp emulatorcert.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

### Issue: CORS Error in Frontend

**Solution**:
```python
# backend/src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: JWT Token Expired

**Solution**:
```typescript
// frontend/src/services/api.ts
// Implement automatic token refresh in API client
if (response.status === 401) {
  const refreshed = await authService.refreshToken();
  if (refreshed) {
    return this.request(endpoint, options); // Retry
  }
}
```

### Issue: Bundle Size Exceeds 200KB

**Solution**:
```javascript
// webpack.config.js
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      chartjs: {
        test: /[\\/]node_modules[\\/]chart\.js/,
        name: 'chartjs',
        priority: 20
      }
    }
  }
}

// Lazy load Chart.js only on History page
const Chart = await import('chart.js/auto');
```

---

## 📈 Progress Tracking

Use the feature checklist to track implementation:

- [ ] Backend: Models and database client
- [ ] Backend: Authentication endpoints
- [ ] Backend: Session CRUD endpoints
- [ ] Backend: Statistics endpoint
- [ ] Backend: Tests (80%+ coverage)
- [ ] Frontend: API client and auth
- [ ] Frontend: Session logging form
- [ ] Frontend: Session history list
- [ ] Frontend: Statistics visualization
- [ ] Frontend: Tests (80%+ coverage)
- [ ] E2E: Complete user journey tests
- [ ] E2E: Accessibility tests (WCAG 2.1 AA)
- [ ] Performance: Core Web Vitals met
- [ ] Performance: Bundle < 200KB
- [ ] Documentation: Code comments and JSDoc
- [ ] Review: Constitution compliance check

---

## 🎯 Next Steps

1. **Start with Backend Models**: Implement `User` and `PracticeSession` Pydantic models
2. **Setup Database Client**: Create CosmosDB connection and CRUD operations
3. **Implement Auth**: Registration, login, JWT generation
4. **Follow TDD**: Write tests before implementation for critical paths
5. **Commit Frequently**: Small, focused commits with descriptive messages

---

## 🆘 Need Help?

- **Specification Questions**: Review [spec.md](spec.md) and [plan.md](plan.md)
- **API Contract**: Check [contracts/openapi.yaml](contracts/openapi.yaml)
- **Technical Decisions**: See [research.md](research.md)
- **Data Model**: Reference [data-model.md](data-model.md)
- **Constitution**: Verify [../../.specify/memory/constitution.md](../../.specify/memory/constitution.md)

**Good luck building! 🎹🎵**
