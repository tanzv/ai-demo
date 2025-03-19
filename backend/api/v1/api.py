from flask import Blueprint
from flask_restx import Api
from api.v1.health import ns as health_ns
from api.v1.endpoints.auth import ns as auth_ns
from api.v1.endpoints.users import ns as users_ns
from api.v1.models import create_user_info_model

# 创建主路由蓝图
api_router = Blueprint('api_v1', __name__)

# 创建 API 实例
api = Api(
    api_router,
    version='1.0',
    title='AI Demo API',
    description='AI Demo 项目的 API 文档',
    doc='/docs',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT token 认证'
        }
    },
    validate=True,
    ordered=True
)

# 创建共享模型
user_info_model = create_user_info_model(api)

# 注册命名空间
api.add_namespace(health_ns, path='/health')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')

# 错误处理
@api_router.errorhandler(Exception)
async def handle_error(error):
    """全局错误处理"""
    return {
        "error": "Internal Server Error",
        "message": str(error)
    }, 500 