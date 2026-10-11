"""TEMPLATE: Alembic environment. Runs every time you call `alembic ...`.

Job: tell Alembic (1) which DB to talk to and (2) what the models look like (Base.metadata),
so `alembic revision --autogenerate` can diff models vs. database.
"""
from alembic import context
from sqlalchemy import engine_from_config, pool

from app import models  # noqa: F401  importing registers every table on Base.metadata
from app.config import settings
from app.db import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)  # single source of truth: .env
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """`alembic upgrade head --sql`: print SQL instead of running it (for DBAs / review)."""
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Normal mode: connect and apply migrations."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # one-off command, no pool needed
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # lets ALTER TABLE work on SQLite (copies the table behind the scenes)
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
