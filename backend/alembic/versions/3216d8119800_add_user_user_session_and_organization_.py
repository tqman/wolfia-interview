"""Add user, user_session and organization tables

Revision ID: 3216d8119800
Revises: 
Create Date: 2024-06-03 20:16:42.044331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3216d8119800'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Creating the organizations table
    op.execute('''
    CREATE TABLE organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        image TEXT,
        hd TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Creating the userstatus enum type
    op.execute('''
    CREATE TYPE userstatus AS ENUM ('ACTIVE', 'PENDING', 'DEACTIVATED');
    ''')

    # Creating the users table
    op.execute('''
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL,
        name TEXT NOT NULL,
        is_internal BOOLEAN NOT NULL DEFAULT FALSE,
        profile_image TEXT,
        organization_id TEXT REFERENCES organizations(id),
        status userstatus NOT NULL DEFAULT 'PENDING',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Creating the user_sessions table
    op.execute('''
    CREATE TABLE user_sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT REFERENCES users(id),
        jti TEXT NOT NULL DEFAULT '',
        expires_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        end_at TIMESTAMP,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    ''')

def downgrade():
    # Dropping the user_sessions table
    op.execute('''
    DROP TABLE user_sessions;
    ''')

    # Dropping the users table
    op.execute('''
    DROP TABLE users;
    ''')

    # Dropping the organizations table
    op.execute('''
    DROP TABLE organizations;
    ''')

    # Dropping the userstatus enum type
    op.execute('''
    DROP TYPE userstatus;
    ''')