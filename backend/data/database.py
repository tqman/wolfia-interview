import os
from contextlib import contextmanager
from datetime import datetime, timezone

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session
from sqlalchemy.orm import sessionmaker

from log import logger

DB_USER = os.getenv("POSTGRES_USER")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = 5432
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=46,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    connect_args={"options": "-c statement_timeout=60000"}
)
Session = scoped_session(sessionmaker(bind=engine))


class BaseModel(PydanticBaseModel):
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.replace(tzinfo=timezone.utc).isoformat()
        }
    }


Base = declarative_base()


@contextmanager
def read_only_session():
    session = Session()
    try:
        yield session
    except Exception as e:
        logger.error(f"Session exception: {e}", exc_info=True)
    finally:
        session.close()


@contextmanager
def read_write_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"Session rollback due to error: {e}", exc_info=True)
        session.rollback()
        raise
    finally:
        session.close()


class Response(BaseModel):
    message: str
