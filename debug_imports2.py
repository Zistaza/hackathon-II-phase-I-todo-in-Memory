#!/usr/bin/env python3
"""Debug script to check when the object changes."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

from src.services.task_storage import initialize_storage, recurrence_templates as rt_before_import
print(f"Before importing TaskService - rt ID: {id(rt_before_import)}")

from src.services.task_service import TaskService
print(f"After importing TaskService - rt_same: {id(rt_before_import)}")

# Check if it's different by importing again
from src.services.task_storage import recurrence_templates as rt_after_import
print(f"After import TaskService - rt_after_import ID: {id(rt_after_import)}")
print(f"Same object? {rt_before_import is rt_after_import}")

# Now create instance
task_service = TaskService()
print(f"After creating TaskService instance - rt ID: {id(rt_before_import)}")

# Import again after creating instance
from src.services.task_storage import recurrence_templates as rt_after_instance
print(f"After creating TaskService instance - rt_after_instance ID: {id(rt_after_instance)}")
print(f"Same object? {rt_before_import is rt_after_instance}")