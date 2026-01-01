#!/usr/bin/env python3
"""Debug script to trace the add_task method execution."""

import os
os.environ['TESTING_ALLOW_PAST_DATES'] = '1'

from src.services.task_storage import initialize_storage, tasks, recurrence_templates
from src.services.task_service import TaskService
from src.services.recurrence_service import RecurrenceService

print("=== Debugging task creation process ===")
print(f"Initial tasks: {len(tasks)}")
print(f"Initial recurrence_templates: {len(recurrence_templates)}")

# Initialize
initialize_storage()
print(f"After initialize - tasks: {len(tasks)}")
print(f"After initialize - recurrence_templates: {len(recurrence_templates)}")

# Create service
task_service = TaskService()
print(f"After TaskService init - tasks: {len(tasks)}")
print(f"After TaskService init - recurrence_templates: {len(recurrence_templates)}")

# Create pattern
pattern = RecurrenceService.create_recurrence_pattern("daily")
print(f"Pattern created: {pattern}")

# Add task with recurrence
print("About to call add_task with recurrence pattern...")
recurring_task = task_service.add_task(
    title="Daily task",
    recurrence_pattern=pattern
)
print(f"Task added - ID: {recurring_task.id}")
print(f"Task is_recurring_template: {recurring_task.is_recurring_template}")
print(f"Tasks after adding recurring task: {len(tasks)}")
print(f"Recurrence templates after adding recurring task: {len(recurrence_templates)}")
print(f"Recurrence templates keys: {list(recurrence_templates.keys())}")

# Check if the task is in both places
print(f"Task {recurring_task.id} in tasks: {recurring_task.id in tasks}")
print(f"Task {recurring_task.id} in recurrence_templates: {str(recurring_task.id) in recurrence_templates}")

# Add non-recurring task for comparison
non_recurring_task = task_service.add_task(title="One-time task")
print(f"Non-recurring task - ID: {non_recurring_task.id}")
print(f"Non-recurring task is_recurring_template: {non_recurring_task.is_recurring_template}")
print(f"Total tasks: {len(tasks)}")
print(f"Total recurrence templates: {len(recurrence_templates)}")