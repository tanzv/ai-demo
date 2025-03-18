from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from config.settings import settings

# 创建数据库 URL
DATABASE_URL = settings.database_url

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 创建 Flask-SQLAlchemy 实例
db = SQLAlchemy()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(app):
    """初始化数据库"""
    from models.user import User  # noqa
    
    # 配置 Flask-SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化 Flask-SQLAlchemy
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        db.create_all() 