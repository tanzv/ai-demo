from datetime import datetime
from typing import Dict, Any, Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import Base

class User(UserMixin, Base):
    """用户模型
    
    属性:
        id: 主键
        username: 唯一用户名
        email: 唯一邮箱地址
        hashed_password: 加密密码
        is_active: 账户是否激活
        is_superuser: 是否具有管理员权限
        created_at: 账户创建时间
        updated_at: 最后更新时间
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=None, onupdate=datetime.utcnow)

    def set_password(self, password: str) -> None:
        """设置用户密码
        
        Args:
            password: 明文密码
        """
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """验证密码
        
        Args:
            password: 待验证的明文密码
            
        Returns:
            bool: 密码是否匹配
        """
        return check_password_hash(self.hashed_password, password)

    def to_dict(self) -> Dict[str, Any]:
        """转换用户对象为字典
        
        Returns:
            Dict[str, Any]: 用户数据字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str) -> Optional["User"]:
        """通过用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回 None
        """
        result = await db.execute(select(cls).filter(cls.username == username))
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str) -> Optional["User"]:
        """通过邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 邮箱地址
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回 None
        """
        result = await db.execute(select(cls).filter(cls.email == email))
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, user_id: int) -> Optional["User"]:
        """通过 ID 获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户 ID
            
        Returns:
            Optional[User]: 用户对象，如果不存在则返回 None
        """
        result = await db.execute(select(cls).filter(cls.id == user_id))
        return result.scalar_one_or_none() 