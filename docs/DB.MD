# Database Schema

## Trackables
Trackables are events that repeat and can be tracked.

```
Table Trackables
    id TEXT PRIMARY KEY, // uuid
    type TEXT NOT NULL, // "habit", "mood", "finance_goal", etc
    name TEXT NOT NULL, // name of the trackable (e.g., "Buy groceries")
    description TEXT,
    color TEXT, // #E7F8CC
    points INT DEFAULT 1,
    config_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived BOOLEAN DEFAULT FALSE,
```

## Trackable_events
History of events for a trackable.

```
Table Trackable_events
    id TEXT PRIMARY KEY, // uuid
    trackable_id TEXT NOT NULL,
    event_type ENUM("completed", "failed", "skipped", "edited"),
    value DECIMAL(10,2), // Money, Percentages, Amounts, Decimal tracking
    note TEXT,
    data_json JSON,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trackable_id) REFERENCES trackables(id)
```
