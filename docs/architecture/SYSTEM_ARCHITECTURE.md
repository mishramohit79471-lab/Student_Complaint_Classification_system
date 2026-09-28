# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────┐          │
│  │  Student   │  │  Department  │  │   Admin     │          │
│  │  Portal    │  │   Dashboard  │  │  Dashboard  │          │
│  └────────────┘  └──────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                            ↓ (HTTP/REST)
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  CORS | Rate Limiting | Authentication | Logging     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Route Layer (FastAPI Routers)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Auth       │  │  Complaints  │  │ Departments  │       │
│  │   Routes     │  │   Routes     │  │   Routes     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           Business Logic Layer (Services)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Auth       │  │ Complaint    │  │ ML/ML        │       │
│  │   Service    │  │ Service      │  │ Service      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│             Data Access Layer (SQLAlchemy ORM)               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   Models: User | Complaint | Department | Comment    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 PostgreSQL Database                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tables: users | complaints | comments | departments │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React)
- **Student Portal**: Complaint submission, status tracking
- **Department Dashboard**: View and manage assigned complaints
- **Admin Dashboard**: System-wide monitoring and analytics
- **Auth Pages**: Login and registration

### Backend (FastAPI)
- **API Gateway**: Entry point for all requests
- **Route Layer**: Handles HTTP methods and request routing
- **Service Layer**: Contains business logic
- **Data Access Layer**: ORM interactions

### Database (PostgreSQL)
- **Users Table**: Student and staff information
- **Complaints Table**: Complaint details, classification, routing
- **Comments Table**: Discussion and resolution notes
- **Departments Table**: Department information

## Data Flow

### Complaint Submission Flow
```
1. Student enters complaint text in form
2. Frontend validates and sends to POST /api/complaints/
3. Backend receives request with JWT token
4. Auth middleware validates token
5. Complaint Service creates complaint record
6. ML Service processes text (Phase 3)
   - Vectorizes text (TF-IDF)
   - Predicts category
   - Determines confidence score
   - Maps category to department
   - Sets priority level
7. Complaint record updated with classification
8. Database stores complaint
9. Response returned to frontend
10. Student redirected to complaint tracking page
```

### Complaint Tracking Flow
```
1. Student views complaints page
2. Frontend requests GET /api/complaints/
3. Backend filters complaints by student_id
4. Returns list of complaints with status
5. Student clicks on complaint for details
6. Frontend requests GET /api/complaints/{id}
7. Backend returns full complaint with comments
8. Student sees classification, department, priority, status
```

### Department Staff Workflow
```
1. Staff logs in with department credentials
2. Frontend requests GET /api/complaints/ (filtered by department)
3. Backend returns assigned complaints
4. Staff can:
   - View complaint details
   - Filter by priority/status
   - Add comments
   - Update status
   - Resolve complaint
5. Updates are stored and student is notified (Phase 4)
```

## Authentication Flow

```
1. User registers with email/password
2. Password is hashed with bcrypt
3. User record stored in database
4. User logs in with email/password
5. Credentials validated against stored hash
6. JWT token generated with user email as "sub" claim
7. Token returned to frontend
8. Frontend stores token in localStorage
9. Subsequent requests include token in Authorization header
10. Middleware validates token and extracts user info
11. User's role determines what operations they can perform
```

## API Design

### RESTful Endpoints
- **GET** - Retrieve resources
- **POST** - Create resources
- **PUT/PATCH** - Update resources
- **DELETE** - Delete resources

### Status Codes
- **200** - Success
- **201** - Created
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **500** - Server Error

### Request/Response Format
- **Content-Type**: application/json
- **Auth Header**: Authorization: Bearer {token}

## Security Architecture

### Authentication
- JWT tokens for stateless authentication
- Token expiration (30 minutes default)
- Refresh token mechanism (Phase 3)

### Authorization
- Role-based access control (RBAC)
- Endpoint-level authorization
- Row-level security (students can only see own complaints)

### Data Protection
- Passwords hashed with bcrypt
- Environment variables for secrets
- HTTPS ready (Production)
- CORS configured for frontend

## Scalability Considerations

### Current Design
- Single database instance
- Monolithic backend
- Simple JWT auth

### Future Improvements
- Horizontal scaling of API servers
- Database read replicas
- Caching layer (Redis)
- Message queue for async processing
- ML model versioning and A/B testing
- Microservices for ML pipeline
