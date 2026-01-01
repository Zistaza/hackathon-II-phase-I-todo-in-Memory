#!/usr/bin/env python3
"""Debug script to test import order."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

# Version 1: Import variables first, then TaskService
print("=== Test 1: Import variables first ===")
from src.services.task_storage import initialize_storage, recurrence_templates as rt1
print(f"rt1 ID: {id(rt1)}, length: {len(rt1)}")

from src.services.task_service import TaskService
print(f"After importing TaskService - rt1 length: {len(rt1)}")

task_service = TaskService()
from src.services.recurrence_service import RecurrenceService
pattern = RecurrenceService.create_recurrence_pattern("daily")
task_service.add_task(title="Test", recurrence_pattern=pattern)
print(f"After adding task - rt1 length: {len(rt1)}")

from src.services.task_storage import recurrence_templates as rt2
print(f"rt2 ID: {id(rt2)}, length: {len(rt2)}")
print(f"Same object: {rt1 is rt2}")

print("\n=== Test 2: Import TaskService first ===")
# Reset
initialize_storage()

from src.services.task_service import TaskService as TaskService2  # Use different name to avoid conflicts
from src.services.task_storage import initialize_storage as init2, recurrence_templates as rt3
print(f"rt3 ID: {id(rt3)}, length: {len(rt3)}")

ts = TaskService2()
from src.services.recurrence_service import RecurrenceService as RecurrenceService2
pattern2 = RecurrenceService2.create_recurrence_pattern("daily")
ts.add_task(title="Test", recurrence_pattern=pattern2)
print(f"After adding task - rt3 length: {len(rt3)}")

from src.services.task_storage import recurrence_templates as rt4
print(f"rt4 ID: {id(rt4)}, length: {len(rt4)}")
print(f"Same object: {rt3 is rt4}")