from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import select

from app import db
from models.user import User
from utils.auth import admin_required

# 创建用户蓝图
bp = Blueprint('users', __name__)

@bp.route('/', methods=['GET'])
@login_required
@admin_required
async def list_users():
    """获取用户列表（仅管理员）
    
    查询参数:
        page: 页码（默认：1）
        per_page: 每页数量（默认：10）
        
    返回:
        {
            "total": 总数量,
            "pages": 总页数,
            "current_page": 当前页码,
            "per_page": 每页数量,
            "items": [
                {
                    "id": 1,
                    "username": "用户名",
                    "email": "邮箱",
                    "is_active": true,
                    "is_superuser": false
                },
                ...
            ]
        }
    """
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 查询用户总数
        total = await db.session.scalar(
            select(db.func.count()).select_from(User)
        )
        
        # 查询用户列表
        result = await db.session.execute(
            select(User)
            .order_by(User.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        users = result.scalars().all()
        
        # 计算总页数
        pages = (total + per_page - 1) // per_page
        
        return jsonify({
            'total': total,
            'pages': pages,
            'current_page': page,
            'per_page': per_page,
            'items': [user.to_dict() for user in users]
        })
        
    except Exception as e:
        current_app.logger.error(f"List users error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/<int:user_id>', methods=['GET'])
@login_required
async def get_user(user_id):
    """获取用户详情
    
    Args:
        user_id: 用户 ID
        
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
        # 检查权限
        if not current_user.is_superuser and current_user.id != user_id:
            return jsonify({
                'error': 'Permission denied',
                'message': '没有权限访问其他用户信息'
            }), 403
        
        # 查询用户
        user = await User.get_by_id(db.session, user_id)
        if not user:
            return jsonify({
                'error': 'Not found',
                'message': '用户不存在'
            }), 404
            
        return jsonify(user.to_dict())
        
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/<int:user_id>', methods=['PUT'])
@login_required
async def update_user(user_id):
    """更新用户信息
    
    Args:
        user_id: 用户 ID
        
    请求体:
        {
            "username": "新用户名",
            "email": "新邮箱",
            "password": "新密码",  # 可选
            "is_active": true,    # 仅管理员可设置
            "is_superuser": false # 仅管理员可设置
        }
        
    返回:
        {
            "message": "更新成功",
            "user": {
                "id": 1,
                "username": "用户名",
                "email": "邮箱",
                "is_active": true,
                "is_superuser": false
            }
        }
    """
    try:
        # 检查权限
        if not current_user.is_superuser and current_user.id != user_id:
            return jsonify({
                'error': 'Permission denied',
                'message': '没有权限修改其他用户信息'
            }), 403
        
        # 查询用户
        user = await User.get_by_id(db.session, user_id)
        if not user:
            return jsonify({
                'error': 'Not found',
                'message': '用户不存在'
            }), 404
            
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No input data',
                'message': '请提供要更新的数据'
            }), 400
            
        # 更新用户信息
        if 'username' in data and data['username'] != user.username:
            if await User.get_by_username(db.session, data['username']):
                return jsonify({
                    'error': 'Username taken',
                    'message': '用户名已被使用'
                }), 400
            user.username = data['username']
            
        if 'email' in data and data['email'] != user.email:
            if await User.get_by_email(db.session, data['email']):
                return jsonify({
                    'error': 'Email taken',
                    'message': '邮箱已被使用'
                }), 400
            user.email = data['email']
            
        if 'password' in data:
            user.set_password(data['password'])
            
        # 仅管理员可以修改这些字段
        if current_user.is_superuser:
            if 'is_active' in data:
                user.is_active = data['is_active']
            if 'is_superuser' in data:
                user.is_superuser = data['is_superuser']
                
        await db.session.commit()
        
        return jsonify({
            'message': '更新成功',
            'user': user.to_dict()
        })
        
    except Exception as e:
        await db.session.rollback()
        current_app.logger.error(f"Update user error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500

@bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
async def delete_user(user_id):
    """删除用户（仅管理员）
    
    Args:
        user_id: 用户 ID
        
    返回:
        {
            "message": "删除成功"
        }
    """
    try:
        # 查询用户
        user = await User.get_by_id(db.session, user_id)
        if not user:
            return jsonify({
                'error': 'Not found',
                'message': '用户不存在'
            }), 404
            
        # 不能删除自己
        if user.id == current_user.id:
            return jsonify({
                'error': 'Invalid operation',
                'message': '不能删除当前登录用户'
            }), 400
            
        await db.session.delete(user)
        await db.session.commit()
        
        return jsonify({'message': '删除成功'})
        
    except Exception as e:
        await db.session.rollback()
        current_app.logger.error(f"Delete user error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': '服务器内部错误'
        }), 500 