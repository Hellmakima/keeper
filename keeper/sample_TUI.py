
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from textual.binding import Binding
from textual.reactive import reactive


class Sidebar(Static):
    can_focus = True

    def compose(self) -> ComposeResult:
        yield Static(
            "[1] Tasks\n"
            "[2] Calendar\n"
            "[3] Lists\n"
            "[4] Mood\n"
            "[5] Metrics",
        )

class TopBar(Static):
    def compose(self) -> ComposeResult:
        yield Static(
            "[m] Month      [n] New task               [e] Edit\n"
            "[w] Week       <space> Toggle mark done   [D] Delete\n"
            "[d] Day\n"
            "────────────────────────────────────────────"
        )


class BottomBar(Static):
    def compose(self) -> ComposeResult:
        yield Static("(q) quit (/) find (?) keybindings")
    
class MainView(Static):
    can_focus = True
    cursor = reactive(0)

    def on_mount(self):
        self.tasks = [
            ("Buy groceries",False),
            ("Finish report", True),
            ("Call Alice", False),
            ("Workout", False),
            ("Read 20 pages", False),
            ("Clean desk", False),
            ("Study Python", False),
        ]
        self.has_focus = False
        self.watch_cursor()

    def on_key(self, event):
        if event.key == "enter":
            self.toggle_done()
        elif event.key == " ":
            self.toggle_done()
        elif event.key == "q":
            self.app.exit()
        self.render_tasks()
    
    def toggle_done(self):
        self.tasks[self.cursor] = (self.tasks[self.cursor][0], not self.tasks[self.cursor][1])
        self.render_tasks()

    def render_tasks(self):
        rendered = []
        for i, task in enumerate(self.tasks):
            if i == self.cursor and self.has_focus:
                # emojis
                rendered.append(f"> {'x' if task[1] else ' '} {task[0]}")
            else:
                rendered.append(f"  {'x' if task[1] else ' '} {task[0]}")
        self.update("\n".join(rendered))

    def watch_cursor(self):
        self.render_tasks()

    def on_focus(self):
        self.render_tasks()

    def on_blur(self):
        self.render_tasks()

    # j/k movement
    def move_down(self):
        if self.cursor < len(self.tasks) - 1:
            self.cursor += 1

    def move_up(self):
        if self.cursor > 0:
            self.cursor -= 1


class KeeperApp(App):

    CSS = """
        Screen {
            layout: horizontal;
        }

        Sidebar {
            width: 24;
            border: solid #444;
            height: 100%;
        }

        #right {
            layout: vertical;
            width: 1fr;
        }

        TopBar {
            height: 4;
            border: solid #444;
        }

        MainView {
            height: 1fr;
            border: solid #444;
        }

        BottomBar {
            height: 2;
            border: solid #444;
        }

        Sidebar:focus, MainView:focus {
            border: heavy white;
        }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("tab", "focus_next", "Next Panel"),
        Binding("h", "left"),
        Binding("j", "down"),
        Binding("k", "up"),
        Binding("l", "right"),
        Binding("space", "toggle_done", "Toggle Done"),
    ]

    def compose(self) -> ComposeResult:
        yield Sidebar()
        with Vertical(id="right"):
            yield TopBar()
            yield MainView()
            yield BottomBar()

    def on_mount(self):
        self.set_focus(self.query_one(MainView))

    # Vim-style navigation
    def action_down(self):
        focused = self.focused
        if isinstance(focused, MainView):
            focused.move_down()

    def action_up(self):
        focused = self.focused
        if isinstance(focused, MainView):
            focused.move_up()

    def action_focus_next(self):
        self.focus_next()
    
    def focus_next(self):
        focused = self.focused
        if isinstance(focused, MainView):
            self.set_focus(self.query_one(Sidebar))
        elif isinstance(focused, Sidebar):
            self.set_focus(self.query_one(TopBar))
        elif isinstance(focused, TopBar):
            self.set_focus(self.query_one(BottomBar))
        elif isinstance(focused, BottomBar):
            self.set_focus(self.query_one(MainView))


if __name__ == "__main__":
    KeeperApp().run()
