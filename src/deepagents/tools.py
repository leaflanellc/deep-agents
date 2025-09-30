"""
Legacy tools module for backward compatibility.

This module re-exports tools from the new tools module structure.
"""

# Import all tools from the new structure for backward compatibility
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tools.filesystem_tools import (
    write_todos,
    ls,
    read_file,
    write_file,
    edit_file,
)

# Re-export for backward compatibility
__all__ = [
    "write_todos",
    "ls",
    "read_file", 
    "write_file",
    "edit_file",
]
