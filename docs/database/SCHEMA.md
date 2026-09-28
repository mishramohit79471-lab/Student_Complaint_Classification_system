# Database Schema

## Tables

### users
Stores user information for students, department staff, and admins.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    full_name VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role ENUM('student', 'department_staff', 'admin') DEFAULT 'student',
    department_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Unique user identifier
- `email`: User's email address (unique)
- `full_name`: User's full name
- `hashed_password`: Bcrypt-hashed password
- `role`: User role (student, department_staff, admin)
- `department_id`: Foreign key to department (for staff)
- `is_active`: Account activation status
- `created_at`: User creation timestamp
- `updated_at`: Last update timestamp

**Indexes:**
- `email` (UNIQUE)

---

### complaints
Main table for storing complaint information and classification results.

```sql
CREATE TABLE complaints (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description TEXT NOT NULL,
    category ENUM(...) NULL,
    assigned_department VARCHAR NULL,
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    status ENUM('Submitted', 'Assigned', 'In Progress', 'Resolved', 'Closed') DEFAULT 'Submitted',
    confidence_score FLOAT NULL,
    resolution TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_to INTEGER NULL,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id)
);
```

**Fields:**
- `id`: Unique complaint identifier
- `student_id`: FK to student who submitted complaint
- `title`: Complaint title (summary)
- `description`: Full complaint description
- `category`: Predicted complaint category
- `assigned_department`: Department responsible for handling
- `priority`: Complaint priority level
- `status`: Current workflow status
- `confidence_score`: ML classification confidence (0-1)
- `resolution`: Resolution notes
- `created_at`: Submission timestamp
- `updated_at`: Last modification timestamp
- `assigned_to`: Staff member handling complaint

**Categories:**
- Fee/Payment
- Attendance
- Academic
- Technical/IT
- Hostel
- Infrastructure/Maintenance
- Examination
- Scholarship
- Library
- Transport
- Student Welfare
- Other

**Indexes:**
- `student_id`
- `status`
- `priority`
- `category`

---

### complaint_comments
Stores comments and discussion on complaints.

```sql
CREATE TABLE complaint_comments (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Fields:**
- `id`: Unique comment identifier
- `complaint_id`: FK to complaint
- `user_id`: FK to user who commented
- `comment_text`: Comment content
- `created_at`: Comment timestamp

**Indexes:**
- `complaint_id`
- `user_id`

---

### departments
Stores department information for routing.

```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields:**
- `id`: Unique department identifier
- `name`: Department name (unique)
- `description`: Department description
- `created_at`: Creation timestamp

**Sample Data:**
- Accounts (Fee/Payment)
- Academic Department (Attendance, Academic)
- IT Support (Technical/IT)
- Hostel Department (Hostel)
- Maintenance (Infrastructure)
- Examination Cell (Examination)
- Student Welfare (Scholarship, Library)
- Transport Department (Transport)
- Admin (Other)

**Indexes:**
- `name` (UNIQUE)

---

## Relationships

```
users (1) ─────────────(N) complaints (student)
         (1) ─────────────(N) complaints (assigned_to)
         (1) ─────────────(N) complaint_comments

departments (1) ─────────────(N) users (department_id)

complaints (1) ─────────────(N) complaint_comments
```

---

## Sample Data

### Initial Departments
```python
departments = [
    {"name": "Accounts", "description": "Fee/Payment Related"},
    {"name": "Academic Department", "description": "Attendance/Academic"},
    {"name": "IT Support", "description": "Technical Issues"},
    {"name": "Hostel Department", "description": "Hostel Related"},
    {"name": "Maintenance", "description": "Infrastructure/Maintenance"},
    {"name": "Examination Cell", "description": "Examination Related"},
    {"name": "Student Welfare", "description": "Scholarship/Library"},
    {"name": "Transport Department", "description": "Transport Issues"},
    {"name": "Admin", "description": "Other/General"},
]
```

---

## Views (Future)

### active_complaints
```sql
CREATE VIEW active_complaints AS
SELECT * FROM complaints
WHERE status IN ('Submitted', 'Assigned', 'In Progress');
```

### department_workload
```sql
CREATE VIEW department_workload AS
SELECT 
    assigned_department,
    COUNT(*) as total_complaints,
    SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) as resolved,
    AVG(CASE 
        WHEN status = 'Resolved' THEN EXTRACT(DAY FROM updated_at - created_at)
        ELSE NULL
    END) as avg_resolution_days
FROM complaints
GROUP BY assigned_department;
```

---

## Migration Strategy

1. **Phase 1**: Initial schema creation (done)
2. **Phase 2**: Add indexes and constraints
3. **Phase 3**: Add ML model version tracking table
4. **Phase 4**: Add notification audit log
5. **Phase 5**: Add analytics materialized views
