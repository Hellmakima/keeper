"""
Plugin container widget for Keeper TUI
"""
from textual.widgets import Static


class PluginContainer(Static):
    """Container for the currently active plugin's entire UI"""

    def __init__(self):
        super().__init__()
        self.current_plugin_widgets = []

    def set_plugin_ui(self, plugin_widgets):
        """Replace current plugin UI with new plugin's widgets"""
        # Remove old plugin widgets
        for widget in self.current_plugin_widgets:
            widget.remove()
        self.current_plugin_widgets = []
        
        # Mount new plugin widgets
        if isinstance(plugin_widgets, list):
            for widget in plugin_widgets:
                self.mount(widget)
                self.current_plugin_widgets.append(widget)
        else:
            self.mount(plugin_widgets)
            self.current_plugin_widgets.append(plugin_widgets)
