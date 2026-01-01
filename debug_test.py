#!/usr/bin/env python3
"""Debug script to reproduce the failing test."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

from src.services.task_storage import initialize_storage
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService

# Simulate the exact test setup from TestCLIIntegration
initialize_storage()  # This simulates conftest.py fixture
task_service = TaskService()

# Reproduce the exact failing test
pattern = RecurrenceService.create_recurrence_pattern("daily")
recurring_task = task_service.add_task(
    title="Daily task",
    recurrence_pattern=pattern
)

# Create a non-recurring task
non_recurring_task = task_service.add_task(title="One-time task")

# Test that recurring tasks can be retrieved
from src.services.task_storage import recurrence_templates
print(f'Length of recurrence_templates: {len(recurrence_templates)}')
print(f'Expected: 1, Actual: {len(recurrence_templates)}')

if len(recurrence_templates) == 1:
    print("SUCCESS: Test would pass")
else:
    print("FAILURE: Test would fail")
    print(f"Recurrence templates: {list(recurrence_templates.keys())}")
    print(f"Task ID: {recurring_task.id}")
    print(f"Is recurring template: {recurring_task.is_recurring_template}")