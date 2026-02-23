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
    
    CSS = """
        #add_task_dialog {
            background: $surface;
            border: thick $primary;
            width: 60;
            height: 15;
            padding: 1;
        }
        #title {
            text-align: center;
            text-style: bold;
        }
    """
    
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


class TasksTopBar(Static):
    """Top bar with task-specific keybindings"""
    
    DEFAULT_CSS = """
        TasksTopBar {
            height: 4;
            border: solid #444;
        }
    """
    
    def on_mount(self):
        self.update(
            "[n] New task               [e] Edit\n"
            "<space> Toggle mark done   [D] Delete\n"
            "────────────────────────────────────────────"
        )


class TasksView(Static):
    """Main view widget for tasks"""
    can_focus = True
    cursor = reactive(0)
    
    DEFAULT_CSS = """
        TasksView {
            height: 1fr;
            border: solid #444;
        }
        TasksView:focus {
            border: heavy white;
        }
    """

    def on_mount(self):
        self.load_tasks()
        self.watch_cursor()

    def load_tasks(self):
        """Load tasks from database"""
        task_list = trackables.list_trackables(type_="task", archived=False)
        self.tasks = []
        
        for task in task_list:
            # Check if task is completed
            events = trackables.get_trackable_events(task['id'])
            completed = False
            for event in reversed(events):
                if event['event_type'] in ['completed', 'uncompleted']:
                    completed = (event['event_type'] == 'completed')
                    break
            
            points = task.get('points', 1)
            self.tasks.append((task['name'], completed, task['id'], points))
        
        if not self.tasks:
            self.tasks = [("No tasks yet. Press 'n' to add one.", False, None, 0)]
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
        total_points = 0
        completed_points = 0
        
        for i, task in enumerate(self.tasks):
            prefix = "> " if i == self.cursor else "  "
            status = "[x]" if task[1] else "[ ]"
            points = task[3] if len(task) > 3 else 0
            
            if task[2] is not None:  # Real task (not placeholder)
                total_points += points
                if task[1]:  # completed
                    completed_points += points
                rendered.append(f"{prefix}{status} {task[0]} ({points} pts)")
            else:
                rendered.append(f"{prefix}{task[0]}")
        
        # Add progress stats if there are tasks
        if total_points > 0:
            rendered.append("")
            rendered.append("─" * 40)
            rendered.append(f"Progress: {completed_points}/{total_points} points")
            
            # Add progress bar
            progress = int((completed_points / total_points) * 20)
            bar = "█" * progress + "░" * (20 - progress)
            percentage = int((completed_points / total_points) * 100)
            rendered.append(f"[{bar}] {percentage}%")
        
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
    def create_view():
        """Return a list of widgets: [TopBar, MainView]"""
        return [TasksTopBar(), TasksView()]
    
    @staticmethod
    def get_keybindings():
        """Return task-specific keybindings"""
        return {
            "n": "New task",
            "e": "Edit task",
            "D": "Delete task",
            "j": "Move down",
            "k": "Move up",
            "space": "Toggle task completion",
        }
