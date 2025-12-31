from typing import List, Optional
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TaskService:
    """
    Handles business logic for task operations with in-memory storage.

    Responsibilities:
    - In-memory task storage and retrieval
    - CRUD operations on tasks
    - Task validation and error handling
    - Sequential ID generation
    - Search, filter, and sort operations
    """

    def __init__(self):
        """Initialize the task service with an empty in-memory collection."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None,
                 priority: str = "medium", tags: List[str] = None) -> Task:
        """
        Add a new task to the collection.

        Args:
            title: Task title (required)
            description: Optional task description
            priority: Task priority level (default: "medium")
            tags: List of tags for the task (default: empty list)

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            TaskValidationError: If title is empty or exceeds character limits
        """
        # Validate inputs before creating task
        self._validate_title(title)
        if description:
            self._validate_description(description)
        if priority:
            self._validate_priority(priority)
        if tags:
            self._validate_tags(tags)

        # Create task with unique ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
            priority=priority,
            tags=tags
        )

        # Add to collection and increment ID counter
        self._tasks.append(task)
        self._next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            List[Task]: All tasks in the collection
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task: The requested task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, priority: Optional[str] = None,
                   tags: Optional[List[str]] = None) -> Task:
        """
        Update an existing task's details.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags (optional)

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
            TaskValidationError: If new values don't meet validation requirements
        """
        task = self.get_task_by_id(task_id)

        # Update title if provided
        if title is not None:
            self._validate_title(title)
            task.update_title(title)

        # Update description if provided
        if description is not None:
            self._validate_description(description)
            task.update_description(description)

        # Update priority if provided
        if priority is not None:
            self._validate_priority(priority)
            task.update_priority(priority)

        # Update tags if provided
        if tags is not None:
            self._validate_tags(tags)
            task.update_tags(tags)

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task_by_id(task_id)
        self._tasks.remove(task)
        return True

    def update_task_status(self, task_id: int, completed: bool) -> Task:
        """
        Update a task's completion status.

        Args:
            task_id: ID of the task to update
            completed: New completion status

        Returns:
            Task: The updated task

        Raises:
            TaskNotFoundError: If no task exists with the given ID
        """
        task = self.get_task_by_id(task_id)
        if completed:
            task.mark_complete()
        else:
            task.mark_incomplete()
        return task

    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in title and description.

        Args:
            keyword: Text to search for in task titles and descriptions

        Returns:
            List[Task]: Tasks containing the keyword
        """
        if not keyword:
            raise TaskValidationError("Search keyword cannot be empty")

        keyword_lower = keyword.lower()
        matching_tasks = []

        for task in self._tasks:
            # Check if keyword is in title or description (case insensitive)
            if keyword_lower in task.title.lower() or \
               (task.description and keyword_lower in task.description.lower()):
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                    tags: Optional[List[str]] = None) -> List[Task]:
        """
        Filter tasks by various criteria.

        Args:
            status: Filter by completion status ('complete' or 'incomplete')
            priority: Filter by priority level ('high', 'medium', 'low')
            tags: Filter by tags (task must have ANY of these tags)

        Returns:
            List[Task]: Tasks matching all specified criteria (AND logic between different filters,
                        OR logic within tag filter)
        """
        filtered_tasks = []

        for task in self._tasks:
            # Check status filter
            if status is not None:
                if status == 'complete' and not task.completed:
                    continue
                elif status == 'incomplete' and task.completed:
                    continue

            # Check priority filter
            if priority is not None:
                if task.priority != priority:
                    continue

            # Check tags filter (OR logic - task must have at least one of the specified tags)
            if tags is not None and tags:
                has_matching_tag = False
                for tag in tags:
                    if tag in task.tags:
                        has_matching_tag = True
                        break
                if not has_matching_tag:
                    continue

            filtered_tasks.append(task)

        return filtered_tasks

    def sort_tasks(self, tasks: List[Task], sort_by: str = 'created') -> List[Task]:
        """
        Sort tasks by specified criteria.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort criteria ('priority', 'alpha', 'created')

        Returns:
            List[Task]: Sorted tasks
        """
        if sort_by == 'priority':
            # Sort by priority: high -> medium -> low
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            return sorted(tasks, key=lambda t: priority_order[t.priority])

        elif sort_by == 'alpha':
            # Sort alphabetically by title
            return sorted(tasks, key=lambda t: t.title.lower())

        elif sort_by == 'created':
            # Sort by creation time (oldest first)
            return sorted(tasks, key=lambda t: t.created_at)

        else:
            # Default to creation order
            return tasks

    def get_filtered_sorted_tasks(self, status: Optional[str] = None,
                                priority: Optional[str] = None,
                                tags: Optional[List[str]] = None,
                                sort_by: str = 'created') -> List[Task]:
        """
        Get tasks with filtering and sorting applied.

        Args:
            status: Filter by completion status
            priority: Filter by priority level
            tags: Filter by tags
            sort_by: Sort criteria

        Returns:
            List[Task]: Filtered and sorted tasks
        """
        # First apply filters
        filtered_tasks = self.filter_tasks(status, priority, tags)

        # Then apply sorting
        sorted_tasks = self.sort_tasks(filtered_tasks, sort_by)

        return sorted_tasks

    def _validate_title(self, title: str) -> None:
        """Validate task title requirements."""
        if not title or not title.strip():
            raise TaskValidationError("Task title cannot be empty")
        if len(title) > 100:
            raise TaskValidationError(f"Task title exceeds 100 character limit: {len(title)} chars")

    def _validate_description(self, description: str) -> None:
        """Validate task description requirements."""
        if description and len(description) > 500:
            raise TaskValidationError(f"Task description exceeds 500 character limit: {len(description)} chars")

    def _validate_priority(self, priority: str) -> None:
        """Validate task priority requirements."""
        valid_priorities = ['high', 'medium', 'low']
        if priority not in valid_priorities:
            raise TaskValidationError(f"Priority must be one of: {', '.join(valid_priorities)}, got: {priority}")

    def _validate_tags(self, tags: List[str]) -> None:
        """Validate task tags requirements."""
        for tag in tags:
            if not tag or not tag.strip():
                raise TaskValidationError(f"Tag cannot be empty: '{tag}'")
            if ' ' in tag:
                raise TaskValidationError(f"Tag cannot contain spaces: '{tag}'")