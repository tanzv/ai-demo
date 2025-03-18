from sqlalchemy import Boolean, Column, Integer, String, DateTime
from config.database import db
from flask_login import UserMixin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(db.Model, UserMixin):
    """User model for database"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=db.func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=db.func.now())

    def set_password(self, password):
        """Set password hash"""
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify password against hash"""
        return pwd_context.verify(password, self.hashed_password)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_superuser': self.is_superuser,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 