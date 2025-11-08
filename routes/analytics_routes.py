from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, Post, Like, Comment
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, desc

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/trending-posts', methods=['GET'])
@jwt_required()
def get_trending_posts():
    """Get trending posts (most likes/comments in last 7 days)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)
    
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    
    trending_posts = db.session.query(
        Post,
        (func.count(Like.id) + func.count(Comment.id)).label('engagement_count')
    ).outerjoin(Like).outerjoin(Comment).filter(
        Post.created_at >= week_ago,
        Post.is_deleted == False
    ).group_by(Post.id).order_by('engagement_count'.desc()).limit(10).all()
    
    posts_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': f"{post.content[:150]}..." if len(post.content) > 150 else post.content,
            'author': post.author.name,
            'likes_count': len(post.likes),
            'comments_count': len(post.comments),
            'view_count': post.view_count,
            'engagement_score': engagement,
            'created_at': post.created_at.isoformat()
        }
        for post, engagement in trending_posts
        if user.role != 'student' or (post.visibility == 'public' and post.status == 'published')
    ]
    
    return jsonify({'trending_posts': posts_data}), 200

@analytics_bp.route('/popular-posts', methods=['GET'])
@jwt_required()
def get_popular_posts():
    """Get most viewed/liked posts of all time"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    posts_query = db.session.query(Post).filter_by(is_deleted=False)

    if user.role == 'student':
        posts_query = posts_query.filter_by(visibility='public', status='published')

    popular_posts = posts_query.order_by(desc(Post.view_count)).limit(10).all()

    posts_data = [
        {
            'id': post.id,
            'title': post.title,
            'content': f"{post.content[:150]}..." if len(post.content) > 150 else post.content,
            'author': post.author.name,
            'likes_count': len(post.likes),
            'comments_count': len(post.comments),
            'view_count': post.view_count,
            'share_count': post.share_count,
            'created_at': post.created_at.isoformat()
        }
        for post in popular_posts
    ]
    
    return jsonify({'popular_posts': posts_data}), 200

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_analytics():
    """Get dashboard analytics (admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Only admins can view analytics'}), 403

    total_users = db.session.query(User).count()
    total_posts = db.session.query(Post).filter_by(is_deleted=False).count()
    total_likes = db.session.query(Like).count()
    total_comments = db.session.query(Comment).count()
    total_views = db.session.query(func.sum(Post.view_count)).filter(Post.is_deleted == False).scalar() or 0

    # Posts this month
    month_ago = datetime.now(timezone.utc) - timedelta(days=30)
    posts_this_month = db.session.query(Post).filter(
        Post.created_at >= month_ago,
        Post.is_deleted == False
    ).count()

    # Active students (have liked or commented this month)
    active_students = db.session.query(User).join(Like).filter(
        Like.created_at >= month_ago,
        User.role == 'student'
    ).distinct().count()
    
    # Most active user
    most_active_user = db.session.query(
        User,
        func.count(Like.id).label('likes_count')
    ).join(Like).group_by(User.id).order_by(desc(func.count(Like.id))).first()

    most_active_data = {
        'name': most_active_user[0].name,
        'engagements': most_active_user[1]
    } if most_active_user else None
    
    return jsonify({
        'total_users': total_users,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_views': total_views,
        'posts_this_month': posts_this_month,
        'active_students_this_month': active_students,
        'most_active_user': most_active_data
    }), 200

@analytics_bp.route('/post-analytics/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post_analytics(post_id):
    """Get detailed analytics for a specific post"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Cannot view analytics for this post'}), 403
    
    likes_by_day = db.session.query(
        func.date(Like.created_at).label('day'),
        func.count(Like.id).label('count')
    ).filter_by(post_id=post_id).group_by('day').order_by('day').all()
    
    comments_by_day = db.session.query(
        func.date(Comment.created_at).label('day'),
        func.count(Comment.id).label('count')
    ).filter_by(post_id=post_id).group_by('day').order_by('day').all()
    
    return jsonify({
        'post_id': post.id,
        'title': post.title,
        'likes_count': len(post.likes),
        'comments_count': len(post.comments),
        'view_count': post.view_count,
        'share_count': post.share_count,
        'likes_by_day': [{'day': str(day), 'count': count} for day, count in likes_by_day],
        'comments_by_day': [{'day': str(day), 'count': count} for day, count in comments_by_day],
        'created_at': post.created_at.isoformat()
    }), 200

@analytics_bp.route('/user-engagement/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_engagement(user_id):
    """Get user engagement metrics"""
    current_user_id = get_jwt_identity()
    current_user = db.session.query(User).get(current_user_id)

    if not current_user:
        return jsonify({'error': 'Current user not found'}), 404

    target_user = db.session.query(User).get(user_id)

    if not target_user:
        return jsonify({'error': 'User not found'}), 404

    # Only admins or the user themselves can view engagement metrics
    if current_user.role not in ['admin', 'super_admin'] and current_user_id != user_id:
        return jsonify({'error': 'Cannot view this user\'s engagement'}), 403

    user_likes = db.session.query(Like).filter_by(user_id=user_id).count()
    user_comments = db.session.query(Comment).filter_by(user_id=user_id).count()
    user_posts = db.session.query(Post).filter_by(author_id=user_id, is_deleted=False).count()
    
    # Engagement score: likes + comments*2 + posts*5
    engagement_score = user_likes + (user_comments * 2) + (user_posts * 5)
    
    return jsonify({
        'user_id': user_id,
        'user_name': target_user.name,
        'likes_given': user_likes,
        'comments_made': user_comments,
        'posts_created': user_posts,
        'engagement_score': engagement_score,
        'followers': len(target_user.followers),
        'following': len(target_user.following)
    }), 200
