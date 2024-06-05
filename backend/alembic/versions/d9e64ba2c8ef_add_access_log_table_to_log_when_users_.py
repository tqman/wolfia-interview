"""Add access_log table to log when users log in and out.

Revision ID: d9e64ba2c8ef
Revises: a9128f06669e
Create Date: 2024-06-05 06:23:45.018890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9e64ba2c8ef'
down_revision: Union[str, None] = 'a9128f06669e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
    CREATE TYPE access_log_event_type AS ENUM ('LOGIN', 'LOGOUT');
    ''')
    
    op.execute('''
    CREATE TABLE access_log (
        id TEXT PRIMARY KEY,
        status access_log_event_type NOT NULL,
        user_id TEXT REFERENCES users(id) NOT NULL,
        internal_user_id TEXT REFERENCES users(id),
        access_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    ''')    

def downgrade() -> None:
    op.execute('''
    DROP TABLE access_log;
    ''')

    op.execute('''
    DROP TYPE access_log_event_type;
    ''')
    
