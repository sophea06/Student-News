# Student News System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-green.svg)](https://www.sqlite.org/)

A comprehensive full-stack student news platform built with Flask backend and Jinja2 templates. Features a modern, responsive design with role-based access control. Admins can publish and manage news posts, while students can view, like, comment, and share articles through an intuitive web interface with real-time notifications.

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Architecture Diagram](#architecture-diagram)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [User Roles & Permissions](#user-roles--permissions)
- [Security Features](#security-features)
- [Database Models](#database-models)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Performance Tips](#performance-tips)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## Features

### Core Features

- **User Authentication**: Secure login/registration with JWT tokens and password hashing (Bcrypt)
- **Multi-role System**: Admin, Editor, Moderator, and Student roles with different permissions
- **Post Management**: Create, edit, delete, and manage posts with categories and scheduling
- **Student Engagement**: Like, comment, and share posts with real-time notifications
- **User Profiles**: Customizable student profiles with bio, profile pictures, and follower system

### Advanced Features

- **Pagination & Filtering**: Browse posts with search, category filters, and sorting
- **Post Scheduling**: Schedule posts to publish at future dates
- **Draft Posts**: Save posts as drafts before publishing
- **Comment Moderation**: Admin approval system for student comments
- **Threaded Comments**: Reply to comments with nested discussion threads
- **File Uploads**: Support for images, documents, and profile pictures
- **Trending Posts**: View popular posts based on engagement metrics
- **Analytics Dashboard**: Track user engagement, view counts, and activity metrics
- **Rate Limiting**: Prevent spam with intelligent rate limiting on API endpoints
- **Soft Delete**: Archive posts instead of permanently deleting them

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd student-news-system

# Backend setup
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Frontend setup (if using Next.js)
npm install

# Run the application
python app.py
# In another terminal: npm run dev
```

Visit `http://localhost:5000` to access the application.

## Screenshots

### Landing Page

![Landing Page](public/placeholder.jpg)

*The main landing page showcasing featured news posts and navigation options for students and administrators.*

### Student Dashboard

![Student Dashboard](static/images/logo.png)

*Student dashboard displaying the news feed, recent posts, trending articles, and user engagement features.*

### Admin Dashboard

![Admin Dashboard](static/images/logoPage.png)

*Administrative control panel with analytics, user management, post moderation, and system statistics.*

### Login Page

![Login Page](public/placeholder.svg)

*Secure authentication page supporting multiple user roles with JWT-based session management.*

*Note: Replace placeholder images with actual screenshots of your application.*

## Architecture Diagram

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐    SQL    ┌─────────────────┐
│   Frontend      │◄────────────────►│   Flask API     │◄─────────►│   SQLite DB     │
│   (Jinja2)      │                  │   Backend       │           │   Database      │
│                 │                  │                 │           │                 │
│ - HTML Templates│                  │ - Routes        │           │ - Users         │
│ - Bootstrap/CSS │                  │ - Models        │           │ - Posts         │
│ - JavaScript    │                  │ - Authentication│           │ - Comments      │
│ - AJAX          │                  │ - File Uploads  │           │ - Analytics     │
└─────────────────┘                  └─────────────────┘           └─────────────────┘
          │                                   │
          │                                   │
          ▼                                   ▼
┌─────────────────┐                  ┌─────────────────┐
│   Static Assets │                  │   Session Store  │
│   (Images, CSS) │                  │   (Flask-Session)│
└─────────────────┘                  └─────────────────┘
```

## Tech Stack

- **Backend**: Flask, SQLAlchemy ORM, Flask-JWT-Extended
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens) with Bcrypt password hashing
- **File Upload**: Secure file handling with validation and Flask-Uploads
- **Frontend**: Jinja2 templates with Bootstrap/CSS, JavaScript (ES6+)
- **Security**: Flask-CORS, Flask-Limiter, Input validation, CSRF protection
- **Session Management**: Flask-Session for server-side sessions
- **Development**: Python 3.8+, pip, virtualenv

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js 18 or higher (optional, for Next.js frontend)
- npm, yarn, or pnpm (optional, for Next.js frontend)

### Version Check Commands

```bash
# Check Python version
python --version

# Check pip version
pip --version

# Check Node.js version (if using Next.js)
node --version

# Check npm version (if using Next.js)
npm --version
```

### Step 1: Clone or Download the Project

\`\`\`bash
cd student-news-system
\`\`\`

### Step 2: Backend Setup (Flask)

#### Create Virtual Environment

\`\`\`bash

# On macOS/Linux

python3 -m venv venv
source venv/bin/activate

# On Windows

python -m venv venv
venv\Scripts\activate
\`\`\`

#### Install Python Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

Or install manually:

\`\`\`bash
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended flask-cors flask-limiter flask-session python-dotenv
\`\`\`

#### Configure Environment (Optional)

Create a `.env` file in the root directory:

\`\`\`
JWT_SECRET_KEY=your-secret-key-here
SECRET_KEY=your-flask-secret-key-here
\`\`\`

### Step 3: Frontend Setup (Next.js)

#### Install Node.js Dependencies

\`\`\`bash

# Using npm

npm install

# Using yarn

yarn install

# Using pnpm

pnpm install
\`\`\`

### Step 4: Run the Applications

#### Start the Backend (Flask API)

\`\`\`bash

# Make sure virtual environment is activated

python app.py
\`\`\`

The Flask API will start at `http://localhost:5000`

#### Start the Frontend (Next.js)

\`\`\`bash

# Using npm

npm run dev

# Using yarn

yarn dev

# Using pnpm

pnpm dev
\`\`\`

The Next.js frontend will start at `http://localhost:3000`

### Step 5: Access the Application

- **Application**: Open `http://localhost:5000` in your browser
- **API Endpoints**: Available at `http://localhost:5000/api/*` (JSON responses)

### Step 6: Create Admin User (Optional)

To create an initial admin user, run the following command after starting the Flask app:

\`\`\`bash
python create_admin.py
\`\`\`

This will prompt you to enter admin details and create the first admin account.

### Step 7: Create Sample Student (Optional)

To create a sample student user for testing:

\`\`\`bash
python create_student.py
\`\`\`

This creates a test student account with predefined credentials.

## Project Structure

\`\`\`
student-news-system/
├── app.py                      # Flask application factory and entry point
├── config.py                   # Configuration settings
├── models.py                   # Database models (User, Post, Comment, etc.)
├── extensions.py               # Flask extensions initialization
├── create_admin.py             # Script to create initial admin user
├── create_student.py           # Script to create sample student user
├── log_parser.py               # Log parsing utilities
├── sample_logs.txt             # Sample log file for testing
├── requirements.txt            # Python dependencies (not shown, but referenced)
├── package.json                # Node.js dependencies and scripts
├── pnpm-lock.yaml              # PNPM lock file
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind CSS configuration (not shown)
├── postcss.config.mjs          # PostCSS configuration
├── .gitignore                  # Git ignore file
│
├── routes/                     # Flask API routes
│   ├── **init**.py            # Routes package init
│   ├── auth_routes.py         # Authentication endpoints
│   ├── user_routes.py         # User profile endpoints
│   ├── post_routes.py         # Post CRUD endpoints
│   ├── admin_routes.py        # Admin management endpoints
│   ├── upload_routes.py       # File upload endpoints
│   └── analytics_routes.py    # Analytics endpoints
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── auth/
│   │   ├── login.html         # Login page
│   │   ├── register.html      # Registration page
│   │   └── logout.html        # Logout confirmation page
│   ├── student/
│   │   ├── dashboard.html     # Student news feed
│   │   ├── home.html          # Student home page
│   │   └── profile.html       # Student profile page
│   └── admin/
│       ├── dashboard.html     # Admin panel
│       └── analytics.html     # Analytics dashboard
│
├── static/                     # Static files for Flask
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   ├── admin-style.css    # Admin page styles
│   │   └── auth.css           # Auth page styles
│   ├── js/
│   │   ├── main.js            # Frontend logic
│   │   ├── admin.js           # Admin page logic
│   │   └── student.js         # Student page logic
│   ├── images/                # Static images
│   │   ├── logo.png           # Main logo
│   │   └── logoPage.png       # Page logo
│   └── uploads/               # User uploaded files (placeholder)
│
├── app/                        # Next.js application directory
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout component
│   ├── page.tsx               # Home page component
│   └── components/            # Reusable React components
│       ├── ui/                # Radix UI components (accordion, button, etc.)
│       └── theme-provider.tsx # Theme provider
│
├── components/                 # Shared UI components (Next.js)
├── hooks/                      # Custom React hooks
├── lib/                        # Utility functions
├── styles/                     # Additional styles
├── public/                     # Static assets for Next.js
│   ├── apple-icon.png         # Apple touch icon
│   ├── icon-dark-32x32.png    # Dark mode icon
│   ├── icon-light-32x32.png   # Light mode icon
│   ├── icon.svg               # SVG icon
│   ├── placeholder-logo.png   # Placeholder logo
│   ├── placeholder-logo.svg   # SVG placeholder logo
│   ├── placeholder.jpg        # Placeholder image
│   ├── placeholder.svg        # SVG placeholder
│   └── student-news-logo.svg  # Student news logo
│
├── uploads/                    # User uploaded files
│   ├── posts/                 # Post images
│   └── profiles/              # Profile pictures
│
├── flask_session/              # Flask session files (auto-generated)
├── instance/                   # Flask instance folder
│   └── database.db            # SQLite database
│
└── README.md                   # This file
\`\`\`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register` | Register new student | No |
| `POST` | `/api/auth/login` | Login user | No |
| `POST` | `/api/auth/logout` | Logout user | Yes |
| `GET` | `/api/auth/profile` | Get current user profile | Yes |
| `PUT` | `/api/auth/profile` | Update user profile | Yes |
| `POST` | `/api/auth/change-password` | Change password | Yes |

### Posts

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/posts` | Get all posts with pagination | No |
| `GET` | `/api/posts/trending` | Get trending posts | No |
| `GET` | `/api/posts/<id>` | Get single post | No |
| `POST` | `/api/posts` | Create post (Admin/Editor only) | Yes |
| `PUT` | `/api/posts/<id>` | Edit post (Admin/Editor only) | Yes |
| `DELETE` | `/api/posts/<id>` | Delete post (Admin/Editor only) | Yes |
| `POST` | `/api/posts/<id>/like` | Like a post | Yes |
| `POST` | `/api/posts/<id>/unlike` | Unlike a post | Yes |

### Comments

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/posts/<id>/comments` | Add comment | Yes |
| `GET` | `/api/posts/<id>/comments` | Get post comments | No |
| `DELETE` | `/api/comments/<id>` | Delete comment | Yes |
| `POST` | `/api/comments/<id>/replies` | Reply to comment | Yes |

### Admin

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/admin/stats` | Dashboard statistics | Admin |
| `GET` | `/api/admin/users` | List all users | Admin |
| `PUT` | `/api/admin/users/<id>/block` | Block user | Admin |
| `PUT` | `/api/admin/users/<id>/unblock` | Unblock user | Admin |
| `GET` | `/api/admin/comments/pending` | Pending comments for moderation | Admin |
| `PUT` | `/api/admin/comments/<id>/approve` | Approve comment | Admin |
| `PUT` | `/api/admin/comments/<id>/reject` | Reject comment | Admin |

### Analytics

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/analytics/dashboard` | Analytics dashboard data | Admin |
| `GET` | `/api/analytics/posts/trending` | Trending posts analysis | Admin |
| `GET` | `/api/analytics/engagement` | User engagement metrics | Admin |

### API Examples

#### Register a new student

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Get posts with pagination

```bash
curl -X GET "http://localhost:5000/api/posts?page=1&per_page=10&category=news"
```

#### Create a post (Admin/Editor only)

```bash
curl -X POST http://localhost:5000/api/posts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Campus Event",
    "content": "Details about the upcoming event...",
    "category": "events"
  }'
```

## Usage Examples

### Register as a Student

1. Navigate to `http://localhost:5000/register`
2. Fill in Full Name, Email, and Password
3. Click "Create Account"
4. Login with your credentials at `http://localhost:5000/login`

### Login as Admin

1. Navigate to `http://localhost:5000/login`
2. Use admin credentials (created during setup)
3. Access admin dashboard at `http://localhost:5000/admin`

### Create a Post (Admin Only)

1. Login as admin and access the admin dashboard
2. Click "Create Post" in the admin panel
3. Fill in title, content, category, and upload images if needed
4. Choose publish date (immediate or scheduled)
5. Click "Create Post"

### Browse Posts (Student)

1. Login as student at `http://localhost:5000/student`
2. View the news feed on the main dashboard
3. Use search, filters, or categories to find specific posts
4. Click on a post to view full content
5. Like, comment, or share posts using the interactive buttons

## User Roles & Permissions

| Action | Student | Editor | Moderator | Admin |
|--------|---------|--------|-----------|-------|
| View Posts | ✓ | ✓ | ✓ | ✓ |
| Create Posts | ✗ | ✓ | ✗ | ✓ |
| Edit Posts | ✗ | Own | ✗ | All |
| Delete Posts | ✗ | Own | ✗ | ✓ |
| Moderate Comments | ✗ | ✗ | ✓ | ✓ |
| Manage Users | ✗ | ✗ | ✗ | ✓ |
| View Analytics | ✗ | ✗ | ✗ | ✓ |

## Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: Prevent brute force attacks and spam
  - 5 registrations per hour
  - 10 login attempts per minute
  - 30 likes per minute per user
  - 20 comments per minute per user
- **CORS Protection**: Cross-Origin Resource Sharing configured
- **Input Validation**: All user inputs validated and sanitized
- **File Validation**: Upload file type and size restrictions

## Database Models

### User

- id, email, full_name, password_hash, bio, profile_picture
- role (student, editor, moderator, admin)
- is_blocked, created_at, updated_at

### Post

- id, title, content, category, author_id, image_url
- status (draft, published, archived)
- scheduled_at, published_at, view_count, share_count
- is_pinned, is_deleted

### Comment

- id, content, post_id, user_id, parent_id (for replies)
- status (pending, approved, rejected)
- created_at, updated_at

### Like

- id, post_id, user_id, created_at

### Notification

- id, user_id, message, type, is_read, created_at

## Development

### Running in Development Mode

```bash
# Activate virtual environment
venv\Scripts\activate

# Set environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run the application
python app.py
```

### Code Style and Linting

```bash
# Install development dependencies
pip install flake8 black isort

# Run linting
flake8 .

# Format code
black .

# Sort imports
isort .
```

### Testing

#### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html
```

#### Writing Tests

Tests are located in the `tests/` directory. Use pytest fixtures for database setup and teardown.

## Environment Variables

Create a `.env` file in the root directory:

\`\`\`
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-flask-secret-key-here

# Database Configuration
SQLALCHEMY_DATABASE_URI=sqlite:///instance/database.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Session Configuration
SESSION_TYPE=filesystem
SESSION_PERMANENT=False
\`\`\`

## Troubleshooting

### Backend (Flask) Issues

#### Database locked

**Solution**: Delete `instance/database.db` and restart the Flask app

#### File upload fails

**Solution**: Ensure `static/uploads/`, `uploads/posts/`, and `uploads/profiles/` directories exist and are writable

#### Login not working

**Solution**: Clear browser cookies and try again. Check if virtual environment is activated.

#### JWT token expired

**Solution**: Default token expires in 30 days. Login again to get a new token

#### Session issues

**Solution**: Clear the `flask_session/` directory and restart the app

### Frontend (Next.js) Issues

#### Port 3000 already in use

**Solution**: Kill the process using port 3000 or change the port in `package.json`

#### API connection failed

**Solution**: Ensure Flask backend is running on `http://localhost:5000` and CORS is configured

#### Build errors

**Solution**: Run `npm install` or `pnpm install` to ensure all dependencies are installed

#### TypeScript errors

**Solution**: Check `tsconfig.json` configuration and ensure all types are properly imported

### General Issues

#### Both applications won't start

**Solution**: Check that Python virtual environment is activated for Flask and Node.js is installed for Next.js

#### Database migration issues

**Solution**: Delete the database file and restart Flask to recreate tables

#### Permission errors

**Solution**: Ensure the application has write permissions to `uploads/`, `flask_session/`, and `instance/` directories

#### Admin creation fails

**Solution**: Run `python create_admin.py` with proper Python environment activated

#### Log parsing issues

**Solution**: Check `sample_logs.txt` format and ensure `log_parser.py` is working correctly

## Performance Tips

- Use pagination when fetching large post lists
- Enable database indexing on frequently searched columns (title, category, author_id)
- Implement caching for trending posts and user sessions
- Consider upgrading to PostgreSQL for production deployments
- Optimize image uploads by implementing compression and resizing
- Use CDN for static assets in production
- Implement database connection pooling for better concurrency
- Monitor API endpoints with rate limiting and logging

## Deployment

### Production Deployment

#### Using Gunicorn (Recommended)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

#### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

```bash
# Build and run
docker build -t student-news-system .
docker run -p 5000:5000 student-news-system
```

#### Environment Setup for Production

```bash
# Set production environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export JWT_SECRET_KEY=your-production-jwt-key
export SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/dbname
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Future Enhancements

- Email notifications for important posts
- Search using full-text indexing
- Post recommendation engine
- Advanced analytics and reporting
- Mobile app integration
- Real-time notifications with WebSockets
- Social media integration
- Advanced user permissions and roles
- Content moderation with AI
- Multi-language support

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Write tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask framework and its amazing community
- SQLAlchemy for the powerful ORM
- All contributors and users of this project

## Support

- 📧 **Email**: For support inquiries
- 🐛 **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 **Documentation**: This README and inline code documentation

---

**Happy News Sharing!** 📰

*Built with ❤️ for the student community*
