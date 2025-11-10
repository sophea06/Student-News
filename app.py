from flask import (
    Flask, render_template, redirect, session, url_for,
    send_from_directory, jsonify, make_response, request
)
from flask_cors import CORS
from flask.cli import with_appcontext
from functools import wraps
import click
import os
import pickle
import shutil
from contextlib import suppress

# Local imports
from config import Config
from extensions import db, bcrypt, jwt, limiter, sess


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # Ensure required directories exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    sess.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": ["Authorization", "Content-Type"], "supports_credentials": True}})

    # ---------------------------
    # Register Blueprints
    # ---------------------------
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.post_routes import post_bp
    from routes.admin_routes import admin_bp
    from routes.upload_routes import upload_bp
    from routes.analytics_routes import analytics_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(post_bp, url_prefix="/api/posts")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(upload_bp, url_prefix="/api/uploads")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

    # ---------------------------
    # Decorator for login required templates
    # ---------------------------
    def login_required_template(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'token' not in session or 'role' not in session:
                return redirect(url_for('login_page'))
            return f(*args, **kwargs)
        return decorated_function

    # ---------------------------
    # HTML Page Routes
    # ---------------------------
    @app.route('/')
    def index():
        """Landing Page"""
        if 'token' in session:
            if session.get('role') == 'admin':
                return redirect(url_for('admin_page'))
            return redirect(url_for('student_page'))
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        """Login Page"""
        if 'token' in session:
            return redirect(url_for('index'))
        return render_template('auth/login.html')

    @app.route('/register')
    def register_page():
        """Register Page"""
        if 'token' in session:
            return redirect(url_for('index'))
        return render_template('auth/register.html')

    @app.route('/student')
    @login_required_template
    def student_page():
        """Student Dashboard"""
        if session.get('role') != 'student':
            return redirect(url_for('index'))
        return render_template('student/dashboard.html')

    @app.route('/admin')
    @login_required_template
    def admin_page():
        """Admin Dashboard"""
        if session.get('role') != 'admin':
            return redirect(url_for('index'))
        return render_template('admin/dashboard.html')

    @app.route('/profile')
    @login_required_template
    def profile_page():
        """User Profile (Admin and Student)"""
        return render_template('student/profile.html')

    @app.route('/contact')
    def contact_page():
        """Contact Page"""
        return render_template('contact.html')

    @app.route('/about')
    def about_page():
        """About Page"""
        return render_template('about.html')

    @app.route('/library')
    def library_page():
        """Library Page"""
        return render_template('library.html')

    @app.route('/study')
    def study_page():
        """Study Materials Page"""
        return render_template('study.html')

    @app.route('/international-study')
    def international_study_page():
        """International Study Page"""
        return render_template('international-study.html')

    @app.route('/dashboard')
    def dashboard_page():
        """Redirect dashboard based on role"""
        if 'token' not in session or 'role' not in session:
            return redirect(url_for('login_page'))

        return redirect(
            url_for('admin_page' if session.get('role') == 'admin' else 'student_page')
        )

    @app.route('/notifications')
    @login_required_template
    def notifications_page():
        """Notifications Page"""
        return render_template('notifications.html')

    # ---------------------------
    # Logout Routes
    # ---------------------------
    @app.route('/logout')
    def logout_page():
        """Logout and show confirmation page"""
        next_url = request.args.get('next') or url_for('index')

        # Clear all session data
        session.clear()
        response = make_response(render_template('auth/logout.html', next_url=next_url))

        # Remove session cookies
        for cookie in ['session', 'session.sig', 'token', 'remember_token', 'user_id', 'username', 'role']:
            response.set_cookie(cookie, '', expires=0, path='/')

        # Prevent caching of logout page
        response.headers.update({
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        })

        return response

    @app.route('/api/auth/logout', methods=['POST'])
    def api_logout():
        """API Logout Endpoint"""
        session.clear()
        response = jsonify({
            'success': True,
            'message': 'Successfully logged out',
            'redirect': url_for('login_page')
        })
        for cookie in ['session', 'session.sig', 'token', 'remember_token']:
            response.set_cookie(cookie, '', expires=0, path='/')
        return response

    # ---------------------------
    # File Serving Route
    # ---------------------------
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ---------------------------
    # CLI Commands
    # ---------------------------
    @app.cli.command("logout-user")
    @click.argument("user_id", type=int)
    @with_appcontext
    def logout_user_command(user_id):
        """Force logout a specific user"""
        from models import User
        from flask_jwt_extended import decode_token

        user = db.session.get(User, user_id)
        if not user:
            click.echo(f"❌ User with ID {user_id} not found.")
            return

        session_dir = os.path.join(app.root_path, 'flask_session')
        if not os.path.exists(session_dir):
            click.echo("⚠️  No session directory found.")
            return

        cleared = 0
        for filename in os.listdir(session_dir):
            if filename.startswith('sess_'):
                filepath = os.path.join(session_dir, filename)
                with suppress(Exception):
                    with open(filepath, 'rb') as f:
                        data = pickle.load(f)
                    if 'token' in data:
                        with suppress(Exception):
                            decoded = decode_token(data['token'])
                            if decoded.get('sub') == user_id:
                                os.remove(filepath)
                                cleared += 1
                                click.echo(f"🗑️  Cleared session {filename}")

        click.echo(f"✅ Logged out user '{user.name}' (ID: {user.id})")
        click.echo(f"🧹 Sessions cleared: {cleared}")

    @app.cli.command("logout-all")
    @with_appcontext
    def logout_all_command():
        """Force logout all users"""
        session_dir = os.path.join(app.root_path, 'flask_session')
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)
            os.makedirs(session_dir)
            click.echo("✅ All sessions cleared.")
        else:
            click.echo("⚠️  Session directory not found.")
        click.echo("Note: JWT tokens remain valid until expiration.")

    # ---------------------------
    # Initialize database
    # ---------------------------
    with app.app_context():
        db.create_all()

    return app


# ---------------------------
# Entry Point
# ---------------------------
def main():
    """Main entry point"""
    os.makedirs('uploads/posts', exist_ok=True)
    os.makedirs('flask_session', exist_ok=True)

    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
