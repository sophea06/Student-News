from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Post, Notification, Follow, ActivityLog
from sqlalchemy import or_, desc, func

user_bp = Blueprint('users', __name__)

@user_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user notifications"""
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    notifications = db.session.query(Notification).filter_by(user_id=user_id).order_by(
        desc(Notification.created_at)
    ).paginate(page=page, per_page=per_page)
    
    notifications_data = [{
        'id': notif.id,
        'message': notif.message,
        'status': notif.status,
        'post_id': notif.post_id,
        'created_at': notif.created_at.isoformat()
    } for notif in notifications.items]
    
    return jsonify({
        'total': notifications.total,
        'pages': notifications.pages,
        'current_page': page,
        'notifications': notifications_data
    }), 200

@user_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    user_id = get_jwt_identity()
    notification = db.session.query(Notification).get(notification_id)
    
    if not notification or notification.user_id != user_id:
        return jsonify({'error': 'Notification not found'}), 404
    
    notification.status = 'read'
    db.session.commit()
    
    return jsonify({'message': 'Notification marked as read'}), 200

@user_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications"""
    user_id = get_jwt_identity()
    
    unread_count = db.session.query(Notification).filter_by(
        user_id=user_id,
        status='unread'
    ).count()
    
    return jsonify({'unread_count': unread_count}), 200


@user_bp.route('/saved-posts', methods=['GET'])
@jwt_required()
def get_saved_posts():
    """Get user's saved (bookmarked) posts - implementation for future bookmark feature"""
    # user_id = get_jwt_identity()  # Removed unused variable

    return jsonify({
        'message': 'Bookmark feature coming soon',
        'saved_posts': []
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Get student profile"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'profile_picture': user.profile_picture,
        'bio': user.bio if hasattr(user, 'bio') else None,
        'posts_count': len(user.posts),
        'likes_count': len(user.likes),
        'comments_count': len(user.comments),
        'followers_count': len(user.followers) if hasattr(user, 'followers') else 0,
        'following_count': len(user.following) if hasattr(user, 'following') else 0,
        'created_at': user.created_at.isoformat()
    }), 200

@user_bp.route('/follow/<int:target_user_id>', methods=['POST'])
@jwt_required()
def follow_user(target_user_id):
    """Follow a user"""
    user_id = get_jwt_identity()
    
    if user_id == target_user_id:
        return jsonify({'error': 'Cannot follow yourself'}), 400
    
    target_user = db.session.query(User).get(target_user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    if hasattr(User, 'followers'):
        if existing := db.session.query(Follow).filter_by(follower_id=user_id, following_id=target_user_id).first():
            return jsonify({'error': 'Already following'}), 409
        
        follow = Follow(follower_id=user_id, following_id=target_user_id)
        db.session.add(follow)
        db.session.commit()
        
        return jsonify({'message': 'Successfully followed user'}), 201
    
    return jsonify({'message': 'Follow feature not yet available'}), 200

@user_bp.route('/activity-logs', methods=['GET'])
@jwt_required()
def get_activity_logs():
    """Get current user's activity logs"""
    user_id = get_jwt_identity()
    
    if hasattr(User, 'activity_logs'):
        logs = db.session.query(ActivityLog).filter_by(user_id=user_id).order_by(
            desc(ActivityLog.created_at)
        ).limit(50).all()
        
        logs_data = [
            {
                'id': log.id,
                'action': log.action,
                'description': log.description,
                'created_at': log.created_at.isoformat()
            }
            for log in logs
        ]
        
        return jsonify({'activity_logs': logs_data}), 200
    
    return jsonify({'activity_logs': []}), 200

@user_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update name if provided
    if 'name' in data:
        if not data['name'].strip():
            return jsonify({'error': 'Name cannot be empty'}), 400
        user.name = data['name'].strip()

    # Update bio if provided
    if 'bio' in data:
        user.bio = data['bio'].strip() if data['bio'] else None

    # Update password if provided
    if 'password' in data and data['password']:
        from extensions import bcrypt
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500

@user_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available post categories"""
    categories = [
        'general',
        'campus',
        'events',
        'announcements',
        'academic',
        'sports',
        'culture'
    ]

    return jsonify({'categories': categories}), 200
