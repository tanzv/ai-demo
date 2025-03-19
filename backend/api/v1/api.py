from flask import Blueprint

# 创建主路由蓝图
api_router = Blueprint('api_v1', __name__)

# 导入并注册子路由
from .endpoints import auth, users

# 认证相关路由
api_router.register_blueprint(auth.bp, url_prefix='/auth')

# 用户相关路由
api_router.register_blueprint(users.bp, url_prefix='/users')

# 错误处理
@api_router.errorhandler(Exception)
async def handle_error(error):
    """全局错误处理"""
    return {
        "error": "Internal Server Error",
        "message": str(error)
    }, 500 