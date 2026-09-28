# Quick Start Guide

## Prerequisites Completed ✅
- Python 3.13 virtual environment created
- Backend dependencies installed
- Frontend scaffolding ready

## Starting the Application

### 1. Database Setup (One-time)

**Create PostgreSQL Database:**
```sql
-- Open pgAdmin or use psql command line
CREATE DATABASE complaint_db;
CREATE USER complaint_user WITH PASSWORD 'your_secure_password';
ALTER ROLE complaint_user SET client_encoding TO 'utf8';
ALTER ROLE complaint_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE complaint_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;
```

### 2. Configure Backend

**Edit:** `backend/.env`
```
DATABASE_URL=postgresql://complaint_user:your_password@localhost:5432/complaint_db
SECRET_KEY=your-very-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### 3. Start Backend Server

**Option A: Double-click (Windows)**
```
backend\run_server.bat
```

**Option B: PowerShell**
```powershell
cd backend
.\run_server.ps1
```

**Option C: Command Prompt**
```cmd
cd backend
python -m uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 4. Start Frontend Server (New Terminal)

**Option A: Double-click (Windows)**
```
frontend\run_dev.bat
```

**Option B: PowerShell**
```powershell
cd frontend
npm install
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view complaint-system-frontend in the browser.

  Local:            http://localhost:3000
```

**Browser opens automatically** to http://localhost:3000

## Testing the System

### Test 1: Register User (via Swagger UI)

1. Open http://localhost:8000/docs
2. Click "Authorize" → Enter any token (temporary)
3. Find `POST /api/auth/register`
4. Click "Try it out"
5. Enter:
```json
{
  "email": "student@test.com",
  "full_name": "Test Student",
  "password": "Test123!@",
  "role": "student"
}
```
6. Click "Execute"

### Test 2: Login

1. In Swagger UI, find `POST /api/auth/login`
2. Click "Try it out"
3. Enter:
```json
{
  "email": "student@test.com",
  "password": "Test123!@"
}
```
4. Click "Execute"
5. Copy the `access_token` from response

### Test 3: Submit Complaint

1. Click "Authorize" button
2. Paste token as: `Bearer <your_token>`
3. Find `POST /api/complaints/`
4. Click "Try it out"
5. Enter:
```json
{
  "title": "Fee Payment Issue",
  "description": "My semester fee was deducted but not credited to the account"
}
```
6. Click "Execute"

### Test 4: View Complaints

1. Find `GET /api/complaints/`
2. Click "Try it out"
3. Click "Execute"

## Project Structure

```
Student_Complaint_Classification_system/
├── backend/
│   ├── app/
│   │   ├── models/           # Database models
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Request/response schemas
│   │   ├── middleware/       # Authentication
│   │   ├── utils/            # Utilities
│   │   ├── main.py          # FastAPI app
│   │   └── database.py       # Database config
│   ├── venv/                # Virtual environment
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   ├── run_server.bat       # Windows startup
│   ├── run_server.ps1       # PowerShell startup
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   ├── package.json
│   ├── .env
│   ├── .env.example
│   ├── run_dev.bat          # Windows startup
│   ├── run_dev.ps1          # PowerShell startup
│   └── .gitignore
├── docs/
│   ├── api/
│   ├── architecture/
│   └── database/
├── README.md
├── SETUP_GUIDE.md
├── QUICKSTART.md
└── .gitignore
```

## Database Tables (Auto-created)

Tables are automatically created when the backend starts:
- ✅ `users` - User accounts
- ✅ `complaints` - Complaint submissions
- ✅ `complaint_comments` - Discussion threads
- ✅ `departments` - Department routing info

## API Endpoints (Phase 2 Complete)

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login & get JWT

### Complaints
- `POST /api/complaints/` - Submit complaint
- `GET /api/complaints/` - List complaints
- `GET /api/complaints/{id}` - Get details
- `PUT /api/complaints/{id}` - Update status
- `POST /api/complaints/{id}/comments` - Add comment

## Development Mode

Both servers run with auto-reload:
- **Backend**: Changes to Python files reload automatically
- **Frontend**: Changes to React files reload automatically

## Troubleshooting

### Port 8000 Already in Use
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Port 3000 Already in Use
```powershell
# Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Database Connection Failed
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database and user exist
- Check password is correct

### Virtual Environment Issues
```powershell
# Deactivate current venv
deactivate

# Remove and recreate
Remove-Item -Recurse venv
py -3.13 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### npm Issues
```powershell
# Clear cache and reinstall
npm cache clean --force
Remove-Item -Recurse node_modules
npm install
```

## Next: Phase 3 (ML Pipeline)

Ready to implement:
- TF-IDF vectorization
- Logistic Regression training
- Auto-classification on complaint submission
- Department routing logic
- Priority determination

See `README.md` for Phase 3 plan.

## Need Help?

1. Check `SETUP_GUIDE.md` for detailed setup
2. Review `docs/api/API_ENDPOINTS.md` for API reference
3. Check `docs/architecture/SYSTEM_ARCHITECTURE.md` for design
4. Review `docs/database/SCHEMA.md` for database structure

---

**Status**: Phase 1 & 2 ✅ Complete - Ready for Phase 3!
