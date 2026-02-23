import importlib
import os
from typer import Typer
from keeper.constants import PLUGINS_DIR
from rich import console


def import_commands_from_plugins(app: Typer):
    """
    Dynamically import all command modules from each plugin
    """
    # see if no plugins exist, if so, raise an error

    for plugin in os.listdir(PLUGINS_DIR):
        plugin_path = os.path.join(PLUGINS_DIR, plugin)
        command_file = os.path.join(plugin_path, "command.py")

        # Only load valid plugin folders
        if (
            os.path.isdir(plugin_path)
            and not plugin.startswith("__")
            and os.path.exists(command_file)
        ):
            module = importlib.import_module(
                f"keeper.plugins.{plugin}.command"
            )
            app.registered_commands.extend(module.app.registered_commands)
    if not app.registered_commands:
        console.Console().print(
            "[red]No plugins found! Please add at least one plugin to begin[/red]",
            "\nYou can find plugins in the [blue]keeper/plugins[/blue] directory or create your own by following the documentation.",
            )
            # TODO: Add command to add plugins
        exit(1)