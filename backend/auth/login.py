from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import Response

from auth.jwt_manager import USER_SESSION_EXPIRY_DURATION_IN_DAYS
from auth.models import UserResponse
from auth.user import create_or_fetch_user, authenticate_user, get_jti_from_request, logout_user_session, UserRequest
from data.database import read_only_session
from data.tables import User, Organization
from log import logger

router = APIRouter()


@router.post(
    "/auth/login",
    operation_id="login",
    description="Login user and create a user session."
)
async def login(user_request: UserRequest):
    try:
        token = create_or_fetch_user(user_request)
        response = Response()
        response.delete_cookie("access_token")
        response.set_cookie(
            key="access_token",
            value=token,
            max_age=int(timedelta(days=USER_SESSION_EXPIRY_DURATION_IN_DAYS).total_seconds()),
            domain=None,
            secure=False,
            httponly=False,
            samesite="lax",
        )
        return response
    except Exception as e:
        logger.error(f"Exception occurred during auth: {e}")
        raise HTTPException(status_code=500, detail="Exception occurred during auth")


@router.post(
    "/auth/logout",
    operation_id="logout",
    description="Logout user."
)
async def logout(request: Request, response: Response, user: User = Depends(authenticate_user)):
    jti = get_jti_from_request(request)
    logout_user_session(user.id, jti)
    response.delete_cookie("access_token")
    return response


@router.get(
    "/auth/me",
    operation_id="currentUser",
    description="Get the current user.",
    response_model=UserResponse,
)
async def me(user: User = Depends(authenticate_user)) -> UserResponse:
    with read_only_session() as session:
        user_data = session.query(
            User.id,
            User.email,
            User.name,
            User.is_internal,
            User.profile_image,
            User.organization_id,
            User.created_at,
            User.updated_at,
            User.status,
        ).filter(User.email == user.email).first()

        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")

        organization_name = None
        if user_data.organization_id:
            organization = session.query(Organization.name).filter_by(id=user_data.organization_id).first()
            organization_name = organization.name if organization else None

        return UserResponse(
            id=user_data.id,
            email=user_data.email,
            name=user_data.name,
            organization_name=organization_name,
            is_internal=user_data.is_internal,
            profile_image=user_data.profile_image,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at,
            status=user_data.status,
        )
