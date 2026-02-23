#!/usr/bin/env python3
"""
Simple runner for Keeper TUI
"""
import sys
import os

# Add keeper module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keeper.keeper_TUI import KeeperTUI

if __name__ == "__main__":
    app = KeeperTUI()
    app.run()
