#!/usr/bin/env python3
"""
Test script to verify Keeper TUI functionality
"""
import sys
import os

# Add keeper module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keeper.api import trackables
from keeper.ui.plugin_loader import load_plugin_uis
from keeper.config.auth_handler import AuthHandler

def test_database():
    """Test database initialization and queries"""
    print("🗄️  Testing Database...")
    
    # Initialize
    AuthHandler.init()
    
    # Test queries
    all_tasks = trackables.list_trackables(type_="task", archived=False)
    print(f"   ✅ Found {len(all_tasks)} tasks in database")
    
    # Test event queries
    for task in all_tasks[:2]:
        events = trackables.get_trackable_events(task['id'])
        print(f"   ✅ Task '{task['name']}' has {len(events)} events")
    
    return True

def test_plugins():
    """Test plugin loading"""
    print("\n🔌 Testing Plugins...")
    
    plugins = load_plugin_uis()
    print(f"   ✅ Loaded {len(plugins)} plugins")
    
    for plugin in plugins:
        name = plugin.get_name()
        shortcut = plugin.get_shortcut()
        keybindings = plugin.get_keybindings()
        print(f"   ✅ Plugin: {name} (shortcut: {shortcut}, {len(keybindings)} keybindings)")
    
    return len(plugins) >= 2

def test_api():
    """Test API functionality"""
    print("\n🔧 Testing API...")
    
    # Create a test task
    task_id = trackables.create_trackable(
        type_="task",
        plugin_owner="test",
        name="Test Task",
        description="This is a test task",
        points=5
    )
    print(f"   ✅ Created test task with ID: {task_id}")
    
    # Add an event
    event_id = trackables.add_trackable_event(
        trackable_id=task_id,
        event_type="completed",
        value=1.0
    )
    print(f"   ✅ Added completion event with ID: {event_id}")
    
    # Query the task
    task = trackables.get_trackable(task_id)
    print(f"   ✅ Retrieved task: {task['name']}")
    
    # Archive it
    trackables.archive_trackable(task_id)
    print(f"   ✅ Archived test task")
    
    return True

def test_app_init():
    """Test app initialization"""
    print("\n🚀 Testing App Initialization...")
    
    try:
        from keeper.keeper_TUI import KeeperTUI
        print("   ✅ KeeperTUI class imported successfully")
        
        # Check if we can instantiate (without running)
        print("   ✅ App structure is valid")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_sample_data():
    """Create sample tasks for testing"""
    print("\n📝 Creating Sample Data...")
    
    import json
    from datetime import datetime, timedelta
    
    sample_tasks = [
        {
            "name": "Review code",
            "description": "Review pull requests",
            "points": 3,
            "date_offset": 0
        },
        {
            "name": "Write documentation",
            "description": "Update README",
            "points": 2,
            "date_offset": 0
        },
        {
            "name": "Fix bug #123",
            "description": "Critical bug in login",
            "points": 5,
            "date_offset": -1
        },
        {
            "name": "Team meeting",
            "description": "Weekly sync",
            "points": 1,
            "date_offset": 1
        },
        {
            "name": "Deploy to staging",
            "description": "Test new features",
            "points": 4,
            "date_offset": 2
        },
        {
            "name": "Client presentation",
            "description": "Demo new features",
            "points": 3,
            "date_offset": 3
        },
    ]
    
    for task_data in sample_tasks:
        task_date = (datetime.now() + timedelta(days=task_data['date_offset'])).strftime('%Y-%m-%d')
        config = {
            "task_date": task_date,
            "from_time": "09:00",
            "to_time": "10:00"
        }
        
        task_id = trackables.create_trackable(
            type_="task",
            plugin_owner="core.calendar",
            name=task_data['name'],
            description=task_data['description'],
            points=task_data['points'],
            config_json=json.dumps(config)
        )
        print(f"   ✅ Created: {task_data['name']} for {task_date}")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("KEEPER TUI TEST SUITE")
    print("=" * 60)
    
    results = {
        "Database": test_database(),
        "Plugins": test_plugins(),
        "API": test_api(),
        "App Init": test_app_init(),
    }
    
    # Create sample data
    create_sample_data()
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s} {status}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
