"""
Keybindings modal screen for Keeper TUI
"""
from textual.widgets import Static, Button
from textual.screen import ModalScreen
from textual.containers import Vertical


class KeybindingsScreen(ModalScreen):
    """Modal screen showing all keybindings"""
    
    CSS = """
        KeybindingsScreen {
            align: center middle;
        }
        
        #keybindings_dialog {
            background: $surface;
            border: thick $primary;
            width: 70;
            height: auto;
            max-height: 90%;
            padding: 1 2;
        }
        
        #title {
            text-align: center;
            text-style: bold;
            margin-bottom: 1;
        }
        
        #content {
            height: auto;
            overflow-y: auto;
        }
        
        .section-title {
            text-style: bold;
            color: $accent;
            margin-top: 1;
        }
    """
    
    def __init__(self, base_bindings: dict, plugin_name: str, plugin_bindings: dict):
        super().__init__()
        self.base_bindings = base_bindings
        self.plugin_name = plugin_name
        self.plugin_bindings = plugin_bindings
    
    def compose(self):
        lines = []
        
        # Base keybindings section
        lines.append("[b]Global Keybindings[/b]\n")
        for key, desc in self.base_bindings.items():
            lines.append(f"  {key:15} {desc}")
        
        # Plugin keybindings section
        if self.plugin_bindings:
            lines.append(f"\n[b]{self.plugin_name} Keybindings[/b]\n")
            for key, desc in self.plugin_bindings.items():
                lines.append(f"  {key:15} {desc}")
        
        yield Vertical(
            Static("Keybindings", id="title"),
            Static("\n".join(lines), id="content"),
            Button("Close", variant="primary", id="close"),
            id="keybindings_dialog"
        )
    
    def on_button_pressed(self, event):
        self.dismiss()
    
    def on_key(self, event):
        if event.key == "escape" or event.key == "q" or event.key == "question_mark":
            self.dismiss()
