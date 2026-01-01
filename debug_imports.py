#!/usr/bin/env python3
"""Debug script to check if same objects are referenced."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

from src.services.task_storage import initialize_storage, recurrence_templates as rt1
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService

# After importing TaskService, check if it affected the reference
from src.services.task_storage import recurrence_templates as rt2

print(f"ID of rt1: {id(rt1)}")
print(f"ID of rt2: {id(rt2)}")
print(f"Are they the same object? {rt1 is rt2}")

# Initialize and create task service
initialize_storage()
task_service = TaskService()

# Check again after creating TaskService
from src.services.task_storage import recurrence_templates as rt3
print(f"ID of rt3: {id(rt3)}")
print(f"Are rt2 and rt3 same? {rt2 is rt3}")

# Create a task
pattern = RecurrenceService.create_recurrence_pattern("daily")
task_service.add_task(title="Test task", recurrence_pattern=pattern)

print(f"Length of rt1: {len(rt1)}")
print(f"Length of rt2: {len(rt2)}")
print(f"Length of rt3: {len(rt3)}")