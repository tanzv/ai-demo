from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """令牌模型"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """令牌载荷模型"""
    sub: int = Field(..., description="用户 ID")
    exp: int = Field(..., description="过期时间")

class UserLogin(BaseModel):
    """用户登录模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpass"
            }
        }

class UserCreate(BaseModel):
    """用户创建模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    is_superuser: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secretpass",
                "is_superuser": False
            }
        }

class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True 