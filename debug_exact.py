#!/usr/bin/env python3
"""Debug script with exact same import sequence as failing test."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

# This is the exact sequence from the failing debug_test.py:
from src.services.task_storage import initialize_storage
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService

# Initialize
initialize_storage()
task_service = TaskService()

# Create and add task
pattern = RecurrenceService.create_recurrence_pattern("daily")
recurring_task = task_service.add_task(
    title="Daily task",
    recurrence_pattern=pattern
)

# Import recurrence_templates AFTER the task operations (like in the failing test)
from src.services.task_storage import recurrence_templates
print(f'Length of recurrence_templates: {len(recurrence_templates)}')
print(f'Task ID: {recurring_task.id}')
print(f'Is recurring template: {recurring_task.is_recurring_template}')

if len(recurrence_templates) == 1:
    print("SUCCESS: Test would pass")
else:
    print("FAILURE: Test would fail")