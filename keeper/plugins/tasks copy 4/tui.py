"""
Task plugin TUI commands for Keeper.
Provides: add-task, show-tasks
"""
import typer
from rich import print
from keeper.api import trackables

app = typer.Typer()

@app.command("add-task")
def add_task():
    """Add a new task (trackable of type 'task')."""
    name = input("Task name: ").strip()
    description = input("Description (optional): ").strip()
    color = input("Color (optional): ").strip()
    points = input("Points (default 1): ").strip()
    points = int(points) if points else 1
    trackables.create_trackable(
        type_="task",
        plugin_owner="core.tasks",
        name=name,
        description=description or None,
        color=color or None,
        points=points,
        config_json=None
    )
    print("[green]Task added![/green]")

@app.command("show-tasks")
def show_all_tasks():
    """Show all tasks (trackables of type 'task')."""
    tasks = trackables.list_trackables(type_="task")
    if not tasks:
        print("[yellow]No tasks found.[/yellow]")
        return
    print("\n[bold]All Tasks:[/bold]")
    for t in tasks:
        print(f"- {t['name']} (id: {t['id']}, points: {t['points']})")
