from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


def register_user(db: Session, payload: UserRegisterRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLoginRequest) -> User:
    user = db.query(User).filter(User.email == payload.email).first()

    # Deliberately identical error for "no such user" and "wrong password" —
    # distinguishing them lets an attacker enumerate which emails are
    # registered.
    invalid_credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
    )

    if user is None:
        raise invalid_credentials_error
    if not verify_password(payload.password, user.hashed_password):
        raise invalid_credentials_error
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    return user


def build_token_for_user(user: User) -> str:
    return create_access_token(subject=user.id, extra_claims={"role": user.role.value})
