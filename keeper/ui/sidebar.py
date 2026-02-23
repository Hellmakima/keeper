"""
Sidebar widget for Keeper TUI
"""
from textual.widgets import Static
from textual.reactive import reactive


class Sidebar(Static):
    """Left sidebar showing available plugins"""
    can_focus = True
    selected_index = reactive(0)
    DEFAULT_CSS = """

        Sidebar {
            width: 24;
            border: solid #444;
            height: 100%;
        }
        Sidebar:focus {
            border: heavy white;
        }
    """

    def __init__(self, plugins):
        super().__init__()
        self.plugins = plugins

    def on_mount(self):
        self.render_sidebar()

    def render_sidebar(self):
        """Render plugin list in sidebar"""
        lines = [
            "[b]Keeper[/b]",
            "",
            "[i]Plugins[/i]",
            "",
        ]
        for i, plugin in enumerate(self.plugins):
            shortcut = plugin.get_shortcut() or str(i + 1) if i < 9 else ""
            name = plugin.get_name()
            prefix = ">" if i == self.selected_index else " "
            shortcut_text = f"[{shortcut}] " if shortcut else ""
            lines.append(f"{prefix}{shortcut_text}{name}")
        self.update("\n".join(lines))

    def watch_selected_index(self):
        self.render_sidebar()
    
    def on_key(self, event):
        """Handle vim-style navigation"""
        if event.key == "j":
            self.move_down()
        elif event.key == "k":
            self.move_up()
        elif event.key == "g":
            # Wait for second 'g' for gg (go to top)
            if hasattr(self, '_last_key') and self._last_key == "g":
                self.selected_index = 0
                self._last_key = None
            else:
                self._last_key = "g"
                return
        elif event.key == "G":
            # Go to bottom
            self.selected_index = len(self.plugins) - 1
        else:
            self._last_key = None
            return
        
        # Switch to the selected plugin immediately
        self.app.load_plugin(self.selected_index)
        self._last_key = event.key
    
    def move_down(self, count=1):
        """Move selection down by count (with wrapping)"""
        self.selected_index = (self.selected_index + count) % len(self.plugins)
    
    def move_up(self, count=1):
        """Move selection up by count (with wrapping)"""
        self.selected_index = (self.selected_index - count) % len(self.plugins)
