import datetime
import os
import uuid
from typing import Optional, Tuple

import jwt
from fastapi import HTTPException
from fastapi import status
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette.requests import Request

from auth.jwt_manager import (
    store_user_session,
    JWT_ALGORITHM, create_access_token,
)
from data.database import read_write_session, read_only_session, BaseModel
from data.tables import Organization, User, UserStatus, UserSession
from log import logger

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class UserRequest(BaseModel):
    email: str
    name: Optional[str]
    organization: Optional[str]
    internal_email: Optional[str]

def create_or_fetch_user(user_request: UserRequest) -> str:
    with read_write_session() as session:
        user = session.query(User).filter_by(email=user_request.email).first()
        if user:
            token = create_new_user_session(session,
                                            user.email,
                                            user_request.internal_email)
            return token
        elif user_request.organization and user_request.name and user_request.email:
            organization = Organization(
                id=str(uuid.uuid4()),
                name=user_request.organization,
                hd=user_request.email.split("@")[1],
                image="",
            )
            session.add(organization)
            session.flush()
            user = User(
                id=str(uuid.uuid4()),
                email=user_request.email,
                name=user_request.name,
                is_internal=False,
                status=UserStatus.ACTIVE,
                organization_id=organization.id,
                profile_image="",
            )
            session.add(user)
            session.flush()
            token = create_new_user_session(session, user.email)
            return token
        else:
            return create_new_user_session(session, user_request.email)


def create_new_user_session(session: Session,
                            email: str,
                            internal_email: str = None) -> str:
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        raise ValueError(f"No user found with email - {email}")

    internal_user =\
        session.query(User).filter(User.email == internal_email).first()

    internal_user_id = None

    if internal_user is not None:
        #This is a request by an "internal user" to impersonate another user.
        #We need to check some things. ARE they an internal user? And is
        #the targeted user NOT an internal user?
        if internal_user.is_internal is not True:
            raise PermissionError(f"User {internal_email} is not " +\
                                  "an internal user. Permission denied.")

        if user.is_internal is True:
            raise PermissionError(f"User {email} is not " +\
                                  "an external user. Permission denied.")

        internal_user_id = internal_user.id

    jti, jwt_token = create_access_token(user.id)

    store_user_session(user.id, jti, internal_user_id)

    return jwt_token

def logout_user_session(user_id: str, jti: str):
    with read_write_session() as session:
        user_sessions = (
            session.query(UserSession)
            .filter(
                and_(
                    UserSession.user_id == user_id,
                    UserSession.jti == jti,
                    UserSession.end_at.is_(None)
                )
            )
            .all()
        )
        for user_session in user_sessions:
            logger.info(f"Ending user session - {user_session.id} for user - {user_id}")
            user_session.status = "logged_out"
            user_session.end_at = datetime.datetime.now(datetime.UTC)
        logger.info(f"User logged out: {user_id}")


def authenticate_token(token: str) -> Tuple[Optional[User], Optional[User]]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        jti = payload["jti"]
    except jwt.ExpiredSignatureError as e:
        logger.warning(f"Expired JWT token: {e}")
        return None, None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid JWT token: {e}")
        return None, None

    with read_only_session() as session:
        result = (
            session.query(UserSession)
            .join(User, UserSession.user_id == User.id)
            .filter(UserSession.jti == jti)
            .first()
        )
        if result and result.end_at is None:
            internal_user = result.internal_user \
                if result.internal_user_id is not None else None

            return result.user, internal_user
        else:
            logger.warning(f"Failed authentication attempt with token: {jti}")
            return None, None


def get_current_user(request: Request) -> Tuple[Optional[User], Optional[User]]:
    jwt_token = request.cookies.get("access_token")
    if jwt_token:
        return authenticate_token(jwt_token)
    return None, None


def decode_jwt(token: str, field: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload.get(field)
    except jwt.ExpiredSignatureError as e:
        logger.warning(f"Expired JWT token: {e}")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid JWT token: {e}")
    return None


def get_jti_from_request(request: Request) -> Optional[str]:
    jwt_token = request.cookies.get("access_token")
    if jwt_token:
        return decode_jwt(jwt_token, "jti")
    return None


def authenticate_user(request: Request) -> Tuple[[User], [User]]:
    """
    Returns the user if the token is valid and the user is active, else raises an exception
    """
    (user, internal_user) = get_current_user(request)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED")

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ORGANIZATION_REQUIRED")
    return user, internal_user
