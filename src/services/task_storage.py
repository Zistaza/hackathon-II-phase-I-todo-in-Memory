"""
In-memory storage structure for the advanced todo CLI application.

This module provides the global storage for tasks, recurrence templates,
reminders, and cached due tasks.
"""

from typing import Dict, List
from ..models.task import Task
from ..models.reminder import Reminder


# Main storage
tasks: Dict[str, Task] = {}  # All tasks by ID
recurrence_templates: Dict[str, Task] = {}  # Tasks with recurrence patterns
reminders: Dict[str, Reminder] = {}  # Active reminders by task ID
due_tasks_cache: List[Task] = []  # Cache of tasks sorted by due date

# Initialize with any required default values
def initialize_storage():
    """Initialize the in-memory storage with default values."""
    global tasks, recurrence_templates, reminders, due_tasks_cache
    tasks = {}
    recurrence_templates = {}
    reminders = {}
    due_tasks_cache = []