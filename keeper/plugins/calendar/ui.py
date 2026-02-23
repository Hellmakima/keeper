"""
Calendar plugin UI for Keeper TUI
Main interface showing tasks, points, and streaks
"""
from datetime import datetime, timedelta
from textual.widgets import Static, Input, Button
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal, Grid
from keeper.ui.base_plugin import BasePluginUI
from keeper.api import trackables
import calendar


class AddTaskFromCalendarScreen(ModalScreen):
    """Modal screen for adding a new task from calendar view"""
    
    CSS = """
        #add_task_dialog {
            background: $surface;
            border: thick $primary;
            width: 60;
            height: 20;
            padding: 1;
        }
        #title {
            text-align: center;
            text-style: bold;
        }
        Button {
            margin: 1;
        }
    """
    
    def __init__(self, selected_date=None):
        super().__init__()
        self.selected_date = selected_date or datetime.now()
    
    def compose(self):
        yield Vertical(
            Static(f"Add Task for {self.selected_date.strftime('%Y-%m-%d')}", id="title"),
            Input(placeholder="Task name", id="task_name"),
            Input(placeholder="Description (optional)", id="description"),
            Input(placeholder="From time (HH:MM, default current+1h)", id="from_time"),
            Input(placeholder="To time (HH:MM, default from+1h)", id="to_time"),
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
            from_time = self.query_one("#from_time", Input).value.strip()
            to_time = self.query_one("#to_time", Input).value.strip()
            points_str = self.query_one("#points", Input).value.strip()
            points = int(points_str) if points_str.isdigit() else 1
            
            if task_name:
                # Store time information in config_json
                import json
                config = {
                    "from_time": from_time or None,
                    "to_time": to_time or None,
                    "task_date": self.selected_date.strftime('%Y-%m-%d')
                }
                
                trackables.create_trackable(
                    type_="task",
                    plugin_owner="core.calendar",
                    name=task_name,
                    description=description or None,
                    points=points,
                    config_json=json.dumps(config)
                )
                self.dismiss(True)
        else:
            self.dismiss(False)


class CalendarTopBar(Static):
    """Top bar with calendar-specific keybindings and view mode"""
    
    DEFAULT_CSS = """
        CalendarTopBar {
            height: 4;
            border: solid #444;
            padding: 0 1;
        }
    """
    
    def __init__(self, view_mode="month"):
        super().__init__()
        self.view_mode = view_mode
    
    def on_mount(self):
        self.update_display()
    
    def update_display(self):
        """Update the display based on current view mode"""
        if self.view_mode == "month":
            self.update(
                "[h/l] Prev/Next month  [j/k] Move  [n] New task\n"
                "[space] Toggle done    [m] Month   [w] Week   [d] Day\n"
                "────────────────────────────────────────────────────────"
            )
        elif self.view_mode == "week":
            self.update(
                "[h/l] Prev/Next week   [j/k] Move  [n] New task\n"
                "[space] Toggle done    [m] Month   [w] Week   [d] Day\n"
                "────────────────────────────────────────────────────────"
            )
        else:  # day
            self.update(
                "[h/l] Prev/Next day    [j/k] Move  [n] New task\n"
                "[space] Toggle done    [m] Month   [w] Week   [d] Day\n"
                "────────────────────────────────────────────────────────"
            )


class CalendarView(Static):
    """Main calendar view widget"""
    can_focus = True
    current_date = reactive(datetime.now())
    cursor = reactive(0)
    view_mode = reactive("month")  # "month", "week", or "day"
    
    DEFAULT_CSS = """
        CalendarView {
            height: 1fr;
            border: solid #444;
            padding: 1;
        }
        CalendarView:focus {
            border: heavy white;
        }
    """
    
    def __init__(self):
        super().__init__()
        self.tasks_by_date = {}
        self.selected_date = datetime.now()
        self.top_bar = None
    
    def on_mount(self):
        self.load_tasks()
        self.render_calendar()
    
    def load_tasks(self):
        """Load all tasks and organize by date"""
        import json
        task_list = trackables.list_trackables(type_="task", archived=False)
        self.tasks_by_date = {}
        
        for task in task_list:
            # Get task date from config_json
            task_date = None
            if task.get('config_json'):
                try:
                    config = json.loads(task['config_json'])
                    task_date = config.get('task_date')
                except:
                    pass
            
            # If no date in config, use created_at
            if not task_date and task.get('created_at'):
                task_date = task['created_at'][:10]  # Get YYYY-MM-DD
            
            if task_date:
                if task_date not in self.tasks_by_date:
                    self.tasks_by_date[task_date] = []
                
                # Check if task is completed
                events = trackables.get_trackable_events(task['id'])
                completed = False
                for event in reversed(events):
                    if event['event_type'] in ['completed', 'uncompleted']:
                        completed = (event['event_type'] == 'completed')
                        break
                
                self.tasks_by_date[task_date].append({
                    'id': task['id'],
                    'name': task['name'],
                    'points': task.get('points', 1),
                    'completed': completed,
                    'description': task.get('description', ''),
                })
    
    def on_key(self, event):
        """Handle keyboard navigation"""
        if event.key == "h":
            self.navigate_prev()
        elif event.key == "l":
            self.navigate_next()
        elif event.key == "j":
            self.move_down()
        elif event.key == "k":
            self.move_up()
        elif event.key == "n":
            self.add_new_task()
        elif event.key == "m":
            self.view_mode = "month"
            self.cursor = 0
            if self.top_bar:
                self.top_bar.view_mode = "month"
                self.top_bar.update_display()
            self.render_calendar()
        elif event.key == "w":
            self.view_mode = "week"
            self.cursor = 0
            if self.top_bar:
                self.top_bar.view_mode = "week"
                self.top_bar.update_display()
            self.render_calendar()
        elif event.key == "d":
            self.view_mode = "day"
            self.cursor = 0
            if self.top_bar:
                self.top_bar.view_mode = "day"
                self.top_bar.update_display()
            self.render_calendar()
        elif event.key == " " or event.key == "enter":
            self.toggle_task_done()
    
    def navigate_prev(self):
        """Navigate to previous period (month/week/day)"""
        if self.view_mode == "month":
            self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        elif self.view_mode == "week":
            self.current_date -= timedelta(days=7)
        else:  # day
            self.current_date -= timedelta(days=1)
        self.cursor = 0
        self.render_calendar()
    
    def navigate_next(self):
        """Navigate to next period (month/week/day)"""
        if self.view_mode == "month":
            next_month = self.current_date.replace(day=28) + timedelta(days=4)
            self.current_date = next_month.replace(day=1)
        elif self.view_mode == "week":
            self.current_date += timedelta(days=7)
        else:  # day
            self.current_date += timedelta(days=1)
        self.cursor = 0
        self.render_calendar()
    
    def move_down(self):
        """Move cursor down"""
        if self.view_mode == "month":
            # Move down one week
            self.current_date += timedelta(days=7)
        elif self.view_mode == "week":
            # In week view, move to next day
            self.current_date += timedelta(days=1)
        else:  # day view
            # In day view, move to next task
            date_str = self.current_date.strftime('%Y-%m-%d')
            tasks = self.tasks_by_date.get(date_str, [])
            if tasks and self.cursor < len(tasks) - 1:
                self.cursor += 1
        self.render_calendar()
    
    def move_up(self):
        """Move cursor up"""
        if self.view_mode == "month":
            # Move up one week
            self.current_date -= timedelta(days=7)
        elif self.view_mode == "week":
            # In week view, move to previous day
            self.current_date -= timedelta(days=1)
        else:  # day view
            # In day view, move to previous task
            if self.cursor > 0:
                self.cursor -= 1
        self.render_calendar()
    
    def add_new_task(self):
        """Show modal to add a new task for selected date"""
        def handle_result(result):
            if result:
                self.load_tasks()
                self.render_calendar()
        
        # Use current_date as the selected date
        self.app.push_screen(AddTaskFromCalendarScreen(self.current_date), handle_result)
    
    def toggle_task_done(self):
        """Toggle completion status of selected task"""
        if self.view_mode != "day":
            return
        
        date_str = self.current_date.strftime('%Y-%m-%d')
        tasks = self.tasks_by_date.get(date_str, [])
        
        if tasks and self.cursor < len(tasks):
            task = tasks[self.cursor]
            # Add completion event
            trackables.add_trackable_event(
                trackable_id=task['id'],
                event_type="completed" if not task['completed'] else "uncompleted",
                value=1.0 if not task['completed'] else 0.0
            )
            # Reload and re-render
            self.load_tasks()
            self.render_calendar()
    
    def render_calendar(self):
        """Render the calendar based on current view mode"""
        if self.view_mode == "month":
            self.render_month_view()
        elif self.view_mode == "week":
            self.render_week_view()
        else:
            self.render_day_view()
    
    def render_month_view(self):
        """Render month calendar view"""
        year = self.current_date.year
        month = self.current_date.month
        
        # Calendar header
        month_name = calendar.month_name[month]
        header = f"{month_name} {year}".center(40)
        
        lines = [header, "=" * 40, ""]
        
        # Weekday headers
        lines.append("  Su  Mo  Tu  We  Th  Fr  Sa")
        lines.append("")
        
        # Get calendar data
        cal = calendar.monthcalendar(year, month)
        today = datetime.now().date()
        selected_day = self.current_date.day
        
        # Render each week
        for week in cal:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "    "
                else:
                    date_obj = datetime(year, month, day).date()
                    date_str = date_obj.strftime('%Y-%m-%d')
                    
                    # Check if there are tasks on this day
                    has_tasks = date_str in self.tasks_by_date
                    
                    # Determine styling
                    if date_obj == today:
                        # Today - yellow background
                        day_str = f"{day:2d}"
                        if has_tasks:
                            week_str += f"[yellow][{day_str}●][/]"
                        else:
                            week_str += f"[yellow][{day_str}][/] "
                    elif day == selected_day:
                        # Selected day - white/highlighted
                        day_str = f"{day:2d}"
                        if has_tasks:
                            week_str += f"[white bold]>{day_str}●[/]"
                        else:
                            week_str += f"[white bold]>{day_str}[/] "
                    else:
                        # Normal day
                        day_str = f"{day:2d}"
                        if has_tasks:
                            week_str += f" {day_str}[green]●[/]"
                        else:
                            week_str += f" {day_str} "
            lines.append(week_str)
        
        # Add summary stats
        lines.append("")
        lines.append("=" * 40)
        
        # Calculate monthly stats
        month_start = datetime(year, month, 1).strftime('%Y-%m-%d')
        if month == 12:
            month_end = datetime(year + 1, 1, 1).strftime('%Y-%m-%d')
        else:
            month_end = datetime(year, month + 1, 1).strftime('%Y-%m-%d')
        
        total_points = 0
        completed_points = 0
        total_tasks = 0
        completed_tasks = 0
        
        for date_str, tasks in self.tasks_by_date.items():
            if month_start <= date_str < month_end:
                for task in tasks:
                    total_tasks += 1
                    total_points += task['points']
                    if task['completed']:
                        completed_tasks += 1
                        completed_points += task['points']
        
        lines.append(f"Monthly Stats:")
        lines.append(f"  Tasks: {completed_tasks}/{total_tasks} completed")
        lines.append(f"  Points: {completed_points}/{total_points}")
        if total_points > 0:
            progress = int((completed_points / total_points) * 20)
            bar = "█" * progress + "░" * (20 - progress)
            percentage = int((completed_points / total_points) * 100)
            lines.append(f"  [{bar}] {percentage}%")
        
        lines.append("")
        lines.append("[green]●[/] = Has tasks | [yellow]Yellow[/] = Today | > = Selected")
        
        self.update("\n".join(lines))
    
    def render_week_view(self):
        """Render week calendar view"""
        # Get start of week (Sunday)
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday() + 1)
        if self.current_date.weekday() == 6:  # Sunday
            start_of_week = self.current_date
        
        lines = []
        lines.append(f"Week of {start_of_week.strftime('%B %d, %Y')}".center(60))
        lines.append("=" * 60)
        lines.append("")
        
        today = datetime.now().date()
        
        # Render each day of the week
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            date_str = day.strftime('%Y-%m-%d')
            day_name = day.strftime('%A')
            
            # Check if this is the selected day
            is_selected = day.date() == self.current_date.date()
            is_today = day.date() == today
            
            # Get tasks for this day
            tasks = self.tasks_by_date.get(date_str, [])
            
            # Format day header
            if is_today:
                day_header = f"[yellow]{day_name} {day.strftime('%m/%d')}[/]"
            elif is_selected:
                day_header = f"[white bold]> {day_name} {day.strftime('%m/%d')}[/]"
            else:
                day_header = f"{day_name} {day.strftime('%m/%d')}"
            
            lines.append(day_header)
            
            if tasks:
                for task in tasks:
                    status = "[x]" if task['completed'] else "[ ]"
                    lines.append(f"  {status} {task['name']} ({task['points']} pts)")
            else:
                lines.append("  No tasks")
            
            lines.append("")
        
        # Weekly stats
        week_start = start_of_week.strftime('%Y-%m-%d')
        week_end = (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d')
        
        total_points = 0
        completed_points = 0
        total_tasks = 0
        completed_tasks = 0
        
        for date_str, tasks in self.tasks_by_date.items():
            if week_start <= date_str < week_end:
                for task in tasks:
                    total_tasks += 1
                    total_points += task['points']
                    if task['completed']:
                        completed_tasks += 1
                        completed_points += task['points']
        
        lines.append("=" * 60)
        lines.append(f"Weekly Stats:")
        lines.append(f"  Tasks: {completed_tasks}/{total_tasks} completed")
        lines.append(f"  Points: {completed_points}/{total_points}")
        if total_points > 0:
            progress = int((completed_points / total_points) * 20)
            bar = "█" * progress + "░" * (20 - progress)
            percentage = int((completed_points / total_points) * 100)
            lines.append(f"  [{bar}] {percentage}%")
        
        self.update("\n".join(lines))
    
    def render_day_view(self):
        """Render single day view with task details"""
        date_str = self.current_date.strftime('%Y-%m-%d')
        day_name = self.current_date.strftime('%A, %B %d, %Y')
        
        lines = []
        lines.append(day_name.center(60))
        lines.append("=" * 60)
        lines.append("")
        
        # Get tasks for this day
        tasks = self.tasks_by_date.get(date_str, [])
        
        if tasks:
            lines.append(f"Tasks for today: ({len(tasks)} total)")
            lines.append("")
            
            for i, task in enumerate(tasks):
                prefix = "> " if i == self.cursor else "  "
                status = "[x]" if task['completed'] else "[ ]"
                lines.append(f"{prefix}{status} {task['name']} ({task['points']} pts)")
                if task.get('description'):
                    lines.append(f"{prefix}   {task['description']}")
                lines.append("")
            
            # Daily stats
            total_points = sum(t['points'] for t in tasks)
            completed_points = sum(t['points'] for t in tasks if t['completed'])
            completed_tasks = sum(1 for t in tasks if t['completed'])
            
            lines.append("=" * 60)
            lines.append(f"Daily Stats:")
            lines.append(f"  Tasks: {completed_tasks}/{len(tasks)} completed")
            lines.append(f"  Points: {completed_points}/{total_points}")
            if total_points > 0:
                progress = int((completed_points / total_points) * 20)
                bar = "█" * progress + "░" * (20 - progress)
                percentage = int((completed_points / total_points) * 100)
                lines.append(f"  [{bar}] {percentage}%")
        else:
            lines.append("No tasks for this day.")
            lines.append("")
            lines.append("Press 'n' to add a new task.")
        
        self.update("\n".join(lines))


class PluginUI(BasePluginUI):
    """Plugin UI registration class for Calendar"""
    
    @staticmethod
    def get_name() -> str:
        return "Calendar"
    
    @staticmethod
    def get_shortcut() -> str:
        return "2"
    
    @staticmethod
    def create_view():
        """Return a list of widgets: [TopBar, MainView]"""
        top_bar = CalendarTopBar()
        view = CalendarView()
        # Connect them so view can update top bar
        view.top_bar = top_bar
        return [top_bar, view]
    
    @staticmethod
    def get_keybindings():
        """Return calendar-specific keybindings"""
        return {
            "h": "Previous period",
            "l": "Next period",
            "j": "Move down",
            "k": "Move up",
            "n": "New task",
            "m": "Month view",
            "w": "Week view",
            "d": "Day view",
            "space": "Toggle task completion",
        }
