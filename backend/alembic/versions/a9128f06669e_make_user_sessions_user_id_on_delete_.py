"""Make user_sessions.user_id ON DELETE CASCADE so that we can actually delete users in the future

Revision ID: a9128f06669e
Revises: 2944f18c79b3
Create Date: 2024-06-05 02:23:07.798779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9128f06669e'
down_revision: Union[str, None] = '2944f18c79b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  # Make user_sessions.user_id be ON DELETE CASCADE so that it is possible
  # to delete a user
    op.execute('''
    -- We have to drop the existing foreign key first
    ALTER TABLE user_sessions 
        DROP CONSTRAINT user_sessions_user_id_fkey;

    -- Now add it back with ON DELETE CASCADE
    ALTER TABLE user_sessions
        ADD CONSTRAINT user_sessions_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
    ''')    

def downgrade() -> None:
  # Undo the above
    op.execute('''
    -- We have to drop the existing foreign key first
    ALTER TABLE user_sessions 
        DROP CONSTRAINT user_sessions_user_id_fkey;

    -- Now add it back without ON DELETE CASCADE
    ALTER TABLE user_sessions
        ADD CONSTRAINT user_sessions_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users(id);
    ''')    
