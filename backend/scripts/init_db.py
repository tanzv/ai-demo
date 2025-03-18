import os
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from config.settings import settings
from models.user import User
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功")

def create_admin_user():
    """创建默认管理员用户"""
    db = SessionLocal()
    try:
        # 检查是否已存在管理员用户
        admin = db.query(User).filter(User.username == settings.get('admin.username')).first()
        if not admin:
            admin = User(
                username=settings.get('admin.username'),
                email=settings.get('admin.email'),
                hashed_password=pwd_context.hash(settings.get('admin.password')),
                is_active=True,
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("默认管理员用户创建成功")
        else:
            print("默认管理员用户已存在")
    except Exception as e:
        print(f"创建管理员用户时出错: {e}")
        db.rollback()
    finally:
        db.close()

def init_postgres_db():
    """初始化 PostgreSQL 数据库"""
    try:
        # 连接到 PostgreSQL 服务器
        conn = psycopg2.connect(
            dbname='postgres',
            user=settings.get('database.user'),
            password=settings.get('database.password'),
            host=settings.get('database.host'),
            port=settings.get('database.port')
        )
        conn.autocommit = True
        cur = conn.cursor()

        # 检查数据库是否存在
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", 
                   (settings.get('database.db_name'),))
        exists = cur.fetchone()

        if not exists:
            # 创建数据库
            db_name = settings.get('database.db_name')
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"数据库 '{db_name}' 创建成功")
        else:
            print(f"数据库 '{settings.get('database.db_name')}' 已存在")

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"创建数据库时出错: {e}")
        return False

def init_app():
    """初始化应用数据库和管理员用户"""
    if init_postgres_db():
        create_tables()
        create_admin_user()
        print("数据库初始化完成")

if __name__ == "__main__":
    print("开始创建初始数据")
    init_app()
    print("初始数据创建完成") 