from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # admin, editor, moderator, student
    profile_picture = db.Column(db.String(255), default=None)
    bio = db.Column(db.Text, default=None)
    is_blocked = db.Column(db.Boolean, default=False)
    block_reason = db.Column(db.String(255), default=None)
    blocked_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy=True, foreign_keys='Post.author_id')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower_user', lazy=True, cascade='all, delete-orphan')
    following = db.relationship('Follow', foreign_keys='Follow.following_id', backref='following_user', lazy=True, cascade='all, delete-orphan')
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Follow(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)
    
    def __repr__(self):
        return f'<Follow {self.follower_id} -> {self.following_id}>'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general', nullable=False)
    image_url = db.Column(db.String(255), default=None)
    visibility = db.Column(db.String(20), default='public', nullable=False)  # public, private, important
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    view_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='published', nullable=False)  # published, draft, scheduled
    is_pinned = db.Column(db.Boolean, default=False)
    scheduled_at = db.Column(db.DateTime, default=None)
    is_deleted = db.Column(db.Boolean, default=False)  # soft delete
    deleted_at = db.Column(db.DateTime, default=None)
    share_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)
    
    def __repr__(self):
        return f'<Like user={self.user_id} post={self.post_id}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), default=None)
    status = db.Column(db.String(20), default='approved', nullable=False)  # pending, approved, rejected
    is_flagged = db.Column(db.Boolean, default=False)
    flag_reason = db.Column(db.String(255), default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, default=None)
    
    # Relationships
    replies = db.relationship('Comment', remote_side=[id], backref='parent', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self):
        return f'<Comment by user={self.user_id} on post={self.post_id}>'

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), default=None)
    status = db.Column(db.String(20), default='unread', nullable=False)  # read or unread
    notification_type = db.Column(db.String(50), default='general', nullable=False)  # like, comment, follow, mention, system
    related_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)  # user who triggered the notification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification user={self.user_id} type={self.notification_type} status={self.status}>'

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ActivityLog {self.action}>'
