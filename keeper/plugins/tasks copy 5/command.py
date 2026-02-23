"""
Tasks plugin commands for Keeper.
"""
from . import tui

# Expose the Typer app for the plugin loader
app = tui.app
