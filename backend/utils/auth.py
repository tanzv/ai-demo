from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from flask import current_app, jsonify, request, g
from config.settings import settings
from functools import wraps
from flask_login import current_user

from models.user import User
from config.database import AsyncSessionLocal

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌
    
    Args:
        user_id: 用户 ID
        expires_delta: 过期时间
        
    Returns:
        str: JWT 令牌
    """
    try:
        current_app.logger.debug(f"开始创建访问令牌，用户 ID：{user_id}")
        
        if not user_id:
            current_app.logger.error("用户 ID 为空")
            raise ValueError("用户 ID 不能为空")
            
        if not settings.SECRET_KEY:
            current_app.logger.error("SECRET_KEY 未设置")
            raise ValueError("SECRET_KEY 未设置")
            
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            current_app.logger.debug(f"使用默认过期时间：{expires_delta}")
            
        expire = datetime.utcnow() + expires_delta
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "type": "access"
        }
        
        current_app.logger.debug(f"准备编码数据：{to_encode}")
        
        token = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        current_app.logger.debug("访问令牌创建成功")
        return token
        
    except Exception as e:
        current_app.logger.error(f"创建访问令牌失败：{str(e)}")
        raise

def create_refresh_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """创建刷新令牌
    
    Args:
        user_id: 用户 ID
        expires_delta: 过期时间
        
    Returns:
        str: JWT 令牌
    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def verify_token(token: str) -> Optional[int]:
    """验证 JWT 令牌
    
    Args:
        token: JWT 令牌
        
    Returns:
        Optional[int]: 用户 ID，如果令牌无效则返回 None
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = int(payload["sub"])
        return user_id
    except (JWTError, ValueError):
        return None

def token_required(f):
    """JWT 令牌验证装饰器"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'error': 'Unauthorized',
                'message': '缺少认证令牌'
            }), 401
            
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        if not user_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': '无效的认证令牌'
            }), 401
            
        # 获取用户
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': '用户不存在'
                }), 401
                
            if not user.is_active:
                return jsonify({
                    'error': 'Forbidden',
                    'message': '用户账户未激活'
                }), 403
                
            # 将用户对象存储在 g 对象中，以便视图函数访问
            g.user = user
            return await f(*args, **kwargs)
        
    return decorated_function

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'error': 'Unauthorized',
                'message': '请先登录'
            }), 401
            
        if not current_user.is_superuser:
            return jsonify({
                'error': 'Permission denied',
                'message': '需要管理员权限'
            }), 403
            
        return await f(*args, **kwargs)
    return decorated_function 