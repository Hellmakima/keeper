"""
Keeper TUI - Main application
"""
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.binding import Binding

from keeper.config.auth_handler import AuthHandler
from keeper.ui.plugin_loader import load_plugin_uis
from keeper.ui.sidebar import Sidebar
from keeper.ui.bottom_bar import BottomBar
from keeper.ui.plugin_container import PluginContainer
from keeper.ui.keybindings_screen import KeybindingsScreen


class KeeperApp(App):
    """Main Keeper TUI application"""

    CSS = """
        Screen {
            layout: horizontal;
        }

        Sidebar {
            width: 24;
            border: solid #444;
            height: 100%;
        }
        
        Sidebar:focus {
            border: heavy white;
        }

        #main_area {
            layout: vertical;
            width: 1fr;
        }

        PluginContainer {
            layout: vertical;
            height: 1fr;
        }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("tab", "focus_next", "Next Panel", show=False),
        Binding("shift+tab", "focus_previous", "Prev Panel", show=False),
        Binding("question_mark", "show_keybindings", "Keybindings"),
    ]

    def __init__(self):
        super().__init__()
        self.plugins = load_plugin_uis()
        if not self.plugins:
            print("Error: No plugins found! Please add at least one plugin with UI.")
            exit(1)
        self.current_plugin_index = 0

    def compose(self) -> ComposeResult:
        yield Sidebar(self.plugins)
        with Vertical(id="main_area"):
            yield PluginContainer()
            yield BottomBar()

    def on_mount(self):
        # Initialize database
        AuthHandler.init()
        
        # Load first plugin
        self.load_plugin(0)
        
        # Set initial focus to sidebar
        self.set_focus(self.query_one(Sidebar))

    def load_plugin(self, index: int):
        """Load a plugin's UI by index"""
        if 0 <= index < len(self.plugins):
            self.current_plugin_index = index
            sidebar = self.query_one(Sidebar)
            sidebar.selected_index = index
            
            plugin_container = self.query_one(PluginContainer)
            plugin_ui = self.plugins[index].create_view()
            plugin_container.set_plugin_ui(plugin_ui)

    def action_switch_plugin(self, index: int):
        """Switch to a plugin by index"""
        self.load_plugin(index)

    def action_show_keybindings(self):
        """Show keybindings help"""
        # Base keybindings
        base_bindings = {
            "q": "Quit application",
            "?": "Show keybindings",
            "tab": "Switch to next panel",
            "shift+tab": "Switch to previous panel",
        }
        
        # Sidebar keybindings (when focused)
        base_bindings.update({
            "j": "Move down in sidebar",
            "k": "Move up in sidebar",
            "gg": "Jump to first plugin",
            "G": "Jump to last plugin",
        })
        
        # Get current plugin's keybindings
        plugin_name = self.plugins[self.current_plugin_index].get_name()
        plugin_bindings = self.plugins[self.current_plugin_index].get_keybindings()
        
        # Show modal
        self.push_screen(KeybindingsScreen(base_bindings, plugin_name, plugin_bindings))


if __name__ == "__main__":
    KeeperApp().run()
