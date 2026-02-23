"""
API for trackables and trackable_events
"""
from typing import Optional, List, Dict, Any
from keeper.db.db import get_db

# --- TRACKABLES ---
def create_trackable(type_: str, plugin_owner: str, name: str, description: Optional[str] = None, color: Optional[str] = None, points: int = 1, config_json: Optional[str] = None) -> int:
    """Create a new trackable and return its ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO trackables (type, plugin_owner, name, description, color, points, config_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """,
            (type_, plugin_owner, name, description, color, points, config_json)
        )
        return cursor.lastrowid

def get_trackable(trackable_id: int) -> Optional[dict]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trackables WHERE id = ?", (trackable_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def list_trackables(type_: Optional[str] = None, plugin_owner: Optional[str] = None, archived: Optional[bool] = None) -> List[dict]:
    query = "SELECT * FROM trackables WHERE 1=1"
    params = []
    if type_:
        query += " AND type = ?"
        params.append(type_)
    if plugin_owner:
        query += " AND plugin_owner = ?"
        params.append(plugin_owner)
    if archived is not None:
        if archived:
            query += " AND archived_at IS NOT NULL"
        else:
            query += " AND archived_at IS NULL"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def archive_trackable(trackable_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE trackables SET archived_at = datetime('now') WHERE id = ?", (trackable_id,))

# --- TRACKABLE EVENTS ---
def add_trackable_event(trackable_id: int, event_type: str, value: Optional[float] = None, note: Optional[str] = None, data_json: Optional[str] = None) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO trackable_events (trackable_id, event_type, value, note, data_json, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (trackable_id, event_type, value, note, data_json)
        )
        return cursor.lastrowid

def get_trackable_events(trackable_id: int, event_type: Optional[str] = None) -> List[dict]:
    query = "SELECT * FROM trackable_events WHERE trackable_id = ?"
    params = [trackable_id]
    if event_type:
        query += " AND event_type = ?"
        params.append(event_type)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

# Optionally, add more API functions as needed.
