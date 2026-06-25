"""
FastAPI dependencies for protected routes.

Usage in a route:
    @router.get("/me")
    def get_me(current_user: User = Depends(get_current_user)):
        ...

    @router.get("/admin-only")
    def admin_route(current_user: User = Depends(require_role(RoleEnum.PLACEMENT_OFFICER))):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.database.session import get_db
from app.models.user import RoleEnum, User

# tokenUrl points Swagger's "Authorize" button at the login endpoint so
# /docs can be used to obtain and apply a token interactively.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_error
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    return user


def require_role(*allowed_roles: RoleEnum):
    """
    Returns a dependency that only allows users whose role is in
    `allowed_roles`. Usage: Depends(require_role(RoleEnum.RECRUITER))
    or Depends(require_role(RoleEnum.RECRUITER, RoleEnum.PLACEMENT_OFFICER))
    for multiple allowed roles.
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of the following roles: "
                f"{', '.join(r.value for r in allowed_roles)}.",
            )
        return current_user

    return role_checker
