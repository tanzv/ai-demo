from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_restx import Namespace, Resource, fields
from utils.auth import (
    create_access_token,
    create_refresh_token,
    token_required
)
from models.user import User
from config.database import AsyncSessionLocal
import asyncio

# 创建命名空间
ns = Namespace('auth', description='认证相关接口')

# 定义请求/响应模型
login_model = ns.model('LoginRequest', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码')
})

register_model = ns.model('RegisterRequest', {
    'username': fields.String(required=True, description='用户名'),
    'email': fields.String(required=True, description='邮箱'),
    'password': fields.String(required=True, description='密码')
})

token_model = ns.model('TokenResponse', {
    'access_token': fields.String(required=True, description='访问令牌'),
    'token_type': fields.String(required=True, description='令牌类型'),
    'expires_in': fields.Integer(required=True, description='过期时间（秒）')
})

# 创建认证蓝图
bp = Blueprint('auth', __name__)

@ns.route('/login')
class Login(Resource):
    @ns.doc('login',
            description='用户登录',
            responses={
                200: ('成功', token_model),
                401: '用户名或密码错误',
                500: '服务器内部错误'
            })
    @ns.expect(login_model)
    @ns.marshal_with(token_model)
    def post(self):
        """用户登录"""
        try:
            data = request.get_json()
            current_app.logger.debug(f"收到登录请求：{data}")
            
            if not data:
                current_app.logger.warning("无效的请求数据")
                return {'message': '无效的请求数据'}, 400
                
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                current_app.logger.warning("用户名或密码为空")
                return {'message': '用户名和密码不能为空'}, 400
            
            # 使用 asyncio.run 运行异步代码
            async def login_async():
                async with AsyncSessionLocal() as session:
                    current_app.logger.debug(f"查询用户：{username}")
                    user = await User.get_by_username(session, username)
                    
                    if not user:
                        current_app.logger.warning(f"用户不存在：{username}")
                        return {'message': '用户名或密码错误'}, 401
                        
                    current_app.logger.debug(f"验证密码：{username}")
                    try:
                        if not user.verify_password(password):
                            current_app.logger.warning(f"密码错误：{username}")
                            return {'message': '用户名或密码错误'}, 401
                    except Exception as e:
                        current_app.logger.error(f"密码验证失败：{str(e)}")
                        return {'message': '服务器内部错误'}, 500
                        
                    if not user.is_active:
                        current_app.logger.warning(f"账户未激活：{username}")
                        return {'message': '账户未激活'}, 403
                    
                    # 创建访问令牌
                    try:
                        current_app.logger.debug(f"创建访问令牌：{username}")
                        access_token = create_access_token(user_id=user.id)
                        current_app.logger.info(f"用户 {username} 登录成功")
                        
                        response = {
                            'access_token': access_token,
                            'token_type': 'bearer',
                            'expires_in': 3600  # 1小时过期
                        }
                        current_app.logger.debug(f"返回响应：{response}")
                        return response
                        
                    except Exception as e:
                        current_app.logger.error(f"创建令牌失败：{str(e)}")
                        return {'message': '服务器内部错误'}, 500
            
            # 运行异步函数
            return asyncio.run(login_async())
                    
        except Exception as e:
            current_app.logger.error(f"登录过程发生错误：{str(e)}")
            return {'message': '服务器内部错误'}, 500

@ns.route('/register')
class Register(Resource):
    @ns.doc('register',
            description='用户注册',
            responses={
                201: '注册成功',
                400: '用户名或邮箱已存在',
                500: '服务器内部错误'
            })
    @ns.expect(register_model)
    async def post(self):
        """用户注册"""
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        async with AsyncSessionLocal() as session:
            if await User.get_by_username(session, username):
                return {'message': '用户名已存在'}, 400
            if await User.get_by_email(session, email):
                return {'message': '邮箱已存在'}, 400
            
            user = User(
                username=username,
                email=email,
                is_active=True,
                is_superuser=False
            )
            user.set_password(password)
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            return {'message': '注册成功'}, 201

@ns.route('/logout')
class Logout(Resource):
    @ns.doc('logout',
            description='用户登出',
            security='apikey',
            responses={
                200: '登出成功',
                401: '未认证',
                500: '服务器内部错误'
            })
    @token_required
    async def post(self):
        """用户登出"""
        return {'message': '登出成功'}

@ns.route('/me')
class CurrentUser(Resource):
    @ns.doc('get_current_user',
            description='获取当前用户信息',
            security='apikey',
            responses={
                200: ('成功', 'UserInfo'),
                401: '未认证',
                500: '服务器内部错误'
            })
    @ns.marshal_with('UserInfo')
    @token_required
    async def get(self):
        """获取当前用户信息"""
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, current_user.id)
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }

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