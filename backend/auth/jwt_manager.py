import datetime
import os
import uuid
from datetime import timedelta

import jwt

from data.database import read_write_session
from data.tables import UserSession, AccessLogEventType, AccessLog

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
USER_SESSION_EXPIRY_DURATION_IN_DAYS = 180
IMPERSONATION_SESSION_EXPIRATION_DURATION_IN_MINS = 60

def create_access_token(user_id: str):
    """
    Create a JWT access token for the given user ID.

    Args:
        user_id (str): The user ID for which the token is being created.

    Returns:
        str: A JWT token as a string.
    """
    try:
        jti = str(uuid.uuid4())
        issuer = "wolfia"  # Issuer of the token
        expiration = datetime.datetime.now(datetime.UTC) + timedelta(days=USER_SESSION_EXPIRY_DURATION_IN_DAYS)

        payload = {
            "sub": user_id,  # Subject of the JWT
            "iss": issuer,  # Issuer of the JWT
            "jti": jti,  # Unique identifier for the JWT
            "exp": expiration,  # Expiration time
            "iat": datetime.datetime.now(datetime.UTC),  # Issued at
        }
        return jti, jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    except Exception as e:
        raise TokenCreationError(f"Error creating token for user {user_id}: {e}")


def store_user_session(user_id: str, jti: str, internal_user_id: str = None):
    """
    Store a new user session in the database.

    Args:
        user_id (str): The user ID for the session.
        jti (str): The JWT token ID.
        internal_user_id (str): Optional internal user ID for impersonation

    Returns:
        str: The ID of the created user session.
    """
    if internal_user_id is not None:
        is_impersonation = True
    else:
        is_impersonation = False
    
    with read_write_session() as session:
        session_args = {'id' : str(uuid.uuid4()),
                        'user_id' : user_id,
                        'jti' : jti,
                        'expires_at' :\
                        session_expiration_timestamp(is_impersonation),
                        'created_at' : datetime.datetime.now(datetime.UTC)}

        #It's an internal user, let's note it on the table.
        if internal_user_id is not None:
            session_args['internal_user_id'] = internal_user_id
        
        user_session = UserSession(**session_args)

        session.add(user_session)

        #Now, let's note it in the access log as well:
        access_log_args = {'id' : str(uuid.uuid4()),
                           'user_id' : user_id,
                           'status' : AccessLogEventType.LOGIN}

        if internal_user_id is not None:
            access_log_args['internal_user_id'] =\
                internal_user_id
            
        access_log = AccessLog(**access_log_args)
            
        session.add(access_log)
        
        session.commit()
        return user_session.id

def session_expiration_timestamp(is_impersonation:bool = False):
    """
    Calculate the timestamp a session should expire at.

    Args:
        user_id (str): The user ID for the session.
        internal_user_id (str): Optional internal user ID for impersonation

    Returns:
        datetime: The datetime object for when the session should expire.
    """

    if not is_impersonation:
        expires_at_ts = datetime.datetime.now(datetime.UTC)
        + timedelta(days=USER_SESSION_EXPIRY_DURATION_IN_DAYS)
    else:
        expires_at_ts = datetime.datetime.now(datetime.UTC)
        + timedelta(minutes=IMPERSONATION_SESSION_EXPIRATION_DURATION_IN_MINS)

    return expires_at_ts
    
class TokenCreationError(Exception):
    """Raised when there is an issue in creating a JWT token."""
