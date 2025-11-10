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

    query = db.session.query(Notification).filter_by(user_id=user_id)

    # Apply filters
    status_filter = request.args.get('status', None)  # 'read', 'unread', or None for all
    type_filter = request.args.get('type', None)  # notification type filter

    if status_filter:
        query = query.filter_by(status=status_filter)

    if type_filter:
        query = query.filter_by(notification_type=type_filter)

    # Order by creation date, unread first
    notifications = query.order_by(
        Notification.status == 'unread',  # Unread notifications first
        desc(Notification.created_at)
    ).paginate(page=page, per_page=per_page)

    notifications_data = []
    for notif in notifications.items:
        data = {
            'id': notif.id,
            'message': notif.message,
            'status': notif.status,
            'notification_type': getattr(notif, 'notification_type', 'general'),
            'post_id': notif.post_id,
            'related_user_id': getattr(notif, 'related_user_id', None),
            'created_at': notif.created_at.isoformat() if notif.created_at else None
        }

        # Add related user info if available
        if getattr(notif, 'related_user_id', None):
            related_user = db.session.query(User).get(notif.related_user_id)
            if related_user:
                data['related_user'] = {
                    'id': related_user.id,
                    'name': related_user.name,
                    'profile_picture': related_user.profile_picture
                }

        notifications_data.append(data)

    return jsonify({
        'total': notifications.total,
        'pages': notifications.pages,
        'current_page': page,
        'per_page': per_page,
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

@user_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_student_feed():
    """Get news feed for student with filters and search"""
    user_id = get_jwt_identity()

    # Query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)

    posts_query = db.session.query(Post).filter_by(
        visibility='public',
        status='published',
        is_deleted=False
    )

    if category:
        posts_query = posts_query.filter_by(category=category)

    if search:
        posts_query = posts_query.filter(
            or_(
                func.lower(Post.title).like(func.lower(f'%{search}%')),
                func.lower(Post.content).like(func.lower(f'%{search}%'))
            )
        )

    posts = posts_query.order_by(desc(Post.is_pinned), desc(Post.created_at)).paginate(page=page, per_page=per_page)

    posts_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': f"{post.content[:200]}..." if len(post.content) > 200 else post.content,
            'category': post.category,
            'image_url': post.image_url,
            'author': post.author.name if post.author else 'Deleted User',
            'author_id': post.author_id,
            'likes_count': len(post.likes),
            'comments_count': len(post.comments),
            'view_count': post.view_count,
            'is_liked': any(like.user_id == user_id for like in post.likes),
            'created_at': post.created_at.isoformat() if post.created_at else None
        }
        for post in posts.items
    ]

    return jsonify({
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page,
        'posts': posts_data
    }), 200

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
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200

@user_bp.route('/follow/<int:target_user_id>', methods=['POST'])
@jwt_required()
def follow_user(target_user_id):
    """Follow a user"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

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

        # Create notification for the followed user
        notification = Notification(
            user_id=target_user_id,
            message=f'{user.name} started following you',
            notification_type='follow',
            related_user_id=user_id,
            status='unread'
        )
        db.session.add(notification)
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
                'created_at': log.created_at.isoformat() if log.created_at else None
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

@user_bp.route('/notifications/settings', methods=['GET'])
@jwt_required()
def get_notification_settings():
    """Get user notification settings"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # For now, return default settings. In future, this could be stored in user preferences
    settings = {
        'email_notifications': True,
        'push_notifications': True,
        'like_notifications': True,
        'comment_notifications': True,
        'follow_notifications': True,
        'system_notifications': True
    }

    return jsonify({'settings': settings}), 200

@user_bp.route('/notifications/settings', methods=['PUT'])
@jwt_required()
def update_notification_settings():
    """Update user notification settings"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # For now, just validate the settings. In future, store in database
    valid_settings = ['email_notifications', 'push_notifications', 'like_notifications',
                     'comment_notifications', 'follow_notifications', 'system_notifications']

    settings = {}
    for setting in valid_settings:
        if setting in data:
            settings[setting] = bool(data[setting])

    # Here you would save settings to database
    # For now, just return success

    return jsonify({
        'message': 'Notification settings updated successfully',
        'settings': settings
    }), 200
