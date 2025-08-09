"""booking model enum fix

Revision ID: 20a6b5fda42d
Revises: 37e96e0e41b4
Create Date: 2025-08-09 17:15:48.171446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20a6b5fda42d'
down_revision: Union[str, None] = '37e96e0e41b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
