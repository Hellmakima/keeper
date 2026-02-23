"""
Authentication handler for local session management.
Automatically handles local user provisioning.
"""
import os

from keeper.constants import APP_DIR, CONFIG_PATH
from keeper.db.db import init_database
from keeper.utils.json_utils import read_json, update_json, write_json


class AuthHandler:

    @classmethod
    def init(cls) -> None:
        """Initialize application directory, config, and database."""
        # Ensure application directory exists
        if not os.path.isdir(APP_DIR):
            os.makedirs(APP_DIR)

        # Ensure config.json exists
        if not os.path.exists(CONFIG_PATH):
            write_json(CONFIG_PATH, {})

        # Initialize database schema
        init_database()

    @classmethod
    def is_logged_in(cls) -> bool:
        """Always returns True for local offline mode."""
        return True

    @classmethod
    def get_user_id(cls) -> int:
        """Get the current local user's ID."""
        # Ensure we are initialized
        if not os.path.exists(CONFIG_PATH):
            cls.init()
            
        cfg = read_json(CONFIG_PATH)
        if "user_id" not in cfg:
            cls.init() # Retry init
            cfg = read_json(CONFIG_PATH)
            
        return cfg["user_id"]

    # Keep get_access_token as alias for compatibility
    @classmethod
    def get_access_token(cls) -> int:
        """Alias for get_user_id for backward compatibility."""
        return cls.get_user_id()
