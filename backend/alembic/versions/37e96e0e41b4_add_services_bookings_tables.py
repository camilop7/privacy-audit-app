"""Add services & bookings tables

Revision ID: 37e96e0e41b4
Revises: 202504191200
Create Date: 2025-05-09 21:32:22.819366
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '37e96e0e41b4'
down_revision = '202504191200'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- 1) Create bookingstatus enum type if not exists ---
    bookingstatus = postgresql.ENUM(
        'pending', 'confirmed', 'completed', 'cancelled',
        name='bookingstatus'
    )
    bookingstatus.create(op.get_bind(), checkfirst=True)

    # --- 2) Modify services table ---
    op.add_column(
        'services',
        sa.Column('price', sa.Float(), nullable=False, server_default="0")
    )
    op.add_column(
        'services',
        sa.Column('duration_minutes', sa.Float(), nullable=False, server_default="0")
    )
    op.alter_column(
        'services',
        'description',
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        'services',
        'category',
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.drop_constraint('services_name_key', 'services', type_='unique')
    op.drop_column('services', 'is_active')

    # --- 3) Modify bookings table ---
    # 3a) Add the new scheduled_for column (replace scheduled_time)
    op.add_column(
        'bookings',
        sa.Column(
            'scheduled_for',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        )
    )

    # 3b) Convert status -> bookingstatus enum
    op.alter_column(
        'bookings',
        'status',
        existing_type=sa.VARCHAR(length=50),
        type_=bookingstatus,
        postgresql_using="status::bookingstatus",
        nullable=False,
        server_default=sa.text("'pending'")
    )

    # 3c) Ensure user_id & service_id are NOT NULL
    op.alter_column(
        'bookings',
        'user_id',
        existing_type=sa.UUID(),
        nullable=False
    )
    op.alter_column(
        'bookings',
        'service_id',
        existing_type=sa.UUID(),
        nullable=False
    )

    # 3d) Recreate foreign keys with proper ondelete behavior
    op.drop_constraint('bookings_user_id_fkey', 'bookings', type_='foreignkey')
    op.drop_constraint('bookings_service_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'fk_bookings_user',
        'bookings', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_bookings_service',
        'bookings', 'services',
        ['service_id'], ['id'],
        ondelete='SET NULL'
    )

    # 3e) Drop old columns
    op.drop_column('bookings', 'scheduled_time')
    op.drop_column('bookings', 'notes')


def downgrade() -> None:
    # --- 1) Revert bookings table ---
    op.add_column(
        'bookings',
        sa.Column('notes', sa.TEXT(), nullable=True)
    )
    op.add_column(
        'bookings',
        sa.Column(
            'scheduled_time',
            postgresql.TIMESTAMP(timezone=True),
            nullable=True
        )
    )

    op.drop_constraint('fk_bookings_service', 'bookings', type_='foreignkey')
    op.drop_constraint('fk_bookings_user', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_service_id_fkey',
        'bookings', 'services',
        ['service_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'bookings_user_id_fkey',
        'bookings', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

    op.alter_column(
        'bookings',
        'service_id',
        existing_type=sa.UUID(),
        nullable=True
    )
    op.alter_column(
        'bookings',
        'user_id',
        existing_type=sa.UUID(),
        nullable=True
    )

    # Revert enum back to VARCHAR
    op.alter_column(
        'bookings',
        'status',
        existing_type=postgresql.ENUM(
            'pending', 'confirmed', 'completed', 'cancelled',
            name='bookingstatus'
        ),
        type_=sa.VARCHAR(length=50),
        postgresql_using="status::text",
        existing_nullable=False
    )

    op.drop_column('bookings', 'scheduled_for')

    # --- 2) Revert services table ---
    op.add_column(
        'services',
        sa.Column('is_active', sa.BOOLEAN(), nullable=True)
    )
    op.create_unique_constraint(
        'services_name_key',
        'services',
        ['name']
    )
    op.alter_column(
        'services',
        'category',
        existing_type=sa.VARCHAR(length=100),
        nullable=False
    )
    op.alter_column(
        'services',
        'description',
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=True
    )
    op.drop_column('services', 'duration_minutes')
    op.drop_column('services', 'price')

    # --- 3) Drop the enum type ---
    bookingstatus = postgresql.ENUM(
        'pending', 'confirmed', 'completed', 'cancelled',
        name='bookingstatus'
    )
    bookingstatus.drop(op.get_bind(), checkfirst=True)
