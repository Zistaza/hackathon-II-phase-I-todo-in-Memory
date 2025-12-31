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
    """

    def __init__(self):
        """Initialize the task service with an empty in-memory collection."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task to the collection.

        Args:
            title: Task title (required)
            description: Optional task description

        Returns:
            Task: The newly created task with assigned ID

        Raises:
            TaskValidationError: If title is empty or exceeds character limits
        """
        # Validate inputs before creating task
        self._validate_title(title)
        if description:
            self._validate_description(description)

        # Create task with unique ID
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
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
                   description: Optional[str] = None) -> Task:
        """
        Update an existing task's details.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)

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