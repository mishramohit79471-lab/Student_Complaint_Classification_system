# API Endpoints Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication Endpoints

### 1. Register User
Create a new user account.

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "email": "student@example.com",
  "full_name": "John Doe",
  "password": "securepassword123",
  "role": "student"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "student@example.com",
  "full_name": "John Doe",
  "role": "student",
  "is_active": true,
  "created_at": "2026-09-28T10:30:00"
}
```

**Error Responses:**
- `400 Bad Request` - Email already registered or invalid data
- `422 Unprocessable Entity` - Validation error

---

### 2. Login User
Authenticate user and get JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "student@example.com",
    "full_name": "John Doe",
    "role": "student",
    "is_active": true,
    "created_at": "2026-09-28T10:30:00"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid email or password
- `403 Forbidden` - Account inactive

---

## Complaint Endpoints

### 3. Submit Complaint
Submit a new complaint (Students only).

**Endpoint:** `POST /complaints/`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "title": "Fee Payment Issue",
  "description": "My semester fee was deducted from my bank account but the college portal still shows payment pending. I have the transaction receipt."
}
```

**Response (201 Created):**
```json
{
  "id": 101,
  "student_id": 1,
  "title": "Fee Payment Issue",
  "description": "My semester fee was deducted...",
  "category": null,
  "assigned_department": null,
  "priority": "Medium",
  "status": "Submitted",
  "confidence_score": null,
  "resolution": null,
  "created_at": "2026-09-28T11:00:00",
  "updated_at": "2026-09-28T11:00:00",
  "comments": []
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing token
- `403 Forbidden` - User is not a student
- `422 Unprocessable Entity` - Validation error

---

### 4. Get Complaints List
Retrieve complaints based on user role.

**Endpoint:** `GET /complaints/?skip=0&limit=10&status_filter=Submitted`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `skip` (int, optional, default: 0) - Number of records to skip
- `limit` (int, optional, default: 10, max: 100) - Number of records to return
- `status_filter` (string, optional) - Filter by status (e.g., "Submitted", "Assigned")

**Response (200 OK):**
```json
[
  {
    "id": 101,
    "title": "Fee Payment Issue",
    "category": null,
    "priority": "Medium",
    "status": "Submitted",
    "created_at": "2026-09-28T11:00:00"
  },
  {
    "id": 102,
    "title": "Attendance Discrepancy",
    "category": null,
    "priority": "Low",
    "status": "Assigned",
    "created_at": "2026-09-28T12:30:00"
  }
]
```

**Role-Based Behavior:**
- **Student**: Returns only their own complaints
- **Department Staff**: Returns complaints assigned to their department
- **Admin**: Returns all complaints

---

### 5. Get Complaint Details
Retrieve full complaint information with comments.

**Endpoint:** `GET /complaints/{complaint_id}`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `complaint_id` (integer) - ID of the complaint

**Response (200 OK):**
```json
{
  "id": 101,
  "student_id": 1,
  "title": "Fee Payment Issue",
  "description": "My semester fee was deducted from my bank account but the college portal still shows payment pending.",
  "category": "Fee/Payment",
  "assigned_department": "Accounts",
  "priority": "High",
  "status": "Assigned",
  "confidence_score": 0.94,
  "resolution": null,
  "created_at": "2026-09-28T11:00:00",
  "updated_at": "2026-09-28T11:05:00",
  "comments": [
    {
      "id": 1,
      "user_id": 5,
      "comment_text": "We are looking into your payment records.",
      "created_at": "2026-09-28T11:05:00"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - No permission to view this complaint
- `404 Not Found` - Complaint not found

---

### 6. Update Complaint Status
Update complaint status and add resolution (Staff/Admin only).

**Endpoint:** `PUT /complaints/{complaint_id}`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `complaint_id` (integer) - ID of the complaint

**Request Body:**
```json
{
  "status": "Resolved",
  "resolution": "Fee has been credited to your account. Transaction ID: TXN123456"
}
```

**Response (200 OK):**
```json
{
  "id": 101,
  "student_id": 1,
  "title": "Fee Payment Issue",
  "description": "My semester fee was deducted from my bank account...",
  "category": "Fee/Payment",
  "assigned_department": "Accounts",
  "priority": "High",
  "status": "Resolved",
  "confidence_score": 0.94,
  "resolution": "Fee has been credited to your account. Transaction ID: TXN123456",
  "created_at": "2026-09-28T11:00:00",
  "updated_at": "2026-09-28T14:30:00",
  "comments": []
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid token
- `403 Forbidden` - User is not staff/admin
- `404 Not Found` - Complaint not found

---

### 7. Add Comment to Complaint
Add a comment or update to a complaint.

**Endpoint:** `POST /complaints/{complaint_id}/comments`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Path Parameters:**
- `complaint_id` (integer) - ID of the complaint

**Request Body:**
```json
{
  "comment_text": "Your fee has been processed. Please check your account within 24 hours."
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "message": "Comment added successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid token
- `404 Not Found` - Complaint not found

---

## Status Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - User lacks permission |
| 404 | Not Found - Resource not found |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error |

---

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication.

**How to authenticate:**
1. Call `/auth/login` to get access token
2. Include token in all subsequent requests:
   ```
   Authorization: Bearer {access_token}
   ```

**Token Format:**
- Type: JWT (JSON Web Token)
- Algorithm: HS256
- Expiration: 30 minutes (default)
- Contains: User email as "sub" claim

---

## Rate Limiting

Currently no rate limiting implemented. 

**Future Implementation:**
- 100 requests per minute per user
- 1000 requests per minute per IP

---

## Example Workflows

### Workflow 1: Student Submits and Tracks Complaint

```
1. POST /auth/login
   Request: {email, password}
   Response: {access_token, user}

2. POST /complaints/
   Headers: Authorization: Bearer {token}
   Request: {title, description}
   Response: {complaint with id}

3. GET /complaints/{complaint_id}
   Headers: Authorization: Bearer {token}
   Response: {full complaint details}

4. GET /complaints/
   Headers: Authorization: Bearer {token}
   Response: {list of student's complaints}
```

### Workflow 2: Staff Member Handles Complaint

```
1. POST /auth/login
   Request: {email, password}
   Response: {access_token, user with department_id}

2. GET /complaints/?status_filter=Assigned
   Headers: Authorization: Bearer {token}
   Response: {list of assigned complaints}

3. GET /complaints/{complaint_id}
   Headers: Authorization: Bearer {token}
   Response: {complaint details}

4. POST /complaints/{complaint_id}/comments
   Headers: Authorization: Bearer {token}
   Request: {comment_text}
   Response: {comment_id}

5. PUT /complaints/{complaint_id}
   Headers: Authorization: Bearer {token}
   Request: {status: "Resolved", resolution: "text"}
   Response: {updated complaint}
```

---

## Testing with cURL

### Register a User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "full_name": "John Doe",
    "password": "password123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "password123"
  }'
```

### Submit Complaint
```bash
curl -X POST "http://localhost:8000/api/complaints/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fee Payment Issue",
    "description": "My fee was deducted but not credited..."
  }'
```

### Get Complaints
```bash
curl -X GET "http://localhost:8000/api/complaints/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
