# Student News System

<p align="center">
  <img src="static/images/logoPage.png" alt="Student News System Logo" width="200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-lightgrey.svg" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-3-green.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
</p>

<p align="center">
  A comprehensive Flask-based student news platform where admins can publish and manage news posts, while students can view, like, comment, and share articles.
</p>

## Screenshots

### Student Dashboard

<p align="center">
  <img src="static/images/logoPage.png" alt="Student Dashboard" width="800">
  <br><em>Student dashboard showing latest news posts with like and comment functionality</em>
</p>

### Admin Panel

<p align="center">
  <img src="static/images/logo.png" alt="Admin Dashboard" width="800">
  <br><em>Admin panel for managing posts, users, and analytics</em>
</p>

### Profile Management

<p align="center">
  <img src="static/images/logo.png" alt="Profile Page" width="400">
  <br><em>User profile page with customizable avatar and bio</em>
</p>

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

## Tech Stack

- **Backend**: Flask, SQLAlchemy ORM
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Security**: Bcrypt hashing
- **File Upload**: Secure file handling with validation
- **Frontend**: HTML5, Bootstrap, JavaScript (Vanilla)
- **Security**: CORS, Rate Limiting, Input validation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

\`\`\`bash
cd student-news-system
\`\`\`

### Step 2: Create Virtual Environment

\`\`\`bash

# On macOS/Linux

python3 -m venv venv
source venv/bin/activate

# On Windows

python -m venv venv
venv\Scripts\activate
\`\`\`

### Step 3: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

Or install manually:

\`\`\`bash
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended flask-cors flask-limiter flask-session python-dotenv
\`\`\`

### Step 4: Configure Environment (Optional)

Create a `.env` file in the root directory:

\`\`\`
JWT_SECRET_KEY=your-secret-key-here
SECRET_KEY=your-flask-secret-key-here
\`\`\`

### Step 5: Run the Application

\`\`\`bash
python app.py
\`\`\`

The application will start at `http://localhost:5000`

### Development Setup (Optional)

If you want to work with the Next.js components:

\`\`\`bash

# Install Node.js dependencies

npm install

# Start the Next.js development server

npm run dev
\`\`\`

### Database Setup

The application uses SQLite by default. To create initial admin and student users:

\`\`\`bash

# Create admin user

python create_admin.py

# Create sample student user

python create_student.py
\`\`\`

## Project Structure

\`\`\`
student-news-system/
├── app.py                      # Flask application factory
├── config.py                   # Configuration settings
├── models.py                   # Database models (User, Post, Comment, etc.)
├── extensions.py               # Flask extensions initialization
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies (for UI components)
├── tsconfig.json               # TypeScript configuration
├── postcss.config.mjs          # PostCSS configuration
├── tailwind.config.ts          # Tailwind CSS configuration
│
├── routes/
│   ├── auth_routes.py          # Authentication endpoints
│   ├── user_routes.py          # User profile endpoints
│   ├── post_routes.py          # Post CRUD endpoints
│   ├── admin_routes.py         # Admin management endpoints
│   ├── upload_routes.py        # File upload endpoints
│   └── analytics_routes.py     # Analytics endpoints
│
├── templates/
│   ├── base.html               # Base template with navigation
│   ├── index.html              # Landing page
│   ├── about.html              # About page
│   ├── contact.html            # Contact page
│   ├── library.html            # Library page
│   ├── study.html              # Study materials page
│   ├── international-study.html # International study page
│   ├── auth/
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Registration page
│   │   └── logout.html         # Logout confirmation page
│   ├── student/
│   │   ├── dashboard.html      # Student news feed
│   │   ├── home.html           # Student home page
│   │   └── profile.html        # Student profile
│   └── admin/
│       ├── dashboard.html      # Admin panel
│       └── analytics.html      # Analytics dashboard
│
├── static/
│   ├── css/
│   │   ├── style.css           # Main styles
│   │   ├── auth.css            # Auth page styles
│   │   ├── admin-style.css     # Admin panel styles
│   │   └── student-style.css   # Student dashboard styles
│   ├── js/
│   │   ├── main.js             # Frontend logic
│   │   ├── admin.js            # Admin panel JavaScript
│   │   └── student.js          # Student dashboard JavaScript
│   ├── images/                 # Static images (logos, etc.)
│   └── placeholder-user.jpg    # Default user avatar
│
├── uploads/                    # User uploaded files
│   ├── posts/                  # Post images
│   └── profiles/               # Profile pictures
│
├── instance/                   # Instance-specific data
│   └── database.db             # SQLite database
│
├── flask_session/              # Flask session files
├── components/                 # Reusable UI components (React/Next.js)
├── app/                        # Next.js app directory
├── lib/                        # Utility libraries
├── hooks/                      # React hooks
├── styles/                     # Additional styles
├── public/                     # Static assets for Next.js
│
├── .gitignore                  # Git ignore rules
├── create_admin.py             # Admin user creation script
├── create_student.py           # Student user creation script
├── log_parser.py               # Log parsing utilities
├── sample_logs.txt             # Sample log files
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

<p align="center">
  <img src="static/images/logo.png" alt="Registration Process" width="600">
</p>

1. Navigate to `http://localhost:5000/register`
2. Fill in Full Name, Email, and Password
3. Click "Create Account"
4. Login with your credentials

### Login as Admin

<p align="center">
  <img src="static/images/logoPage.png" alt="Admin Login" width="400">
</p>

1. Navigate to `http://localhost:5000/login`
2. Use admin credentials (created during setup)
3. Access admin dashboard at `/admin`

### Create a Post (Admin Only)

<p align="center">
  <img src="static/images/logo.png" alt="Create Post Interface" width="700">
</p>

1. Go to Admin Dashboard (`/admin`)
2. Click "Create Post"
3. Fill in title, content, category
4. Choose publish date (immediate or scheduled)
5. Click "Create Post"

### Browse Posts (Student)

<p align="center">
  <img src="static/images/logoPage.png" alt="Student Dashboard" width="800">
</p>

1. Login as student
2. Go to Student Dashboard (`/student`)
3. View news feed, use search, or filter by category
4. Click post to view full content
5. Like, comment, or share posts

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

### Issue: Database locked

**Solution**: Delete `database.db` and restart the app

### Issue: File upload fails

**Solution**: Ensure `static/uploads/` directory exists and is writable

### Issue: Login not working

**Solution**: Clear browser cookies and try again

### Issue: JWT token expired

**Solution**: Default token expires in 30 days. Login again to get a new token.

## Performance Tips

- Use pagination when fetching large post lists
- Enable database indexing on frequently searched columns
- Implement caching for trending posts
- Consider upgrading to PostgreSQL for production

## Future Enhancements

- Email notifications for important posts
- Search using full-text indexing
- Post recommendation engine
- Advanced analytics and reporting
- Mobile app integration
- Real-time notifications with WebSockets

## Development

### Running Tests

\`\`\`bash

# Run Flask tests (if implemented)

python -m pytest
\`\`\`

### Code Quality

\`\`\`bash

# Format code with black

black .

# Lint code with flake8

flake8 .

# Type check with mypy (if configured)

mypy .
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:

- Create an issue in the repository
- Contact: <support@studentnews.com>

## Acknowledgments

- Flask framework for the web application
- Bootstrap for responsive UI components
- SQLite for lightweight database management
- JWT for secure authentication

---

**Happy News Sharing!** 📰
