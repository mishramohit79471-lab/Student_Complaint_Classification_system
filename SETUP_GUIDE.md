# Setup Guide - Student Complaint Classification System

Complete step-by-step guide to set up the project locally.

## Prerequisites

Before starting, ensure you have installed:
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/)

## Windows Setup

### Step 1: Clone Repository
```bash
cd Desktop
git clone <repository-url>
cd Student_Complaint_Classification_system
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

#### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables
```bash
copy .env.example .env
# Edit .env with notepad and update:
# - DATABASE_URL: postgresql://user:password@localhost:5432/complaint_db
# - SECRET_KEY: your-very-secret-key-min-32-chars
# - DEBUG: False (for production)
```

#### 2.4 Create PostgreSQL Database

**Option A: Using psql (Command Prompt)**
```bash
# Start PostgreSQL service first
net start postgresql-x64-15  # Adjust version number

# Connect to PostgreSQL
psql -U postgres

# In psql:
CREATE DATABASE complaint_db;
CREATE USER complaint_user WITH PASSWORD 'your_secure_password';
ALTER ROLE complaint_user SET client_encoding TO 'utf8';
ALTER ROLE complaint_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE complaint_user SET default_transaction_deferrable TO on;
ALTER ROLE complaint_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;
\q
```

**Option B: Using pgAdmin (GUI)**
1. Open pgAdmin
2. Right-click on "Databases" → Create → Database
3. Name: `complaint_db`
4. Create a login role for `complaint_user`
5. Grant privileges

#### 2.5 Update Database URL in .env
```
DATABASE_URL=postgresql://complaint_user:your_password@localhost:5432/complaint_db
```

#### 2.6 Run Backend Server
```bash
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Access:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Step 3: Frontend Setup

#### 3.1 Open New Terminal
Keep backend running, open another terminal.

#### 3.2 Navigate to Frontend
```bash
cd frontend
```

#### 3.3 Install Dependencies
```bash
npm install
```

#### 3.4 Configure Environment Variables
```bash
copy .env.example .env
# Keep default or edit if backend is on different URL
# REACT_APP_API_URL=http://localhost:8000/api
```

#### 3.5 Start Development Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view complaint-system-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://xxx.xxx.x.xxx:3000
```

**Browser opens automatically** to http://localhost:3000

---

## macOS/Linux Setup

### Step 1: Clone Repository
```bash
cd ~/Desktop
git clone <repository-url>
cd Student_Complaint_Classification_system
```

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your editor:
nano .env
# Or: vim .env
```

#### 2.4 Create PostgreSQL Database

**macOS (using Homebrew):**
```bash
# Install PostgreSQL if not already installed
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database and user
createdb complaint_db
createuser complaint_user -P  # Enter password when prompted

# Grant privileges
psql complaint_db
GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;
\q
```

**Linux (Ubuntu/Debian):**
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres createdb complaint_db
sudo -u postgres createuser complaint_user -P

# Grant privileges
sudo -u postgres psql -d complaint_db -c "GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;"
```

#### 2.5 Update .env with Correct URL
```
DATABASE_URL=postgresql://complaint_user:password@localhost:5432/complaint_db
```

#### 2.6 Run Backend Server
```bash
python -m uvicorn app.main:app --reload
```

### Step 3: Frontend Setup

In another terminal:
```bash
cd frontend
npm install
npm start
```

---

## Testing the Setup

### 1. Test Backend API

**Open Swagger UI:** http://localhost:8000/docs

**Test Registration:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "TestPass123!",
    "role": "student"
  }'
```

**Test Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### 2. Test Frontend
- Visit http://localhost:3000
- See the homepage

---

## Troubleshooting

### PostgreSQL Connection Error
```
Error: could not connect to database
```
**Solution:**
- Verify PostgreSQL is running
- Windows: `net start postgresql-x14` (adjust version)
- macOS: `brew services start postgresql@15`
- Linux: `sudo systemctl start postgresql`
- Check DATABASE_URL in .env is correct

### Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:**
```bash
# Kill process on port 8000 (backend)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9
```

### Module Not Found Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### npm Dependencies Issues
```
npm ERR! code ERESOLVE
```
**Solution:**
```bash
npm install --legacy-peer-deps
```

### Permission Denied (macOS/Linux)
```
Permission denied: ./venv/bin/activate
```
**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## Project Structure Verification

After setup, verify the structure:

```
Student_Complaint_Classification_system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── middleware/
│   │   ├── services/
│   │   └── utils/
│   ├── venv/
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
├── frontend/
│   ├── src/
│   ├── public/
│   ├── node_modules/
│   ├── package.json
│   ├── .env
│   └── .gitignore
├── docs/
├── README.md
├── SETUP_GUIDE.md
├── .gitignore
└── .git/
```

---

## Next Steps

1. **Test the API** using Swagger UI at http://localhost:8000/docs
2. **Create test users** with different roles
3. **Submit test complaints** and track their flow
4. **Review documentation** in `/docs` folder
5. **Proceed to Phase 3** - ML Pipeline Implementation

---

## Useful Commands

### Backend
```bash
# Activate environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run with auto-reload
python -m uvicorn app.main:app --reload

# Run without reload
python -m uvicorn app.main:app

# Run with specific port
python -m uvicorn app.main:app --port 8001

# Deactivate environment
deactivate
```

### Frontend
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Database
```bash
# Connect to database (PostgreSQL)
psql -U complaint_user -d complaint_db

# List tables
\dt

# Exit psql
\q
```

---

## Environment Checklist

- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] PostgreSQL 12+ installed and running
- [ ] Git installed
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] .env files created and configured
- [ ] Database created with user
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:3000

---

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review error messages carefully
3. Check the README.md for additional information
4. Verify all prerequisites are installed
5. Ensure environment variables are correctly set

Good luck! 🚀
