Everything is a Plugins
each needs to add some UI, db, services
app/
  plugins/
  TUI_Engine/
  db/
  UI Composition/.   (layout, leftbar, topbar)
  Feature Registry/. (plugins register here)


# Tables
Tasks
  - task_id
  - name
  - description
  - from time
  - to time
  - points
  - color

Tasks_history
  - task_id
  - time

Habits
  - habit_id
  - name
  - description
  - type
  - goal_type ENUM (boolean/integer)
  - goal_amount
  - goal_unit
  - repeat columns not decided yet
  - expiry
  - points
  - color

Metrics
 No table needed, each plugin can export its own metrics
 this plugin will fetch all the metrics and show them in the UI
 IDK how to do this

Moods
  - mood_id
  - parent_id
  - name

Bad_habits
  - bad_habit_id
  - name
  - description
  - type
  - goal_type
  - goal_amount
  - goal_unit

```
Note
In python all trackables are from a common base class Trackable
History table is common for all trackables. Store trackable_id, time, and json data.
Each trackable has its own table
```

History
  - time
  - note
  - table_name
  - event_id (task_id, habit_id, mood_id)
  - data_json (amount, note, etc)

Streaks
No table needed, can be calculated from history

Brain_chemicals
  - habit_id
  - dopamine
  - oxytocin
  - serotonin
  - endorphin

---
CHATGPT

Perfect. Let’s define this cleanly and concretely for SQLite (ideal for Keeper), but I’ll keep types generic enough that you could move to Postgres later.

---

# 🧱 `trackables` Table

Represents **anything that can be tracked**
(tasks, habits, bad habits, finance goals, food entries, etc.)

---

### `id`

**Type:** `INTEGER PRIMARY KEY AUTOINCREMENT`
**Stores:** Unique identifier for the trackable
**Points to:** Referenced by `trackable_events.trackable_id`

---

### `type`

**Type:** `TEXT NOT NULL`
**Stores:** Logical type of the trackable

Examples:

* `"task"`
* `"habit"`
* `"bad_habit"`
* `"finance_goal"`
* `"food_entry"`
* `"plugin_defined"`

Used for:

* Filtering
* Rendering correct UI
* Metrics grouping

---

### `plugin_owner`

**Type:** `TEXT NOT NULL`
**Stores:** Which plugin created/owns this trackable

Examples:

* `"core.tasks"`
* `"core.habits"`
* `"plugin.finance"`
* `"plugin.mood"`

Used for:

* Clean uninstall
* Feature scoping
* Permissions

---

### `name`

**Type:** `TEXT NOT NULL`
**Stores:** Display name

Example:

* `"Go to gym"`
* `"Save $100"`
* `"No sugar"`

---

### `description`

**Type:** `TEXT` (nullable)
**Stores:** Longer explanation

Example:

* `"Upper body strength training"`
* `"For the winter hoodie"`

---

### `color`

**Type:** `TEXT`
**Stores:** UI color identifier

Examples:

* `"red"`
* `"#FF5733"`
* `"theme.primary"`

Used only for rendering.

---

### `points`

**Type:** `INTEGER DEFAULT 1`
**Stores:** Points awarded (or deducted) per completion

Examples:

* `5`
* `-3` (bad habit)

Used for:

* Gamification
* Streak scoring
* Leaderboards

---

### `config_json`

**Type:** `TEXT` (JSON string)
**Stores:** Configuration specific to this trackable

Examples:

Habit:

```json
{
  "repeat_rule": "RRULE:FREQ=DAILY",
  "expiry_hours": 12
}
```

Finance goal:

```json
{
  "monthly_limit": 500,
  "category": "food"
}
```

Food tracker:

```json
{
  "calorie_target": 2000
}
```

This avoids schema explosion.

---

### `created_at`

**Type:** `DATETIME NOT NULL` (store as ISO8601 TEXT in SQLite)
**Stores:** When the trackable was created

Example:

```
2026-02-14T15:22:00
```

---

### `archived_at`

**Type:** `DATETIME` (nullable)
**Stores:** Soft delete / archive time

If NULL → active
If NOT NULL → archived

Used for:

* Hiding from UI
* Preserving history

---

---

# 🧾 `trackable_events` Table

Represents **every action/log related to a trackable**

---

### `id`

**Type:** `INTEGER PRIMARY KEY AUTOINCREMENT`
**Stores:** Unique event ID

---

### `trackable_id`

**Type:** `INTEGER NOT NULL`
**Points to:** `trackables(id)`

**Constraint:**

```sql
FOREIGN KEY (trackable_id)
REFERENCES trackables(id)
ON DELETE CASCADE
```

Meaning:
If a trackable is deleted → its events auto-delete.

---

### `event_type`

**Type:** `TEXT NOT NULL`
**Stores:** What happened

Examples:

* `"completed"`
* `"failed"`
* `"skipped"`
* `"logged"`
* `"expired"`
* `"edited"`

This allows flexible logic.

---

### `value`

**Type:** `REAL` (nullable)

Why REAL instead of INTEGER?
Because:

* Money
* Percentages
* Amounts
* Decimal tracking

Examples:

* `1` (task completed)
* `3` (habit count)
* `-20.5` (spent money)
* `80` (score)

If boolean completion → value = 1

---

### `note`

**Type:** `TEXT` (nullable)

Stores user note for that event.

Example:

* `"Felt tired but still did it"`
* `"Stress from work"`

---

### `data_json`

**Type:** `TEXT` (JSON string)

Stores structured event-specific metadata.

Examples:

Mood entry:

```json
{
  "intensity": 4,
  "trigger": "work"
}
```

Finance entry:

```json
{
  "category": "food",
  "payment_method": "card"
}
```

Habit entry:

```json
{
  "unit": "pages"
}
```

This avoids creating new columns per plugin.

---

### `created_at`

**Type:** `DATETIME NOT NULL`

When the event occurred.

---

# 🔗 Relationship Summary

```
trackables (1)
     ↓
trackable_events (many)
```

Everything in Keeper becomes:

> A trackable
> Producing events

---

# 🧠 Why This Structure Is Powerful

You can now compute:

### Daily Points

```sql
SELECT SUM(value)
FROM trackable_events
JOIN trackables
ON trackables.id = trackable_events.trackable_id
WHERE event_type = 'completed'
AND date(created_at) = date('now');
```

### Current Streak

Count consecutive days with at least 1 completed event.

### Mood vs Productivity

Join mood trackables with other trackables via date.

---

# 📌 Optional Indexes (Important)

Add:

```sql
CREATE INDEX idx_events_trackable
ON trackable_events(trackable_id);

CREATE INDEX idx_events_created_at
ON trackable_events(created_at);

CREATE INDEX idx_trackables_plugin
ON trackables(plugin_owner);
```

This keeps metrics fast.

---

# 🎯 Clean Plugin Uninstall

Delete by owner:

```sql
DELETE FROM trackables
WHERE plugin_owner = 'plugin.finance';
```

Events auto-delete via cascade.

No schema mess.

---

# 🧠 Final Mental Model

In Keeper:

> Trackables define what can happen.
> Events define what did happen.

That’s it.

---

If you want next, we can:

* Design the exact SQL `CREATE TABLE` statements
* Design the Python `Trackable` base class
* Design how repeat rules should be implemented cleanly
* Design streak calculation efficiently
* Design how metrics plugins query this safely

What should we refine next?
