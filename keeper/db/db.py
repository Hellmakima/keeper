"""
SQLite database management for Keeper.
Handles connection, schema creation, and core database operations.
"""
import os
import sqlite3
from contextlib import contextmanager
from typing import Optional

from keeper.constants import APP_DIR

# Database file path
DB_PATH = os.path.join(APP_DIR, "keeper.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize the database schema if it doesn't exist."""
    # Ensure app directory exists
    if not os.path.isdir(APP_DIR):
        os.makedirs(APP_DIR)

    from .schema import (
        CREATE_TABLE_TRACKABLES,
        CREATE_TABLE_TRACKABLE_EVENTS,
        CREATE_INDEX_EVENTS_TRACKABLE,
        CREATE_INDEX_EVENTS_CREATED_AT,
        CREATE_INDEX_TRACKABLES_PLUGIN,
    )
    with get_db() as conn:
        cursor = conn.cursor()

        # Trackables and events tables
        cursor.execute(CREATE_TABLE_TRACKABLES)
        cursor.execute(CREATE_TABLE_TRACKABLE_EVENTS)
        cursor.execute(CREATE_INDEX_EVENTS_TRACKABLE)
        cursor.execute(CREATE_INDEX_EVENTS_CREATED_AT)
        cursor.execute(CREATE_INDEX_TRACKABLES_PLUGIN)
        conn.commit()

import importlib

def run_plugin_migrations(plugin_name: str, action: str):
    """
    Run 'create_tables' or 'drop_tables' for a plugin.
    action: 'create' or 'drop'
    """
    try:
        migrations = importlib.import_module(f"plugins.{plugin_name}.migrations")
    except ModuleNotFoundError:
        raise Exception(f"No migrations found for plugin '{plugin_name}'")
    with get_db() as conn:
        if action == "create":
            migrations.create_tables(conn)
        elif action == "drop":
            migrations.drop_tables(conn)
        else:
            raise ValueError("action must be 'create' or 'drop'")
            