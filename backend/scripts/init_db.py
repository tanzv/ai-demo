import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from config.database import engine, AsyncSessionLocal, Base
from config.settings import settings
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_database() -> None:
    """创建数据库（如果不存在）"""
    try:
        conn = await asyncpg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database="postgres",
        )
        
        # 检查数据库是否存在
        result = await conn.fetchrow(
            "SELECT 1 FROM pg_database WHERE datname = $1",
            settings.POSTGRES_DB,
        )
        
        if not result:
            # 创建数据库
            await conn.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"数据库 {settings.POSTGRES_DB} 创建成功")
        
        await conn.close()
    except Exception as e:
        print(f"创建数据库时出错: {e}")
        raise

async def create_tables() -> None:
    """创建数据库表"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("数据库表创建成功")
    except Exception as e:
        print(f"创建数据库表时出错: {e}")
        raise

async def create_admin_user(session: AsyncSession) -> None:
    """创建管理员用户（如果不存在）"""
    try:
        # 检查管理员用户是否存在
        admin = await session.get(User, 1)
        
        if not admin:
            # 创建管理员用户
            admin = User(
                id=1,
                username="admin",
                email="admin@example.com",
                hashed_password=pwd_context.hash("admin123"),
                is_active=True,
                is_superuser=True,
            )
            session.add(admin)
            await session.commit()
            print("管理员用户创建成功")
        else:
            print("管理员用户已存在")
    except Exception as e:
        print(f"创建管理员用户时出错: {e}")
        await session.rollback()
        raise

async def init_app() -> None:
    """初始化应用"""
    # 创建数据库（如果不存在）
    await create_database()
    
    # 创建数据库表
    await create_tables()
    
    # 创建管理员用户
    async with AsyncSessionLocal() as session:
        await create_admin_user(session)

if __name__ == "__main__":
    asyncio.run(init_app()) 