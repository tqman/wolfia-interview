"""Add user_sessions.internal_user_id to allow for impersonation of other users.

Revision ID: 2944f18c79b3
Revises: 3216d8119800
Create Date: 2024-06-05 02:13:22.308946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2944f18c79b3'
down_revision: Union[str, None] = '3216d8119800'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  # Add the user_sessions.internal_user_id column which references
  # users.id. If the user gets deleted, we should also delete any sessions
  # that reference them.
    op.execute('''
    ALTER TABLE user_sessions 
        ADD COLUMN internal_user_id TEXT REFERENCES users(id) ON DELETE CASCADE
    ''')    

def downgrade() -> None:
  # And, remove the user_sessions.internal_user_id column
    op.execute('''
    ALTER TABLE user_sessions 
        DROP COLUMN internal_user_id
    ''')    

