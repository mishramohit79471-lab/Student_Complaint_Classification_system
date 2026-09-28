# Student Complaint Classification & Department Routing System

An AI-powered full-stack system for automatic complaint classification and intelligent department routing.

## Features

- **Student Complaint Submission**: Easy-to-use interface for students to submit complaints
- **AI-Powered Classification**: Automatic categorization using TF-IDF + Logistic Regression
- **Department Routing**: Intelligent routing to appropriate departments
- **Priority Assignment**: Dynamic priority determination based on complaint analysis
- **Status Tracking**: Real-time complaint status tracking for students
- **Department Dashboard**: View and manage assigned complaints
- **Admin Analytics**: Comprehensive system monitoring and analytics
- **Role-Based Access**: Three user roles (Student, Department Staff, Admin)

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **ML/AI**: Scikit-learn (TF-IDF, Logistic Regression)

### Frontend
- **Framework**: React.js
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

### Infrastructure
- **Version Control**: Git
- **API Documentation**: Swagger/OpenAPI

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── models/           # SQLAlchemy models
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── middleware/       # Authentication middleware
│   │   ├── services/         # Business logic
│   │   ├── utils/            # Security and utilities
│   │   ├── main.py          # FastAPI app initialization
│   │   └── database.py       # Database configuration
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   ├── context/          # React context
│   │   ├── utils/            # Utility functions
│   │   └── styles/           # CSS files
│   ├── package.json
│   └── .env.example
├── docs/
│   ├── architecture/         # Architecture documentation
│   ├── api/                  # API documentation
│   └── database/             # Database schema docs
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
# Create tables (automatic on app start)
python -m uvicorn app.main:app --reload
```

6. Access API documentation:
```
http://localhost:8000/docs
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env if needed
```

4. Start development server:
```bash
npm start
```

5. Access the application:
```
http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Complaints
- `POST /api/complaints/` - Submit new complaint
- `GET /api/complaints/` - Get complaints (filtered by role)
- `GET /api/complaints/{id}` - Get complaint details
- `PUT /api/complaints/{id}` - Update complaint status
- `POST /api/complaints/{id}/comments` - Add comment to complaint

## User Roles

### Student
- Register and login
- Submit complaints
- View their own complaints
- Track complaint status
- View assigned department and priority

### Department Staff
- Login to dashboard
- View assigned complaints
- Filter and search complaints
- Update complaint status
- Add comments and resolution
- Mark complaints as resolved

### Admin
- Access admin dashboard
- View all complaints
- Monitor system analytics
- Reassign complaints
- Manage departments and users

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/db_name
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Authentication**: Stateless authentication with JWT tokens
- **CORS**: Configured cross-origin resource sharing
- **Environment Variables**: Secrets stored in .env files
- **Role-Based Access Control**: Endpoint access restricted by user role

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Use Prettier for code formatting

## Next Phases

### Phase 3: ML Pipeline
- Train classification model
- Integrate predictions into complaint flow
- Add priority determination logic

### Phase 4: Frontend UI
- Authentication pages
- Student complaint form
- Department dashboard
- Admin analytics dashboard

### Phase 5: Testing & Deployment
- Integration testing
- API testing with Postman/Swagger
- Performance optimization
- Production deployment

## Database Schema

See `docs/database/` for detailed schema documentation.

## API Documentation

See `docs/api/` for detailed API documentation.

## Architecture

See `docs/architecture/` for system architecture documentation.

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Create a pull request

## License

This project is part of a portfolio project for educational purposes.

## Support

For issues and questions, please open an issue on GitHub.

---

**Status**: Phase 1-2 Complete (Project Setup & Core Backend)
**Last Updated**: 2026-09-28
