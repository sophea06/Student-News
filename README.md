# Student News System

A comprehensive full-stack student news platform with a Flask backend API and Next.js frontend. Admins can publish and manage news posts, while students can view, like, comment, and share articles through a modern React interface.

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

## Screenshots

### Landing Page

![Landing Page](public/placeholder.jpg)

### Student Dashboard

![Student Dashboard](static/images/logo.png)

### Admin Dashboard

![Admin Dashboard](static/images/logoPage.png)

### Login Page

![Login Page](public/placeholder.svg)

*Note: Replace placeholder images with actual screenshots of your application.*

## Architecture Diagram

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐    SQL    ┌─────────────────┐
│   Frontend      │◄────────────────►│   Flask API     │◄─────────►│   SQLite DB     │
│   (Next.js)     │                  │   Backend       │           │   Database      │
│                 │                  │                 │           │                 │
│ - React Components│                │ - Routes        │           │ - Users         │
│ - TypeScript     │                │ - Models        │           │ - Posts         │
│ - Tailwind CSS   │                │ - Authentication│           │ - Comments      │
│ - Radix UI       │                │ - File Uploads  │           │ - Analytics     │
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

- **Backend**: Flask, SQLAlchemy ORM
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Security**: Bcrypt hashing
- **File Upload**: Secure file handling with validation
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS, Radix UI components
- **Security**: CORS, Rate Limiting, Input validation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js 18 or higher
- npm or yarn or pnpm

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
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended flask-cors flask-limiter
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

- **Frontend**: Open `http://localhost:3000` in your browser
- **Backend API**: Available at `http://localhost:5000` (used by frontend)

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

- `POST /api/auth/register` - Register new student
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/profile` - Get current user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password

### Posts

- `GET /api/posts` - Get all posts with pagination
- `GET /api/posts/trending` - Get trending posts
- `GET /api/posts/<id>` - Get single post
- `POST /api/posts` - Create post (Admin/Editor only)
- `PUT /api/posts/<id>` - Edit post (Admin/Editor only)
- `DELETE /api/posts/<id>` - Delete post (Admin/Editor only)
- `POST /api/posts/<id>/like` - Like a post
- `POST /api/posts/<id>/unlike` - Unlike a post

### Comments

- `POST /api/posts/<id>/comments` - Add comment
- `GET /api/posts/<id>/comments` - Get post comments
- `DELETE /api/comments/<id>` - Delete comment
- `POST /api/comments/<id>/replies` - Reply to comment

### Admin

- `GET /api/admin/stats` - Dashboard statistics
- `GET /api/admin/users` - List all users
- `PUT /api/admin/users/<id>/block` - Block user
- `PUT /api/admin/users/<id>/unblock` - Unblock user
- `GET /api/admin/comments/pending` - Pending comments for moderation
- `PUT /api/admin/comments/<id>/approve` - Approve comment
- `PUT /api/admin/comments/<id>/reject` - Reject comment

### Analytics

- `GET /api/analytics/dashboard` - Analytics dashboard data
- `GET /api/analytics/posts/trending` - Trending posts analysis
- `GET /api/analytics/engagement` - User engagement metrics

## Usage Examples

### Register as a Student

1. Navigate to `http://localhost:3000` (Next.js frontend)
2. Click "Register" and fill in Full Name, Email, and Password
3. Click "Create Account"
4. Login with your credentials

### Login as Admin

1. Navigate to `http://localhost:3000/login`
2. Use admin credentials (created during setup)
3. Access admin dashboard through the navigation menu

### Create a Post (Admin Only)

1. Login as admin and access the admin dashboard
2. Click "Create Post" in the admin panel
3. Fill in title, content, category, and upload images if needed
4. Choose publish date (immediate or scheduled)
5. Click "Create Post"

### Browse Posts (Student)

1. Login as student at `http://localhost:3000`
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

## Environment Variables

Create a `.env` file with:

\`\`\`
JWT_SECRET_KEY=your-jwt-secret-key
SECRET_KEY=your-flask-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///database.db
UPLOAD_FOLDER=static/uploads
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

## Future Enhancements

- Email notifications for important posts
- Search using full-text indexing
- Post recommendation engine
- Advanced analytics and reporting
- Mobile app integration
- Real-time notifications with WebSockets

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Happy News Sharing!** 📰
