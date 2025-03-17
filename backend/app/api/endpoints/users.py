from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....schemas import user as user_schemas
from ....models.user import User
from ....core import security
from ....api import deps

router = APIRouter()

@router.post("/", response_model=user_schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册",
        )
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被使用",
        )
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=User.get_password_hash(user_in.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=user_schemas.User)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=user_schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: user_schemas.UserUpdate,
) -> Any:
    """
    Update own user.
    """
    if user_in.username is not None:
        user = db.query(User).filter(
            User.username == user_in.username,
            User.id != current_user.id
        ).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="该用户名已被使用",
            )
        current_user.username = user_in.username
    
    if user_in.email is not None:
        user = db.query(User).filter(
            User.email == user_in.email,
            User.id != current_user.id
        ).first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="该邮箱已被注册",
            )
        current_user.email = user_in.email
    
    if user_in.password is not None:
        current_user.hashed_password = User.get_password_hash(user_in.password)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user 