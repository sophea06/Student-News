from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import User, ActivityLog
from extensions import db, bcrypt

auth_bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student or admin account"""
    data = request.get_json()
    
    # Validation
    if not data or not data.get('email') or not data.get('password') or not data.get('name') or not data.get('role'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['role'] not in ['admin', 'student']:
        return jsonify({'error': 'Invalid role. Must be admin or student'}), 400
    
    if db.session.query(User).filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    # Hash password and create user
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=password_hash,
        role=data['role']
    )

    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Registration successful',
        'user_id': user.id,
        'email': user.email,
        'role': user.role
    }), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Login with email and password"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = db.session.query(User).filter_by(email=data['email']).first()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    if not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    if user.is_blocked:
        return jsonify({'error': 'Account has been blocked'}), 403
    
    # Create JWT token
    access_token = create_access_token(identity=user.id)

    # Store token and role in session for template routes
    session['token'] = access_token
    session['role'] = user.role
    session.modified = True

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'profile_picture': user.profile_picture
        }
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user_id = get_jwt_identity()
    if not (user := db.session.query(User).get(user_id)):
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'profile_picture': user.profile_picture,
        'bio': user.bio,
        'followers_count': len(user.followers) if hasattr(user, 'followers') else 0,
        'following_count': len(user.following) if hasattr(user, 'following') else 0,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    if not (user := db.session.query(User).get(user_id)):
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()

    if 'name' in data:
        user.name = data['name']

    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']

    if 'bio' in data:
        user.bio = data['bio']

    db.session.commit()

    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'profile_picture': user.profile_picture,
            'bio': user.bio
        }
    }), 200

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    user_id = get_jwt_identity()
    if not (user := db.session.query(User).get(user_id)):
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()

    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Missing old_password or new_password'}), 400

    if not bcrypt.check_password_hash(user.password_hash, data['old_password']):
        return jsonify({'error': 'Old password is incorrect'}), 401

    user.password_hash = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')

    log = ActivityLog(
        user_id=user_id,
        action='PASSWORD_CHANGE',
        description='User changed password'
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user by clearing session"""
    # Clear session
    session.clear()

    # Create response with CORS headers and delete session cookie
    response = jsonify({'message': 'Logout successful'})
    response.set_cookie('session', '', max_age=0, path='/', httponly=True)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 200
