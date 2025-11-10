from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, limiter
from models import User, Post, Like, Comment, Notification
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_, func, desc
import os
from werkzeug.utils import secure_filename

post_bp = Blueprint('posts', __name__)

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@post_bp.route('/public', methods=['GET'])
def get_public_posts():
    """Get public posts for home page (no auth required)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)  # Show fewer on home page
    category = request.args.get('category', None)

    # Base query - only public, published posts, not deleted
    query = db.session.query(Post).filter_by(
        visibility='public',
        status='published',
        is_deleted=False
    )

    # Filter by category if specified
    if category and category != 'all':
        query = query.filter_by(category=category)

    # Sort by pinned first, then newest
    query = query.order_by(desc(Post.is_pinned), desc(Post.created_at))

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page)

    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': f"{post.content[:150]}..." if len(post.content) > 150 else post.content,
        'category': post.category,
        'image_url': post.image_url,
        'author': post.author.name if post.author else 'Deleted User',
        'likes_count': len(post.likes),
        'comments_count': len(post.comments),
        'view_count': post.view_count,
        'share_count': post.share_count,
        'is_pinned': post.is_pinned,
        'created_at': post.created_at.isoformat() if post.created_at else None
    } for post in pagination.items]

    return jsonify({
        'posts': posts_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

def build_comment_tree(comment):
    return {
        'id': comment.id,
        'author': comment.user.name if comment.user else 'Deleted User',
        'author_id': comment.user_id,
        'content': comment.content,
        'status': comment.status,
        'is_flagged': comment.is_flagged,
        'created_at': comment.created_at.isoformat() if comment.created_at else None,
        'replies': [build_comment_tree(reply) for reply in (comment.replies or [])]
    }

@post_bp.route('', methods=['GET'])
@jwt_required()
def get_posts():
    """Get paginated posts with filtering"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    sort_by = request.args.get('sort_by', 'newest')  # newest, popular, trending
    
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Base query - exclude soft deleted posts
    query = db.session.query(Post).filter_by(is_deleted=False)

    # Students see only public posts, admins see all
    if user.role == 'student':
        query = query.filter_by(visibility='public', status='published')

    # Filter by category
    if (category := request.args.get('category', None)) and category != 'all':
        query = query.filter_by(category=category)

    # Search by title or content
    if (search := request.args.get('search', None)):
        query = query.filter(
            or_(
                func.lower(Post.title).like(func.lower(f'%{search}%')),
                func.lower(Post.content).like(func.lower(f'%{search}%'))
            )
        )
    
    # Sort
    if sort_by == 'popular':
        query = query.order_by(desc(Post.view_count))
    elif sort_by == 'trending':
        # Trending: posts with most likes in last 7 days
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        query = query.filter(Post.created_at >= week_ago).outerjoin(Like).group_by(Post.id).order_by(desc(func.count(Like.id)))
    else:  # newest
        query = query.order_by(desc(Post.is_pinned), desc(Post.created_at))
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page)
    
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': f"{post.content[:150]}..." if len(post.content) > 150 else post.content,
        'category': post.category,
        'image_url': post.image_url,
        'author': post.author.name if post.author else 'Deleted User',
        'author_id': post.author_id,
        'likes_count': len(post.likes),
        'comments_count': len(post.comments),
        'view_count': post.view_count,
        'share_count': post.share_count,
        'is_liked': any(like.user_id == user_id for like in post.likes),
        'is_pinned': post.is_pinned,
        'status': post.status,
        'created_at': post.created_at.isoformat() if post.created_at else None
    } for post in pagination.items]
    
    return jsonify({
        'posts': posts_data,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    }), 200

@post_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post (admin/editor only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'editor', 'super_admin']:
        return jsonify({'error': 'Only admins and editors can create posts'}), 403

    data = request.form  # Use form data to handle file uploads

    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    status = data.get('status', 'published')  # published, draft, scheduled
    scheduled_at = None

    if status == 'scheduled':
        try:
            scheduled_at = datetime.fromisoformat(data.get('scheduled_at'))
        except:
            return jsonify({'error': 'Invalid scheduled_at format'}), 400

    # Handle image upload
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            if not allowed_image_file(file.filename):
                return jsonify({'error': 'Only image files (jpg, jpeg, png, gif) are allowed'}), 400

            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_IMAGE_SIZE:
                return jsonify({'error': 'Image too large (max 10MB)'}), 400

            # Create upload directory if it doesn't exist
            upload_dir = 'uploads/posts'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Generate unique filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(f'post_{user_id}_{timestamp}_{file.filename}')

            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)

            # Return file URL
            image_url = f'/uploads/posts/{filename}'

    # Also allow image_url from form data (for external links)
    if not image_url and data.get('image_url'):
        image_url = data.get('image_url')

    post = Post(
        title=data['title'],
        content=data['content'],
        category=data.get('category', 'general'),
        image_url=image_url,
        visibility=data.get('visibility', 'public'),
        author_id=user_id,
        status=status,
        scheduled_at=scheduled_at,
        is_pinned=data.get('is_pinned', False)
    )

    db.session.add(post)
    db.session.commit()

    # Create notifications for published posts
    if status == 'published':
        students = db.session.query(User).filter_by(role='student', is_blocked=False).all()
        for student in students:
            notification = Notification(
                user_id=student.id,
                message=f'New post: {post.title}',
                post_id=post.id,
                notification_type='system',
                status='unread'
            )
            db.session.add(notification)

    db.session.commit()

    return jsonify({
        'message': 'Post created successfully',
        'post_id': post.id,
        'status': status,
        'image_url': image_url
    }), 201

@post_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    """Get post details"""
    user_id = get_jwt_identity()
    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    # Check visibility (admin can see all, students see public only)
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role == 'student' and post.visibility != 'public':
        return jsonify({'error': 'Access denied'}), 403

    # Increment view count
    post.view_count += 1
    db.session.commit()

    # Show all approved comments to all users
    comments = db.session.query(Comment).filter_by(post_id=post_id, status='approved').all()

    comments_data = [{
        'id': comment.id,
        'author': comment.user.name if comment.user else 'Deleted User',
        'author_id': comment.user_id,
        'content': comment.content,
        'status': comment.status,
        'is_flagged': comment.is_flagged,
        'created_at': comment.created_at.isoformat() if comment.created_at else None,
        'replies': [build_comment_tree(reply) for reply in (comment.replies or [])]
    } for comment in comments]
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'image_url': post.image_url,
        'visibility': post.visibility,
        'author': post.author.name if post.author else 'Deleted User',
        'author_id': post.author_id,
        'likes_count': len(post.likes),
        'comments_count': len(post.comments),
        'view_count': post.view_count,
        'share_count': post.share_count,
        'is_liked': any(like.user_id == user_id for like in post.likes),
        'comments': comments_data,
        'created_at': post.created_at.isoformat() if post.created_at else None,
        'updated_at': post.updated_at.isoformat() if post.updated_at else None,
        'is_pinned': post.is_pinned,
        'status': post.status
    }), 200

@post_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update post (admin/editor only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'editor', 'super_admin']:
        return jsonify({'error': 'Only admins and editors can update posts'}), 403

    post = db.session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Can only update your own posts'}), 403

    data = request.form  # Use form data to handle file uploads

    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'category' in data:
        post.category = data['category']
    if 'visibility' in data:
        post.visibility = data['visibility']
    if 'status' in data:
        post.status = data['status']
    if 'scheduled_at' in data:
        try:
            post.scheduled_at = datetime.fromisoformat(data['scheduled_at'])
        except:
            return jsonify({'error': 'Invalid scheduled_at format'}), 400
    if 'is_pinned' in data:
        post.is_pinned = data['is_pinned']

    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            if not allowed_image_file(file.filename):
                return jsonify({'error': 'Only image files (jpg, jpeg, png, gif) are allowed'}), 400

            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size > MAX_IMAGE_SIZE:
                return jsonify({'error': 'Image too large (max 10MB)'}), 400

            # Create upload directory if it doesn't exist
            upload_dir = 'uploads/posts'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Generate unique filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(f'post_{user_id}_{timestamp}_{file.filename}')

            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)

            # Update post image_url
            post.image_url = f'/uploads/posts/{filename}'

    # Also allow image_url from form data (for external links)
    if 'image_url' in data and not post.image_url:
        post.image_url = data.get('image_url')

    db.session.commit()

    return jsonify({
        'message': 'Post updated successfully',
        'post_id': post.id,
        'image_url': post.image_url
    }), 200

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete post (admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Only admins can delete posts'}), 403
    
    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Can only delete your own posts'}), 403
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Post deleted successfully'}), 200

@post_bp.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
@limiter.limit("30 per minute")  # Rate limit likes to prevent spam
def like_post(post_id):
    """Like a post"""
    user_id = get_jwt_identity()
    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if post.is_deleted:
        return jsonify({'error': 'Post not found'}), 404
    if user.role == 'student' and post.visibility != 'public':
        return jsonify({'error': 'Access denied'}), 403

    if (existing_like := db.session.query(Like).filter_by(user_id=user_id, post_id=post_id).first()):
        return jsonify({'error': 'Already liked'}), 409
    
    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    # Create notification for post author (if not liking own post)
    if post.author_id != user_id:
        notification = Notification(
            user_id=post.author_id,
            message=f'{user.name} liked your post "{post.title}"',
            post_id=post.id,
            notification_type='like',
            related_user_id=user_id,
            status='unread'
        )
        db.session.add(notification)
        db.session.commit()

    return jsonify({
        'message': 'Post liked successfully',
        'likes_count': len(post.likes)
    }), 201

@post_bp.route('/<int:post_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_post(post_id):
    """Unlike a post"""
    user_id = get_jwt_identity()
    
    like = db.session.query(Like).filter_by(user_id=user_id, post_id=post_id).first()
    
    if not like:
        return jsonify({'error': 'Like not found'}), 404
    
    db.session.delete(like)
    db.session.commit()
    
    post = db.session.query(Post).get(post_id)
    
    return jsonify({
        'message': 'Post unliked successfully',
        'likes_count': len(post.likes)
    }), 200

@post_bp.route('/<int:post_id>/comments', methods=['POST'])
@jwt_required()
@limiter.limit("20 per minute")  # Rate limit comments to prevent spam
def add_comment(post_id):
    """Add comment to post with moderation"""
    user_id = get_jwt_identity()
    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'error': 'Comment content is required'}), 400
    
    parent_comment_id = data.get('parent_comment_id')  # For threaded replies
    
    # Auto-approve all comments
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    status = 'approved'  # All comments are auto-approved
    
    comment = Comment(
        content=data['content'],
        user_id=user_id,
        post_id=post_id,
        parent_comment_id=parent_comment_id,
        status=status,
        approved_at=datetime.now(timezone.utc) if status == 'approved' else None
    )
    
    db.session.add(comment)
    db.session.commit()

    # Create notification for post author (if not commenting on own post)
    if post.author_id != user_id:
        notification = Notification(
            user_id=post.author_id,
            message=f'{user.name} commented on your post "{post.title}"',
            post_id=post.id,
            notification_type='comment',
            related_user_id=user_id,
            status='unread'
        )
        db.session.add(notification)
        db.session.commit()

    return jsonify({
        'message': 'Comment added successfully',
        'comment': {
            'id': comment.id,
            'author': user.name if user else 'Deleted User',
            'content': comment.content,
            'status': status,
            'created_at': comment.created_at.isoformat() if comment.created_at else None
        },
        'comments_count': len(post.comments)
    }), 201

@post_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Delete own comment or moderate (admin)"""
    user_id = get_jwt_identity()
    comment = db.session.query(Comment).get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != user_id:
        user = db.session.query(User).get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role not in ['admin', 'moderator', 'super_admin']:
            return jsonify({'error': 'Can only delete your own comments'}), 403
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    
    post = db.session.query(Post).get(post_id)
    
    return jsonify({
        'message': 'Comment deleted successfully',
        'comments_count': len(post.comments)
    }), 200

@post_bp.route('/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    """Get all comments for a post with thread structure"""
    user_id = get_jwt_identity()
    post = db.session.query(Post).get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Show all approved comments to all users
    comments = db.session.query(Comment).filter_by(post_id=post_id, status='approved').all()
    
    
    # Get only root comments (no parent)
    root_comments = [build_comment_tree(c) for c in comments if c.parent_comment_id is None]
    
    return jsonify({
        'comments': root_comments,
        'total_count': len(comments)
    }), 200

@post_bp.route('/comments/<int:comment_id>/approve', methods=['POST'])
@jwt_required()
def approve_comment(comment_id):
    """Approve comment (moderator/admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'moderator', 'super_admin']:
        return jsonify({'error': 'Only moderators can approve comments'}), 403
    
    comment = db.session.query(Comment).get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    comment.status = 'approved'
    comment.approved_at = datetime.now(timezone.utc)
    db.session.commit()
    
    return jsonify({'message': 'Comment approved'}), 200

@post_bp.route('/comments/<int:comment_id>/reject', methods=['POST'])
@jwt_required()
def reject_comment(comment_id):
    """Reject comment (moderator/admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'moderator', 'super_admin']:
        return jsonify({'error': 'Only moderators can reject comments'}), 403
    
    comment = db.session.query(Comment).get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    comment.status = 'rejected'
    db.session.commit()
    
    return jsonify({'message': 'Comment rejected'}), 200

@post_bp.route('/comments/<int:comment_id>/flag', methods=['POST'])
@jwt_required()
def flag_comment(comment_id):
    """Flag comment for review"""
    comment = db.session.query(Comment).get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    data = request.get_json()
    reason = data.get('reason', 'No reason provided')
    
    comment.is_flagged = True
    comment.flag_reason = reason
    db.session.commit()
    
    return jsonify({'message': 'Comment flagged for review'}), 200

@post_bp.route('/<int:post_id>/share', methods=['POST'])
@jwt_required()
def share_post(post_id):
    """Track post shares"""
    post = db.session.query(Post).get(post_id)

    if not post or post.is_deleted:
        return jsonify({'error': 'Post not found'}), 404
    
    post.share_count += 1
    db.session.commit()
    
    return jsonify({
        'message': 'Post shared successfully',
        'share_count': post.share_count
    }), 200

@post_bp.route('/<int:post_id>/soft-delete', methods=['DELETE'])
@jwt_required()
def soft_delete_post(post_id):
    """Soft delete post (admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Only admins can soft delete posts'}), 403

    post = db.session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Can only soft delete your own posts'}), 403

    post.is_deleted = True
    post.deleted_at = datetime.now(timezone.utc)
    db.session.commit()

    return jsonify({'message': 'Post archived successfully'}), 200

@post_bp.route('/<int:post_id>/restore', methods=['POST'])
@jwt_required()
def restore_post(post_id):
    """Restore soft deleted post (admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Only admins can restore posts'}), 403

    post = db.session.query(Post).get(post_id)

    if not post or not post.is_deleted:
        return jsonify({'error': 'Post not found'}), 404

    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Can only restore your own posts'}), 403

    post.is_deleted = False
    post.deleted_at = None
    db.session.commit()

    return jsonify({'message': 'Post restored successfully'}), 200

@post_bp.route('/<int:post_id>/pin', methods=['POST'])
@jwt_required()
def pin_post(post_id):
    """Pin important post to top (admin only)"""
    user_id = get_jwt_identity()
    user = db.session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.role not in ['admin', 'super_admin']:
        return jsonify({'error': 'Only admins can pin posts'}), 403

    post = db.session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if user.role not in ['admin', 'super_admin'] and post.author_id != user_id:
        return jsonify({'error': 'Can only pin your own posts'}), 403

    post.is_pinned = not post.is_pinned
    db.session.commit()

    return jsonify({
        'message': f'Post {"pinned" if post.is_pinned else "unpinned"}',
        'is_pinned': post.is_pinned
    }), 200

