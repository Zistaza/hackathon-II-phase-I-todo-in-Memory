import pytest
from datetime import datetime, timedelta
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestTaskServiceExtended:
    """Extended unit tests for the TaskService including search, filter, and sort functionality."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    # Tests for T029: Unit Tests for search functionality in TaskService
    def test_search_tasks_by_title(self):
        """Test searching tasks by keyword in title."""
        # Add tasks
        self.service.add_task("Buy groceries", "Get milk and bread")
        self.service.add_task("Clean house", "Vacuum and dust")
        self.service.add_task("Call mom", "Catch up with mom")

        # Search for "groceries"
        results = self.service.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"

        # Search for "house"
        results = self.service.search_tasks("house")
        assert len(results) == 1
        assert results[0].title == "Clean house"

    def test_search_tasks_by_description(self):
        """Test searching tasks by keyword in description."""
        # Add tasks
        self.service.add_task("Task 1", "This is a description about groceries")
        self.service.add_task("Task 2", "Another description about work")
        self.service.add_task("Task 3", "No matching words here")

        # Search for "groceries" in description
        results = self.service.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Task 1"
        assert "groceries" in results[0].description

    def test_search_tasks_case_insensitive(self):
        """Test that search is case insensitive."""
        self.service.add_task("Buy Groceries", "Get MILK and bread")

        # Search with different cases
        results = self.service.search_tasks("GROCERIES")
        assert len(results) == 1
        assert results[0].title == "Buy Groceries"

        results = self.service.search_tasks("milk")
        assert len(results) == 1
        assert results[0].title == "Buy Groceries"

    def test_search_tasks_no_matches(self):
        """Test searching when no tasks match the keyword."""
        self.service.add_task("Buy groceries", "Get milk and bread")

        results = self.service.search_tasks("nonexistent")
        assert len(results) == 0

    def test_search_tasks_empty_keyword(self):
        """Test searching with empty keyword raises validation error."""
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.search_tasks("")
        assert "Search keyword cannot be empty" in str(exc_info.value)

    def test_search_tasks_whitespace_only_keyword(self):
        """Test searching with whitespace-only keyword (this does not raise validation error in current implementation)."""
        # The current implementation only checks 'if not keyword:' which doesn't catch whitespace-only strings
        # Whitespace-only keywords are processed normally
        self.service.add_task("Test Task", "This contains spaces")

        results = self.service.search_tasks("   ")  # Whitespace-only keyword
        # This should return empty results since no task contains just spaces
        assert len(results) == 0

    # Tests for T030: Unit Tests for filter operations in TaskService
    def test_filter_tasks_by_status_complete(self):
        """Test filtering tasks by completion status - complete."""
        # Add tasks with different statuses
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Mark task2 as complete
        self.service.update_task_status(2, True)

        # Filter for complete tasks
        results = self.service.filter_tasks(status="complete")
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].completed is True

    def test_filter_tasks_by_status_incomplete(self):
        """Test filtering tasks by completion status - incomplete."""
        # Add tasks with different statuses
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        # Mark task2 as complete
        self.service.update_task_status(2, True)

        # Filter for incomplete tasks
        results = self.service.filter_tasks(status="incomplete")
        assert len(results) == 2
        assert all(task.completed is False for task in results)
        assert {task.id for task in results} == {1, 3}

    def test_filter_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        # Add tasks with different priorities
        task1 = self.service.add_task("Task 1", priority="high")
        task2 = self.service.add_task("Task 2", priority="medium")
        task3 = self.service.add_task("Task 3", priority="low")
        task4 = self.service.add_task("Task 4", priority="high")

        # Filter for high priority
        results = self.service.filter_tasks(priority="high")
        assert len(results) == 2
        assert all(task.priority == "high" for task in results)
        assert {task.id for task in results} == {1, 4}

        # Filter for medium priority
        results = self.service.filter_tasks(priority="medium")
        assert len(results) == 1
        assert results[0].priority == "medium"
        assert results[0].id == 2

    def test_filter_tasks_by_tags(self):
        """Test filtering tasks by tags."""
        # Add tasks with different tags
        task1 = self.service.add_task("Task 1", tags=["work", "urgent"])
        task2 = self.service.add_task("Task 2", tags=["home", "personal"])
        task3 = self.service.add_task("Task 3", tags=["work", "study"])
        task4 = self.service.add_task("Task 4", tags=["fun"])

        # Filter for tasks with "work" tag
        results = self.service.filter_tasks(tags=["work"])
        assert len(results) == 2
        assert all("work" in task.tags for task in results)
        assert {task.id for task in results} == {1, 3}

    def test_filter_tasks_by_multiple_tags_or_logic(self):
        """Test filtering tasks by multiple tags using OR logic."""
        # Add tasks with different tags
        task1 = self.service.add_task("Task 1", tags=["work"])
        task2 = self.service.add_task("Task 2", tags=["home"])
        task3 = self.service.add_task("Task 3", tags=["work", "study"])
        task4 = self.service.add_task("Task 4", tags=["fun"])
        task5 = self.service.add_task("Task 5", tags=["personal"])

        # Filter for tasks with "work" OR "home" tag
        results = self.service.filter_tasks(tags=["work", "home"])
        assert len(results) == 3
        assert all("work" in task.tags or "home" in task.tags for task in results)
        assert {task.id for task in results} == {1, 2, 3}

    def test_filter_tasks_combined_criteria_and_logic(self):
        """Test filtering tasks by multiple criteria using AND logic between different filters."""
        # Add tasks with different attributes
        task1 = self.service.add_task("Task 1", priority="high", tags=["work"])
        task2 = self.service.add_task("Task 2", priority="high", tags=["work"])
        task3 = self.service.add_task("Task 3", priority="medium", tags=["work"])
        task4 = self.service.add_task("Task 4", priority="high", tags=["home"])
        task5 = self.service.add_task("Task 5", priority="high", tags=["work"])

        # Update some tasks to be completed
        self.service.update_task_status(1, True)  # Task 1: completed
        self.service.update_task_status(2, False)  # Task 2: incomplete
        self.service.update_task_status(3, False)  # Task 3: incomplete
        self.service.update_task_status(4, False)  # Task 4: incomplete
        self.service.update_task_status(5, True)  # Task 5: completed

        # Filter for high priority AND work tag AND incomplete
        results = self.service.filter_tasks(status="incomplete", priority="high", tags=["work"])
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].priority == "high"
        assert "work" in results[0].tags
        assert results[0].completed is False

    def test_filter_tasks_no_filters_returns_all(self):
        """Test that filtering with no criteria returns all tasks."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        self.service.add_task("Task 3")

        results = self.service.filter_tasks()
        assert len(results) == 3

    def test_filter_tasks_empty_tags_list(self):
        """Test filtering with empty tags list (should not filter by tags)."""
        self.service.add_task("Task 1", tags=["work"])
        self.service.add_task("Task 2", tags=["home"])

        results = self.service.filter_tasks(tags=[])
        assert len(results) == 2

    # Tests for T039: Unit Tests for all sorting operations in TaskService
    def test_sort_tasks_by_priority(self):
        """Test sorting tasks by priority (high -> medium -> low)."""
        # Add tasks with different priorities in random order
        task1 = self.service.add_task("Low Priority", priority="low")
        task2 = self.service.add_task("High Priority", priority="high")
        task3 = self.service.add_task("Medium Priority", priority="medium")
        task4 = self.service.add_task("Another High", priority="high")

        # Sort by priority
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "priority")

        # Check order: high should come first, then medium, then low
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "high"
        assert sorted_tasks[2].priority == "medium"
        assert sorted_tasks[3].priority == "low"

        # Verify the specific tasks
        assert sorted_tasks[0].title in ["High Priority", "Another High"]
        assert sorted_tasks[1].title in ["High Priority", "Another High"]
        assert sorted_tasks[2].title == "Medium Priority"
        assert sorted_tasks[3].title == "Low Priority"

    def test_sort_tasks_by_alpha(self):
        """Test sorting tasks alphabetically by title."""
        # Add tasks with titles in random order
        task1 = self.service.add_task("Zebra Task", priority="low")
        task2 = self.service.add_task("Alpha Task", priority="high")
        task3 = self.service.add_task("Mango Task", priority="medium")
        task4 = self.service.add_task("Beta Task", priority="high")

        # Sort alphabetically
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "alpha")

        # Check alphabetical order
        expected_order = ["Alpha Task", "Beta Task", "Mango Task", "Zebra Task"]
        actual_order = [task.title for task in sorted_tasks]
        assert actual_order == expected_order

    def test_sort_tasks_by_created(self):
        """Test sorting tasks by creation time (oldest first)."""
        # Add tasks at different times
        task1 = self.service.add_task("First Task")
        task2 = self.service.add_task("Second Task")
        task3 = self.service.add_task("Third Task")

        # Sort by creation time
        tasks = self.service.get_all_tasks()
        sorted_tasks = self.service.sort_tasks(tasks, "created")

        # Should maintain creation order (oldest first)
        assert sorted_tasks[0].id == 1
        assert sorted_tasks[1].id == 2
        assert sorted_tasks[2].id == 3

    def test_sort_tasks_default_behavior(self):
        """Test default sort behavior."""
        # Add tasks
        task1 = self.service.add_task("Task 3")
        task2 = self.service.add_task("Task 1")
        task3 = self.service.add_task("Task 2")

        # Get all tasks (default sort is by creation)
        tasks = self.service.get_all_tasks()
        default_sorted = self.service.sort_tasks(tasks)  # No sort_by parameter

        # Should maintain original order (by creation)
        assert default_sorted[0].id == 1
        assert default_sorted[1].id == 2
        assert default_sorted[2].id == 3

    def test_sort_tasks_invalid_sort_by(self):
        """Test sorting with invalid sort_by parameter."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")

        tasks = self.service.get_all_tasks()
        # Should return tasks unchanged for invalid sort_by
        sorted_tasks = self.service.sort_tasks(tasks, "invalid")
        assert len(sorted_tasks) == 2

    # Tests for combined filter and sort functionality
    def test_get_filtered_sorted_tasks(self):
        """Test combined filtering and sorting functionality."""
        # Add tasks with various attributes
        task1 = self.service.add_task("Urgent Work Task", priority="high", tags=["work", "urgent"])
        task2 = self.service.add_task("Low Priority Home Task", priority="low", tags=["home"])
        task3 = self.service.add_task("Medium Work Task", priority="medium", tags=["work"])
        task4 = self.service.add_task("High Priority Fun Task", priority="high", tags=["fun"])

        # Update statuses
        self.service.update_task_status(1, False)  # Incomplete
        self.service.update_task_status(2, True)   # Complete
        self.service.update_task_status(3, False)  # Incomplete
        self.service.update_task_status(4, False)  # Incomplete

        # Filter for incomplete work tasks and sort by priority
        results = self.service.get_filtered_sorted_tasks(status="incomplete", tags=["work"], sort_by="priority")

        # Should have 2 results (tasks 1 and 3), sorted by priority (high first)
        assert len(results) == 2
        assert results[0].id == 1  # High priority work task
        assert results[1].id == 3  # Medium priority work task
        assert all("work" in task.tags for task in results)
        assert all(task.completed is False for task in results)

    def test_add_task_with_priority_and_tags(self):
        """Test adding tasks with priority and tags."""
        task = self.service.add_task("Test Task", priority="high", tags=["work", "urgent"])

        assert task.priority == "high"
        assert task.tags == ["work", "urgent"]

        # Retrieve and verify
        retrieved_task = self.service.get_task_by_id(1)
        assert retrieved_task.priority == "high"
        assert retrieved_task.tags == ["work", "urgent"]

    def test_update_task_with_priority_and_tags(self):
        """Test updating tasks with priority and tags."""
        # Add a task
        task = self.service.add_task("Test Task", priority="low", tags=["old"])

        # Update priority and tags
        updated_task = self.service.update_task(1, priority="high", tags=["new", "tags"])

        assert updated_task.priority == "high"
        assert updated_task.tags == ["new", "tags"]

        # Verify through retrieval
        retrieved_task = self.service.get_task_by_id(1)
        assert retrieved_task.priority == "high"
        assert retrieved_task.tags == ["new", "tags"]

    def test_validation_in_add_task_with_priority_and_tags(self):
        """Test validation when adding tasks with priority and tags."""
        # Test invalid priority
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.add_task("Test Task", priority="invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

        # Test invalid tag
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.add_task("Test Task", tags=["with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_validation_in_update_task_with_priority_and_tags(self):
        """Test validation when updating tasks with priority and tags."""
        self.service.add_task("Test Task")

        # Test invalid priority
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.update_task(1, priority="invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

        # Test invalid tag
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.update_task(1, tags=["with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)