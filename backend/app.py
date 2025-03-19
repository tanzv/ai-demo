from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from functools import wraps
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from config.database import init_db, Base, AsyncSessionLocal

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# 创建异步引擎
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.IS_DEVELOPMENT,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

def async_route(f):
    """异步路由装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

async def init_app_async():
    """异步初始化应用"""
    await init_db()

def create_app(config_object=None):
    """创建 Flask 应用
    
    Args:
        config_object: 配置对象
        
    Returns:
        Flask: Flask 应用实例
    """
    app = Flask(__name__)
    
    # 配置应用
    app.config.from_object(config_object or settings)
    
    # 配置 SQLAlchemy（使用同步 URL）
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SYNC_DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = settings.IS_DEVELOPMENT
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    }
    
    # 初始化扩展
    db.init_app(app)
    with app.app_context():
        Base.metadata.bind = db.engine
    
    login_manager.init_app(app)
    CORS(app, 
         resources={r"/api/*": {"origins": settings.CORS_ORIGINS}},
         supports_credentials=settings.CORS_CREDENTIALS)
    
    # 用户加载器
    @login_manager.user_loader
    @async_route
    async def load_user(user_id):
        from models.user import User
        async with AsyncSessionLocal() as session:
            return await User.get_by_id(session, int(user_id))
    
    # 注册蓝图
    from api.v1.api import api_router
    app.register_blueprint(api_router, url_prefix='/api/v1')
    
    # 错误处理
    @app.errorhandler(404)
    async def not_found_error(error):
        """处理 404 错误"""
        return {"error": "Not Found", "message": "请求的资源不存在"}, 404

    @app.errorhandler(500)
    async def internal_error(error):
        """处理 500 错误"""
        return {"error": "Internal Server Error", "message": "服务器内部错误"}, 500

    # 健康检查
    @app.route('/health')
    async def health_check():
        """健康检查接口"""
        return {"status": "healthy", "message": "服务运行正常"}

    # 关闭时执行
    @app.teardown_appcontext
    async def shutdown(exception=None):
        """应用关闭时执行的操作"""
        # 在这里添加清理代码
        app.logger.info("应用正在关闭")
    
    # 将 WSGI 应用转换为 ASGI 应用
    asgi_app = WsgiToAsgi(app)
    
    # 初始化数据库
    asyncio.run(init_app_async())
    app.logger.info("数据库连接池已初始化")
    
    return asgi_app 