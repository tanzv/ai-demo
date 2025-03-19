from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from models.user import User
from utils.auth import (
    create_access_token,
    create_refresh_token,
)

# 创建认证蓝图
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
async def login():
    """用户登录
    
    请求体:
        {
            "username": "用户名或邮箱",
            "password": "密码"
        }
        
    返回:
        {
            "access_token": "访问令牌",
            "refresh_token": "刷新令牌",
            "token_type": "bearer"
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No input data',
                'message': '请提供登录信息'
            }), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'error': 'Invalid input',
                'message': '用户名和密码不能为空'
            }), 400
        
        # 尝试通过用户名查找用户
        user = await User.get_by_username(db.session, username)
        if not user:
            # 如果用户名不存在，尝试通过邮箱查找
            user = await User.get_by_email(db.session, username)
        
        if not user or not user.verify_password(password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': '用户名/邮箱或密码不正确'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'error': 'Account inactive',
                'message': '用户账户未激活'
            }), 400
        
        # 登录用户
        login_user(user)
        
        # 生成令牌
        access_token_expires = timedelta(minutes=30)  # 从配置中获取
        refresh_token_expires = timedelta(days=7)     # 从配置中获取
        
        return jsonify({
            'access_token': create_access_token(user.id, access_token_expires),
            'refresh_token': create_refresh_token(user.id, refresh_token_expires),
            'token_type': 'bearer'
        })
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/register', methods=['POST'])
async def register():
    """注册新用户
    
    请求体:
        {
            "username": "用户名",
            "email": "邮箱",
            "password": "密码",
            "is_superuser": false  # 可选，默认为 false
        }
        
    返回:
        {
            "id": 1,
            "username": "用户名",
            "email": "邮箱",
            "is_active": true,
            "is_superuser": false
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No input data',
                'message': '请提供注册信息'
            }), 400
            
        # 检查必填字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing field',
                    'message': f'缺少必填字段：{field}'
                }), 400
        
        # 检查用户名是否已存在
        if await User.get_by_username(db.session, data['username']):
            return jsonify({
                'error': 'Username taken',
                'message': '用户名已被注册'
            }), 400
        
        # 检查邮箱是否已存在
        if await User.get_by_email(db.session, data['email']):
            return jsonify({
                'error': 'Email taken',
                'message': '邮箱已被注册'
            }), 400
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            is_superuser=data.get('is_superuser', False)
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        await db.session.commit()
        await db.session.refresh(user)
        
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        await db.session.rollback()
        current_app.logger.error(f"Register error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/me', methods=['GET'])
@login_required
async def get_me():
    """获取当前用户信息
    
    返回:
        {
            "id": 1,
            "username": "用户名",
            "email": "邮箱",
            "is_active": true,
            "is_superuser": false
        }
    """
    try:
        return jsonify(current_user.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/refresh', methods=['POST'])
@login_required
async def refresh_token():
    """刷新访问令牌
    
    返回:
        {
            "access_token": "新的访问令牌",
            "refresh_token": "新的刷新令牌",
            "token_type": "bearer"
        }
    """
    try:
        access_token_expires = timedelta(minutes=30)  # 从配置中获取
        refresh_token_expires = timedelta(days=7)     # 从配置中获取
        
        return jsonify({
            'access_token': create_access_token(current_user.id, access_token_expires),
            'refresh_token': create_refresh_token(current_user.id, refresh_token_expires),
            'token_type': 'bearer'
        })
        
    except Exception as e:
        current_app.logger.error(f"Refresh token error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/logout', methods=['POST'])
@login_required
async def logout():
    """用户登出
    
    返回:
        {
            "message": "登出成功"
        }
    """
    try:
        logout_user()
        return jsonify({'message': '登出成功'})
        
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500 