from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from config.database import db
from utils.auth import create_access_token, create_refresh_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'error': 'Missing username or password'
        }), 400
        
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.verify_password(data['password']):
        login_user(user)
        return jsonify({
            'access_token': create_access_token(user.id),
            'refresh_token': create_refresh_token(user.id),
            'token_type': 'bearer'
        })
        
    return jsonify({
        'error': 'Invalid username or password'
    }), 401

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return jsonify({
        'message': 'Logout successful'
    })

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
            
    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already registered"}), 400
        
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400
        
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        is_superuser=data.get('is_superuser', False)
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_me():
    """Get current user information"""
    return jsonify(current_user.to_dict())

@auth_bp.route('/refresh', methods=['POST'])
@login_required
def refresh():
    """Refresh access token"""
    return jsonify({
        "access_token": create_access_token(current_user.id),
        "refresh_token": create_refresh_token(current_user.id),
        "token_type": "bearer"
    }) 