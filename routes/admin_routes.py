from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Post, Comment, Notification
from functools import wraps
from datetime import datetime, timezone
from sqlalchemy import desc

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.query(User).get(user_id)

        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get admin dashboard overview statistics"""
    total_students = db.session.query(User).filter_by(role='student').count()
    total_posts = db.session.query(Post).count()
    total_comments = db.session.query(Comment).count()
    recent_posts = db.session.query(Post).order_by(desc(Post.created_at)).limit(5).all()
    
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'author': post.author.name,
        'likes': len(post.likes),
        'comments': len(post.comments),
        'created_at': post.created_at.isoformat() if post.created_at else None
    } for post in recent_posts]
    
    return jsonify({
        'total_students': total_students,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'recent_posts': posts_data
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get list of all students"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    users = db.session.query(User).filter_by(role='student').paginate(page=page, per_page=per_page)
    
    users_data = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'is_blocked': user.is_blocked,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'posts_count': len(user.posts)
    } for user in users.items]
    
    return jsonify({
        'total': users.total,
        'pages': users.pages,
        'current_page': page,
        'users': users_data
    }), 200

@admin_bp.route('/users/<int:user_id>/block', methods=['PUT'])
@admin_required
def block_user(user_id):
    """Block a student account"""
    user = db.session.query(User).get(user_id)

    if not user or user.role == 'admin':
        return jsonify({'error': 'User not found or cannot block admin'}), 404
    
    data = request.get_json() or {}
    reason = data.get('reason', 'No reason provided')
    
    user.is_blocked = True
    if hasattr(user, 'block_reason'):
        user.block_reason = reason
    if hasattr(user, 'blocked_at'):
        user.blocked_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({'message': f'User {user.email} has been blocked'}), 200

@admin_bp.route('/users/<int:user_id>/unblock', methods=['PUT'])
@admin_required
def unblock_user(user_id):
    """Unblock a student account"""
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.is_blocked = False
    if hasattr(user, 'block_reason'):
        user.block_reason = None
    if hasattr(user, 'blocked_at'):
        user.blocked_at = None
    
    db.session.commit()
    
    return jsonify({'message': f'User {user.email} has been unblocked'}), 200

@admin_bp.route('/users/<int:user_id>/reset-password', methods=['PUT'])
@admin_required
def reset_user_password(user_id):
    """Reset user password to default"""
    from app import bcrypt
    
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    default_password = 'temp123456'
    user.password_hash = bcrypt.generate_password_hash(default_password).decode('utf-8')
    db.session.commit()
    
    return jsonify({
        'message': f'Password reset for {user.email}',
        'temporary_password': default_password
    }), 200

@admin_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@admin_required
def delete_comment(comment_id):
    """Delete a comment (for spam/inappropriate content)"""
    comment = db.session.query(Comment).get(comment_id)

    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200

@admin_bp.route('/send-announcement', methods=['POST'])
@admin_required
def send_announcement():
    """Send announcement to all students"""
    data = request.get_json()
    
    if not data.get('message'):
        return jsonify({'error': 'Message is required'}), 400
    
    students = db.session.query(User).filter_by(role='student').all()
    
    for student in students:
        notification = Notification(
            user_id=student.id,
            message=data['message'],
            status='unread'
        )
        db.session.add(notification)
    
    db.session.commit()
    
    return jsonify({
        'message': f'Announcement sent to {len(students)} students'
    }), 200
