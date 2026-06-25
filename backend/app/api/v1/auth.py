from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.database.session import get_db
from app.models.user import RoleEnum, User
from app.schemas.auth import TokenResponse, UserLoginRequest, UserOut, UserRegisterRequest
from app.services.auth_service import authenticate_user, build_token_for_user, register_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """Creates a new account and immediately returns a usable access token,
    so the frontend doesn't need a separate login call right after signup."""
    user = register_user(db, payload)
    token = build_token_for_user(user)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Uses the standard OAuth2 password-flow form (username + password
    fields) rather than a JSON body, so this endpoint works directly with
    Swagger UI's "Authorize" button and any standard OAuth2 client.
    `form_data.username` is treated as the email address.
    """
    credentials = UserLoginRequest(email=form_data.username, password=form_data.password)
    user = authenticate_user(db, credentials)
    token = build_token_for_user(user)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.post("/login/json", response_model=TokenResponse)
def login_json(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    JSON-body equivalent of /login, for frontend code that prefers
    sending `{"email": ..., "password": ...}` over a form-encoded body.
    Both endpoints produce an identical token.
    """
    user = authenticate_user(db, payload)
    token = build_token_for_user(user)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)) -> UserOut:
    """Returns the profile of whichever user the bearer token belongs to."""
    return UserOut.model_validate(current_user)


@router.get("/placement-officer-check")
def placement_officer_check(
    current_user: User = Depends(require_role(RoleEnum.PLACEMENT_OFFICER)),
) -> dict[str, str]:
    """
    Demonstrates role-gated access — only usable by Placement Officer
    accounts. Exists purely to make role-based access control testable in
    this step; real Placement Officer routes (Module 10: Placement
    Analytics) replace this later.
    """
    return {"message": f"Welcome, {current_user.full_name}. You have Placement Officer access."}
