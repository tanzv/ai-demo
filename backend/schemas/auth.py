from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: int
    exp: int

class UserLogin(BaseModel):
    """User login request schema"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class UserCreate(BaseModel):
    """User creation request schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    is_superuser: bool = False

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: str
    updated_at: str | None

    class Config:
        from_attributes = True 