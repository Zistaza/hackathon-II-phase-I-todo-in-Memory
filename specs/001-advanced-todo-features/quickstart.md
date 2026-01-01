# Quickstart Guide: Advanced Todo Features

## Overview
This guide provides a quick introduction to the advanced features of the todo CLI application: recurring tasks and due date reminders.

## Prerequisites
- Python 3.13+
- UV package manager
- In-memory storage (no external dependencies)

## Installation
The advanced features are built into the existing todo CLI application. No additional installation required.

## Getting Started

### 1. Adding Tasks with Due Dates
```bash
# Add a task with a due date
todo add "Submit report" --due "2026-01-15"

# Add a task with a specific due date and time
todo add "Team meeting" --due "2026-01-10 14:30"

# Add a task with a reminder
todo add "Doctor appointment" --due "2026-01-08" --remind "2026-01-07 18:00"
```

### 2. Creating Recurring Tasks
```bash
# Add a daily recurring task
todo add "Morning exercise" --recur "daily"

# Add a weekly recurring task
todo add "Team sync" --recur "weekly" --recur-days "mon,wed,fri"

# Add a custom recurring task
todo add "Pay rent" --recur "every 30 days"
```

### 3. Viewing Tasks
```bash
# View all tasks with due dates and reminders
todo view

# View upcoming tasks sorted by due date
todo view --upcoming

# View only overdue tasks
todo view --overdue

# View only recurring tasks
todo view --recurring
```

### 4. Managing Recurring Tasks
```bash
# List all recurring tasks
todo recurring --list

# Cancel a recurring pattern
todo modify 123 --cancel-recur

# Update recurrence pattern
todo modify 123 --update-recur "every 2 days"
```

### 5. Managing Reminders
```bash
# List all active reminders
todo reminders --list

# List upcoming reminders
todo reminders --upcoming
```

## Common Use Cases

### Daily Routine
```bash
# Set up daily recurring tasks
todo add "Check emails" --recur "daily" --remind "09:00"
todo add "Review tasks" --recur "daily" --remind "17:00"
```

### Weekly Meetings
```bash
# Set up weekly recurring meetings
todo add "Team standup" --recur "weekly" --recur-days "mon,tue,wed,thu,fri" --due "09:30"
```

### Monthly Bills
```bash
# Set up monthly recurring tasks
todo add "Pay electricity bill" --recur "every 30 days" --due "2026-01-15"
```

## Date/Time Formats

### Due Dates
- `YYYY-MM-DD`: Date only (e.g., "2026-01-15")
- `YYYY-MM-DD HH:MM`: Date and time (e.g., "2026-01-15 14:30")
- `HH:MM`: Time only (assumes today's date, e.g., "09:00")

### Recurrence Patterns
- `daily`: Every day
- `weekly`: Every week
- `every N days`: Every N days (e.g., "every 3 days")
- `every N weeks`: Every N weeks (e.g., "every 2 weeks")

## Tips
1. Use `--upcoming` to see tasks in order of urgency
2. Recurring tasks continue to generate even after individual instances are completed
3. Reminders only trigger when the CLI application is active
4. All times use your system's local timezone