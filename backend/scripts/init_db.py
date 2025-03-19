import asyncio
from sqlalchemy import text
from config.database import engine, Base
from config.settings import settings

# 导入所有模型以确保它们被注册到 Base.metadata
from models.user import User

async def init_db():
    """初始化数据库"""
    try:
        # 删除所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            print("数据库表删除成功")
        
        # 创建所有表
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("数据库表创建成功")
        
        # 创建默认管理员用户
        from config.database import AsyncSessionLocal
        
        async with AsyncSessionLocal() as session:
            # 检查是否已存在管理员用户
            admin = await User.get_by_username(session, "admin")
            if not admin:
                admin = User(
                    username="admin",
                    email="admin@example.com",
                    is_active=True,
                    is_superuser=True
                )
                admin.set_password("admin123")
                print(f"新管理员用户密码哈希值: {admin.hashed_password}")
                session.add(admin)
                await session.commit()
                print("管理员用户创建成功")
            else:
                print(f"现有管理员用户密码哈希值: {admin.hashed_password}")
                # 更新现有管理员用户的密码
                admin.set_password("admin123")
                print(f"更新后的密码哈希值: {admin.hashed_password}")
                await session.commit()
                print("管理员用户密码更新成功")
                
    except Exception as e:
        print(f"数据库初始化失败：{str(e)}")
        raise

async def main():
    """主函数"""
    try:
        await init_db()
        print("数据库初始化成功")
    except Exception as e:
        print(f"数据库初始化失败：{str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 