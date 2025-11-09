# Student News System

A comprehensive Flask-based student news platform where admins can publish and manage news posts, while students can view, like, comment, and share articles.

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
pip install flask flask-sqlalchemy flask-bcrypt flask-jwt-extended flask-cors flask-limiter
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

## Project Structure

\`\`\`
student-news-system/
├── app.py                      # Flask application factory
├── config.py                   # Configuration settings
├── models.py                   # Database models (User, Post, Comment, etc.)
├── requirements.txt            # Python dependencies
│
├── routes/
│   ├── auth_routes.py         # Authentication endpoints
│   ├── user_routes.py         # User profile endpoints
│   ├── post_routes.py         # Post CRUD endpoints
│   ├── admin_routes.py        # Admin management endpoints
│   ├── upload_routes.py       # File upload endpoints
│   └── analytics_routes.py    # Analytics endpoints
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── auth/
│   │   ├── login.html         # Login page
│   │   └── register.html      # Registration page
│   ├── student/
│   │   ├── dashboard.html     # Student dashboard
│   │   └── profile.html       # Student profile
│   └── admin/
│       └── dashboard.html     # Admin panel
│
├── static/
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── auth.css           # Auth page styles
│   ├── js/
│   │   └── main.js            # Frontend logic
│   └── uploads/               # User uploaded files
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
1. Navigate to `http://localhost:5000/register`
2. Fill in Full Name, Email, and Password
3. Click "Create Account"
4. Login with your credentials

### Login as Admin
1. Navigate to `http://localhost:5000/login`
2. Use admin credentials (created during setup)
3. Access admin dashboard at `/admin`

### Create a Post (Admin Only)
1. Go to Admin Dashboard (`/admin`)
2. Click "Create Post"
3. Fill in title, content, category
4. Choose publish date (immediate or scheduled)
5. Click "Create Post"

### Browse Posts (Student)
1. Login as student
2. Go to Student Dashboard (`/student`)
3. View notifications and manage profile
4. Access other features as needed
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

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Happy News Sharing!** 📰
