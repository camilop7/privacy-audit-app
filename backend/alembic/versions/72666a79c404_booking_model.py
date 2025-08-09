"""booking model

Revision ID: 72666a79c404
Revises: 20a6b5fda42d
Create Date: 2025-08-09 17:34:21.010736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '72666a79c404'
down_revision: Union[str, None] = '20a6b5fda42d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 0) Ensure the new enum exists
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'booking_status') THEN
        CREATE TYPE booking_status AS ENUM ('pending','confirmed','cancelled','completed');
      END IF;
    END$$;
    """)

    # 1) Drop old default that references the old type
    op.execute("ALTER TABLE bookings ALTER COLUMN status DROP DEFAULT")

    # 2) Alter column type with an explicit cast via text
    op.alter_column(
        'bookings', 'status',
        existing_type=postgresql.ENUM('pending', 'confirmed', 'completed', 'cancelled', name='bookingstatus'),
        type_=sa.Enum('pending', 'confirmed', 'cancelled', 'completed', name='booking_status'),
        postgresql_using="status::text::booking_status",
        existing_nullable=False,
    )

    # 3) Set new default on the new type
    op.execute("ALTER TABLE bookings ALTER COLUMN status SET DEFAULT 'pending'::booking_status")

    # 4) Tidy up: drop the old enum type if nothing uses it
    op.execute("DROP TYPE IF EXISTS bookingstatus")


def downgrade() -> None:
    # Recreate old enum if needed
    op.execute("""
    DO $$
    BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'bookingstatus') THEN
        CREATE TYPE bookingstatus AS ENUM ('pending','confirmed','completed','cancelled');
      END IF;
    END$$;
    """)

    # Drop default first
    op.execute("ALTER TABLE bookings ALTER COLUMN status DROP DEFAULT")

    # Cast back to old enum via text
    op.alter_column(
        'bookings', 'status',
        existing_type=sa.Enum('pending', 'confirmed', 'cancelled', 'completed', name='booking_status'),
        type_=postgresql.ENUM('pending', 'confirmed', 'completed', 'cancelled', name='bookingstatus'),
        postgresql_using="status::text::bookingstatus",
        existing_nullable=False,
    )

    # Restore old default
    op.execute("ALTER TABLE bookings ALTER COLUMN status SET DEFAULT 'pending'::bookingstatus")

    # Drop the new enum type
    op.execute("DROP TYPE IF EXISTS booking_status")
