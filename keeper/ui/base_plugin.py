"""
Base plugin UI interface for Keeper TUI
Each plugin should create a UI module that provides a PluginUI class
"""
from textual.widget import Widget
from typing import Optional, Union, List, Dict


class BasePluginUI:
    """Base class for plugin UI components"""
    
    @staticmethod
    def get_name() -> str:
        """Return the display name for the sidebar"""
        raise NotImplementedError("Plugin must implement get_name()")
    
    @staticmethod
    def get_shortcut() -> Optional[str]:
        """Return keyboard shortcut (e.g., '1', '2', etc.)"""
        return None
    
    @staticmethod
    def create_view() -> Union[Widget, List[Widget]]:
        """
        Create and return the UI widget(s) for this plugin.
        Can return:
        - A single Widget that fills the entire plugin area
        - A list of Widgets to compose multiple sections (e.g., topbar, mainview, etc.)
        """
        raise NotImplementedError("Plugin must implement create_view()")
    
    @staticmethod
    def get_keybindings() -> Dict[str, str]:
        """
        Return plugin-specific keybindings as a dict of {key: description}.
        Example: {"n": "New task", "e": "Edit task", "d": "Delete task"}
        """
        return {}
