from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User
import os
from werkzeug.utils import secure_filename
from datetime import datetime

upload_bp = Blueprint('uploads', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """Upload file for posts or profiles"""
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large (max 10MB)'}), 400
    
    # Create upload directory if it doesn't exist
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(f'{user_id}_{timestamp}_{file.filename}')
    
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Return file URL
    file_url = f'/uploads/{filename}'
    
    return jsonify({
        'message': 'File uploaded successfully',
        'file_url': file_url,
        'filename': filename
    }), 201

@upload_bp.route('/profile-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    """Upload profile picture"""
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    def allowed_image_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

    if not allowed_image_file(file.filename):
        return jsonify({'error': 'Only image files allowed'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > 5 * 1024 * 1024:  # 5MB for profile pictures
        return jsonify({'error': 'Image too large (max 5MB)'}), 400
    
    upload_dir = 'uploads/profiles'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(f'profile_{user_id}_{timestamp}_{file.filename}')
    
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Update user profile picture
    user = db.session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.profile_picture = f'/uploads/profiles/{filename}'
    db.session.commit()
    
    return jsonify({
        'message': 'Profile picture updated',
        'profile_picture': user.profile_picture
    }), 201
