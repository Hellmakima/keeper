"""
Plugin UI loader for Keeper TUI
Dynamically discovers and loads plugin UI components
"""
import importlib
import os
from typing import List, Type
from keeper.ui.base_plugin import BasePluginUI

# Get the actual plugins directory
PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")


def load_plugin_uis() -> List[Type[BasePluginUI]]:
    """
    Discover and load all plugin UIs from the plugins directory.
    Returns a list of PluginUI classes.
    """
    plugin_uis = []
    
    if not os.path.exists(PLUGINS_DIR):
        return plugin_uis
    
    for plugin in os.listdir(PLUGINS_DIR):
        plugin_path = os.path.join(PLUGINS_DIR, plugin)
        ui_file = os.path.join(plugin_path, "ui.py")
        
        # Only load valid plugin folders
        if (
            os.path.isdir(plugin_path)
            and not plugin.startswith("__")
            and os.path.exists(ui_file)
        ):
            try:
                module = importlib.import_module(f"keeper.plugins.{plugin}.ui")
                if hasattr(module, "PluginUI"):
                    plugin_uis.append(module.PluginUI)
            except Exception as e:
                print(f"Warning: Failed to load UI for plugin {plugin}: {e}")
    
    return plugin_uis
