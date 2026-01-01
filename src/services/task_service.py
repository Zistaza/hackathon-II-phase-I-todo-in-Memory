from typing import List, Optional
from datetime import datetime
from src.models.task import Task, RecurrencePattern
from src.services.datetime_utils import is_datetime_in_future
from src.exceptions import TaskNotFoundError, TaskValidationError
import src.services.task_storage


class TaskService:
    """
    TaskService using global in-memory storage (task_storage).
    Handles CRUD, filtering, sorting, search, reminders, recurrence.
    """

    def __init__(self):
        # No self._tasks: use global storage instead
        pass

    # ----------------- Add Task -----------------
    def add_task(self, title: str, description: Optional[str] = None,
                 priority: str = "medium", tags: List[str] = None,
                 due_date: Optional[datetime] = None,
                 reminder_time: Optional[datetime] = None,
                 recurrence_pattern: Optional[RecurrencePattern] = None) -> Task:

        self._validate_title(title)
        if description:
            self._validate_description(description)
        if priority:
            self._validate_priority(priority)
        if tags:
            self._validate_tags(tags)
        if due_date:
            self._validate_due_date(due_date)
        if reminder_time:
            self._validate_reminder_time(reminder_time)
        if due_date and reminder_time:
            self._validate_reminder_before_due(reminder_time, due_date)
        if recurrence_pattern:
            self._validate_recurrence_pattern(recurrence_pattern)

        task_id = len(src.services.task_storage.tasks) + 1
        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            reminder_time=reminder_time,
            recurrence_pattern=recurrence_pattern
        )

        # Add to global storage
        src.services.task_storage.tasks[task_id] = task

        # If recurring, store in recurrence_templates
        if recurrence_pattern:
            src.services.task_storage.recurrence_templates[str(task_id)] = task
            task.is_recurring_template = True

        return task

    # ----------------- Get Tasks -----------------
    def get_all_tasks(self) -> List[Task]:
        return list(src.services.task_storage.tasks.values())

    def get_task_by_id(self, task_id: int) -> Task:
        task = src.services.task_storage.tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task

    # ----------------- Update Task -----------------
    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None, priority: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    due_date: Optional[datetime] = None,
                    reminder_time: Optional[datetime] = None) -> Task:

        task = self.get_task_by_id(task_id)

        if title:
            self._validate_title(title)
            task.update_title(title)
        if description:
            self._validate_description(description)
            task.update_description(description)
        if priority:
            self._validate_priority(priority)
            task.update_priority(priority)
        if tags:
            self._validate_tags(tags)
            task.update_tags(tags)
        if due_date:
            self._validate_due_date(due_date)
            task.due_date = due_date
        if reminder_time:
            self._validate_reminder_time(reminder_time)
            if due_date and reminder_time > due_date:
                raise TaskValidationError("Reminder time must be before due date")
            task.reminder_time = reminder_time

        return task

    # ----------------- Delete Task -----------------
    def delete_task(self, task_id: int) -> bool:
        task = src.services.task_storage.tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        del src.services.task_storage.tasks[task_id]

        # Remove from recurrence templates and reminders
        src.services.task_storage.recurrence_templates.pop(str(task_id), None)
        src.services.task_storage.reminders.pop(str(task_id), None)

        return True

    # ----------------- Update Status -----------------
    def update_task_status(self, task_id: int, completed: bool) -> Task:
        task = self.get_task_by_id(task_id)
        if completed:
            task.mark_complete()
        else:
            task.mark_incomplete()
        return task

    # ----------------- Search -----------------
    def search_tasks(self, keyword: str) -> List[Task]:
        if not keyword:
            raise TaskValidationError("Search keyword cannot be empty")

        keyword_lower = keyword.lower()
        return [
            task for task in src.services.task_storage.tasks.values()
            if keyword_lower in task.title.lower() or
               (task.description and keyword_lower in task.description.lower())
        ]

    # ----------------- Filter & Sort -----------------
    def filter_tasks(self, status: Optional[str] = None,
                     priority: Optional[str] = None,
                     tags: Optional[List[str]] = None) -> List[Task]:

        filtered_tasks = []
        for task in src.services.task_storage.tasks.values():
            if status:
                if status == 'complete' and not task.completed:
                    continue
                if status == 'incomplete' and task.completed:
                    continue
            if priority and task.priority != priority:
                continue
            if tags and not any(tag in task.tags for tag in tags):
                continue
            filtered_tasks.append(task)
        return filtered_tasks

    def sort_tasks(self, tasks: List[Task], sort_by: str = 'created') -> List[Task]:
        if sort_by == 'priority':
            order = {'high': 0, 'medium': 1, 'low': 2}
            return sorted(tasks, key=lambda t: order[t.priority])
        if sort_by == 'alpha':
            return sorted(tasks, key=lambda t: t.title.lower())
        if sort_by == 'created':
            return sorted(tasks, key=lambda t: t.created_at)
        return tasks

    def get_filtered_sorted_tasks(self, status: Optional[str] = None,
                                  priority: Optional[str] = None,
                                  tags: Optional[List[str]] = None,
                                  sort_by: str = 'created') -> List[Task]:
        filtered = self.filter_tasks(status, priority, tags)
        return self.sort_tasks(filtered, sort_by)

    # ----------------- Upcoming & Overdue -----------------
    def get_upcoming_tasks(self, limit: Optional[int] = None) -> List[Task]:
        tasks = [t for t in src.services.task_storage.tasks.values() if t.due_date and not t.completed]
        tasks.sort(key=lambda t: t.due_date)
        return tasks[:limit] if limit else tasks

    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        return [
            t for t in src.services.task_storage.tasks.values()
            if t.due_date and t.due_date < now and not t.completed
        ]

    # ----------------- Recurrence -----------------
    def cancel_recurrence_for_task(self, task_id: int) -> bool:
        from .recurrence_service import RecurrenceService
        return RecurrenceService.cancel_recurrence_pattern(task_id)

    def update_recurrence_for_task(self, task_id: int, new_pattern: RecurrencePattern) -> bool:
        from .recurrence_service import RecurrenceService
        return RecurrenceService.update_recurrence_pattern(task_id, new_pattern)

    # ----------------- Validation Helpers -----------------
    def _validate_title(self, title: str):
        if not title or not title.strip():
            raise TaskValidationError("Task title cannot be empty")
        if len(title) > 100:
            raise TaskValidationError("Task title exceeds 100 characters")

    def _validate_description(self, description: str):
        if description and len(description) > 500:
            raise TaskValidationError("Task description exceeds 500 characters")

    def _validate_priority(self, priority: str):
        if priority not in ['high', 'medium', 'low']:
            raise TaskValidationError("Priority must be high, medium, or low")

    def _validate_tags(self, tags: List[str]):
        for tag in tags:
            if not tag or ' ' in tag:
                raise TaskValidationError(f"Invalid tag: '{tag}'")

    def _validate_due_date(self, due_date: datetime):
        if not is_datetime_in_future(due_date):
            raise TaskValidationError(f"Due date must be in the future: {due_date}")

    def _validate_reminder_time(self, reminder_time: datetime):
        if not is_datetime_in_future(reminder_time):
            raise TaskValidationError(f"Reminder time must be in the future: {reminder_time}")

    def _validate_reminder_before_due(self, reminder_time: datetime, due_date: datetime):
        if reminder_time > due_date:
            raise TaskValidationError("Reminder must be before due date")

    def _validate_recurrence_pattern(self, recurrence_pattern: RecurrencePattern):
        pass  # handled by RecurrencePattern class
