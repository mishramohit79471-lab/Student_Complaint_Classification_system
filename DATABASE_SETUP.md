# Database Setup Guide - PostgreSQL

The automatic setup script failed because PostgreSQL requires a password for the `postgres` user that was configured during installation.

## Option 1: Using pgAdmin (Recommended - GUI)

pgAdmin is usually installed with PostgreSQL on Windows.

### Steps:

1. **Open pgAdmin**
   - Search for "pgAdmin 4" in Windows Start Menu
   - Click to open

2. **Create Database**
   - Right-click "Databases" → Create → Database
   - Name: `complaint_db`
   - Click "Save"

3. **Create Login Role**
   - Right-click "Login/Group Roles" → Create → Login/Group Role
   - Name: `complaint_user`
   - Password: `complaint_user_123`
   - In "Privileges" tab:
     - Can login? ON
     - Create databases? OFF
   - Click "Save"

4. **Grant Privileges**
   - Right-click on `complaint_db` → Properties → Security
   - Find `complaint_user` and grant all privileges

5. **Verify Connection**
   - In pgAdmin, add a new connection with:
     - Host: localhost
     - Database: complaint_db
     - Username: complaint_user
     - Password: complaint_user_123

### Result:
```
Database: complaint_db
User: complaint_user
Password: complaint_user_123
```

---

## Option 2: Using Command Line (psql)

If you know the postgres password:

1. **Open Command Prompt (Run as Administrator)**

2. **Connect to PostgreSQL**
   ```cmd
   "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -h localhost
   ```
   - When prompted, enter the postgres password (set during installation)

3. **Create Database and User**
   ```sql
   CREATE DATABASE complaint_db;
   CREATE USER complaint_user WITH PASSWORD 'complaint_user_123';
   GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;
   \q
   ```

---

## Option 3: Reset PostgreSQL Password

If you forgot the postgres password:

1. **Stop PostgreSQL Service**
   ```powershell
   Stop-Service -Name postgresql-x64-17
   ```

2. **Edit pg_hba.conf**
   - Path: `C:\Program Files\PostgreSQL\17\data\pg_hba.conf`
   - Find the line with `host    all             all             127.0.0.1/32            md5`
   - Change `md5` to `trust`
   - Save the file

3. **Start PostgreSQL**
   ```powershell
   Start-Service -Name postgresql-x64-17
   ```

4. **Connect without Password**
   ```cmd
   "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -h localhost
   ```

5. **Reset Password**
   ```sql
   ALTER USER postgres WITH PASSWORD 'your_new_password';
   CREATE DATABASE complaint_db;
   CREATE USER complaint_user WITH PASSWORD 'complaint_user_123';
   GRANT ALL PRIVILEGES ON DATABASE complaint_db TO complaint_user;
   \q
   ```

6. **Restore pg_hba.conf**
   - Change `trust` back to `md5` in pg_hba.conf
   - Save and restart PostgreSQL

---

## Configuration File

Once you create the database and user, update `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://complaint_user:complaint_user_123@localhost:5432/complaint_db
SECRET_KEY=your-very-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

---

## Verification

Test the connection:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python
```

Then in Python:
```python
from app.database import engine
with engine.connect() as conn:
    print("✓ Database connection successful!")
```

---

## Next Steps

Once configured:
1. Start backend: `python -m uvicorn app.main:app --reload`
2. Tables auto-create on startup
3. Test via: http://localhost:8000/docs

---

## Troubleshooting

### "FATAL:  password authentication failed"
- Verify username: `complaint_user`
- Verify password: `complaint_user_123`
- Check DATABASE_URL in `.env`

### "database complaint_db does not exist"
- Create the database in pgAdmin or psql
- Database name must be exactly: `complaint_db`

### "role complaint_user does not exist"
- Create the user in pgAdmin or psql
- Ensure it has login privileges

---

Need help? Run this after setup:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python create_db.py  # Will try to verify connection
```
