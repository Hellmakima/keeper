# SQLite schema for Keeper trackables and events

CREATE_TABLE_TRACKABLES = '''
CREATE TABLE IF NOT EXISTS trackables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    plugin_owner TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    color TEXT,
    points INTEGER DEFAULT 1,
    config_json TEXT,
    created_at DATETIME NOT NULL DEFAULT (datetime('now')),
    archived_at DATETIME
);
'''

CREATE_TABLE_TRACKABLE_EVENTS = '''
CREATE TABLE IF NOT EXISTS trackable_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trackable_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,
    value REAL,
    note TEXT,
    data_json TEXT,
    created_at DATETIME NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (trackable_id) REFERENCES trackables(id) ON DELETE CASCADE
);
'''

CREATE_INDEX_EVENTS_TRACKABLE = '''
CREATE INDEX IF NOT EXISTS idx_events_trackable ON trackable_events(trackable_id);
'''

CREATE_INDEX_EVENTS_CREATED_AT = '''
CREATE INDEX IF NOT EXISTS idx_events_created_at ON trackable_events(created_at);
'''

CREATE_INDEX_TRACKABLES_PLUGIN = '''
CREATE INDEX IF NOT EXISTS idx_trackables_plugin ON trackables(plugin_owner);
'''
