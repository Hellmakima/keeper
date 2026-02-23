# Keeper TUI - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hellmakima/keeper.git
cd keeper
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install textual typer
```

## Configuration

### Database Initialization

On first run, Keeper will automatically:
1. Create `~/.keeper/` directory
2. Initialize SQLite database at `~/.keeper/keeper.db`
3. Create necessary tables

No manual configuration required!

## Running Keeper

### Method 1: Using the run script

```bash
python run_keeper.py
```

### Method 2: Direct module execution

```bash
python -m keeper.keeper_TUI
```

### Method 3: After installation

```bash
keeper
```

## Testing

Run the test suite to verify installation:

```bash
python test_keeper.py
```

Expected output:
```
============================================================
KEEPER TUI TEST SUITE
============================================================
🗄️  Testing Database...
   ✅ Found X tasks in database
🔌 Testing Plugins...
   ✅ Loaded 2 plugins
   ✅ Plugin: Tasks (shortcut: 1, X keybindings)
   ✅ Plugin: Calendar (shortcut: 2, X keybindings)
🔧 Testing API...
   ✅ Created test task with ID: X
   ✅ Added completion event with ID: X
🚀 Testing App Initialization...
   ✅ KeeperTUI class imported successfully
   ✅ App structure is valid
============================================================
TOTAL: 4/4 tests passed
🎉 All tests passed!
```

## Directory Structure

```
keeper/
├── api/              # Database API layer
│   └── trackables.py # CRUD operations for trackables
├── commands/         # CLI commands
│   └── commands.py   # Command implementations
├── config/           # Configuration handlers
│   └── auth_handler.py # Auth and DB initialization
├── db/               # Database layer
│   ├── db.py         # Database connection
│   └── schema.py     # Table schemas
├── plugins/          # Plugin modules
│   ├── calendar/     # Calendar plugin
│   │   └── ui.py     # Calendar UI
│   └── tasks/        # Tasks plugin
│       ├── ui.py     # Tasks UI
│       └── command.py # Task commands
├── ui/               # Core UI components
│   ├── base_plugin.py     # Plugin base class
│   ├── sidebar.py         # Sidebar navigation
│   ├── plugin_loader.py   # Plugin discovery
│   ├── plugin_container.py # Plugin container
│   ├── bottom_bar.py      # Bottom status bar
│   └── keybindings_screen.py # Help screen
├── utils/            # Utilities
│   ├── json_utils.py # JSON helpers
│   └── keeper_cron.py # Cron utilities
├── constants.py      # App constants
└── keeper_TUI.py     # Main application
```

## Database Schema

### Tables

**trackables**
- id (INTEGER PRIMARY KEY)
- type (TEXT) - e.g., "task", "habit", "goal"
- plugin_owner (TEXT) - Plugin that created it
- name (TEXT) - Display name
- description (TEXT, nullable)
- color (TEXT, nullable)
- points (INTEGER, default 1)
- config_json (TEXT, nullable) - Plugin-specific config
- created_at (TIMESTAMP)
- archived_at (TIMESTAMP, nullable)

**trackable_events**
- id (INTEGER PRIMARY KEY)
- trackable_id (INTEGER, foreign key)
- event_type (TEXT) - e.g., "completed", "uncompleted"
- value (REAL, nullable)
- note (TEXT, nullable)
- data_json (TEXT, nullable)
- created_at (TIMESTAMP)

## Troubleshooting

### Import Errors

If you get "ModuleNotFoundError: No module named 'keeper'":
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python run_keeper.py
```

### Database Locked

If you get "database is locked" error:
1. Close any other Keeper instances
2. Remove locks: `rm ~/.keeper/*.lock` (if exists)

### Textual Not Found

```bash
pip install textual
```

### VERSION Error in constants.py

This has been fixed in the latest version. The VERSION now uses a try-except block to handle missing package metadata.

## Development

### Installing in Development Mode

```bash
pip install -e .
```

This allows you to edit code and see changes immediately without reinstalling.

### Running Tests During Development

```bash
python test_keeper.py
```

### Adding a New Plugin

1. Create a new directory under `keeper/plugins/your_plugin/`
2. Create `ui.py` with a `PluginUI` class
3. Implement required methods: `get_name()`, `get_shortcut()`, `create_view()`, `get_keybindings()`
4. The plugin will be auto-discovered on next run

## Next Steps

- Read [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
- Read [CODE_SUMMARY.md](CODE_SUMMARY.md) for architecture overview
- Read [DEPLOYMENT_READY.md](DEPLOYMENT_READY.md) for deployment instructions
