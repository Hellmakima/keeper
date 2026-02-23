"""
Tasks plugin UI for Keeper TUI
"""
from textual.widgets import Static, Input, Button
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from keeper.ui.base_plugin import BasePluginUI
from keeper.api import trackables


class AddTaskScreen(ModalScreen):
    """Modal screen for adding a new task"""
    
    def compose(self):
        yield Vertical(
            Static("Add New Task", id="title"),
            Input(placeholder="Task name", id="task_name"),
            Input(placeholder="Description (optional)", id="description"),
            Input(placeholder="Points (default 1)", id="points"),
            Horizontal(
                Button("Add", variant="primary", id="add"),
                Button("Cancel", variant="default", id="cancel"),
            ),
            id="add_task_dialog"
        )
    
    def on_button_pressed(self, event):
        if event.button.id == "add":
            task_name = self.query_one("#task_name", Input).value.strip()
            description = self.query_one("#description", Input).value.strip()
            points_str = self.query_one("#points", Input).value.strip()
            points = int(points_str) if points_str.isdigit() else 1
            
            if task_name:
                trackables.create_trackable(
                    type_="task",
                    plugin_owner="core.tasks",
                    name=task_name,
                    description=description or None,
                    points=points,
                )
                self.dismiss(True)
        else:
            self.dismiss(False)


class TasksView(Static):
    """Main view widget for tasks"""
    can_focus = True
    cursor = reactive(0)

    def on_mount(self):
        self.load_tasks()
        self.watch_cursor()

    def load_tasks(self):
        """Load tasks from database"""
        task_list = trackables.list_trackables(type_="task", archived=False)
        self.tasks = [(task['name'], False, task['id']) for task in task_list]
        if not self.tasks:
            self.tasks = [("No tasks yet. Press 'n' to add one.", False, None)]
        self.render_tasks()

    def on_key(self, event):
        if event.key == "n":
            self.add_new_task()
        elif event.key == "enter" or event.key == " ":
            self.toggle_done()
        elif event.key == "j":
            self.move_down()
        elif event.key == "k":
            self.move_up()
        self.render_tasks()
    
    def add_new_task(self):
        """Show modal to add a new task"""
        def handle_result(result):
            if result:
                self.load_tasks()
        self.app.push_screen(AddTaskScreen(), handle_result)
    
    def toggle_done(self):
        """Toggle task completion status"""
        if self.cursor < len(self.tasks) and self.tasks[self.cursor][2] is not None:
            task = self.tasks[self.cursor]
            # Add completion event
            trackables.add_trackable_event(
                trackable_id=task[2],
                event_type="completed" if not task[1] else "uncompleted",
                value=1.0 if not task[1] else 0.0
            )
            self.tasks[self.cursor] = (task[0], not task[1], task[2])
            self.render_tasks()

    def render_tasks(self):
        """Render task list to the view"""
        rendered = []
        for i, task in enumerate(self.tasks):
            prefix = "> " if i == self.cursor else "  "
            status = "[x]" if task[1] else "[ ]"
            rendered.append(f"{prefix}{status} {task[0]}")
        self.update("\n".join(rendered))

    def watch_cursor(self):
        self.render_tasks()

    def on_focus(self):
        self.render_tasks()

    def on_blur(self):
        self.render_tasks()

    def move_down(self):
        if self.cursor < len(self.tasks) - 1:
            self.cursor += 1
            self.render_tasks()

    def move_up(self):
        if self.cursor > 0:
            self.cursor -= 1
            self.render_tasks()


class PluginUI(BasePluginUI):
    """Plugin UI registration class for Tasks"""
    
    @staticmethod
    def get_name() -> str:
        return "Tasks"
    
    @staticmethod
    def get_shortcut() -> str:
        return "1"
    
    @staticmethod
    def create_view() -> Static:
        return TasksView()
