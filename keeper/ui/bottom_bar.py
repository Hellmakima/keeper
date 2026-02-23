"""
Bottom bar widget for Keeper TUI
"""
from textual.widgets import Static
from textual.app import ComposeResult


from textual.widgets import Label

class BottomBar(Label):
    """Bottom bar with general keybindings"""
    DEFAULT_CSS = """
    BottomBar {
        min-height: 1;
        border: solid #444;
        width: 100%;
        text-align: right;
    }
    """

    def on_mount(self):
        self.update("(q) quit  (tab) switch panel  (j/k) navigate  (?) keybindings")
