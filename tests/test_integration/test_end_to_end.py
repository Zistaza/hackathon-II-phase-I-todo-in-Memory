import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestEndToEnd:
    """Integration tests for end-to-end workflows."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    def test_complete_workflow_add_view_update_complete_delete(self):
        """Test the complete workflow: add → view → update → view → complete → view → delete → view."""
        # 1. Add tasks
        task1 = self.service.add_task("First Task", "Description for first task")
        task2 = self.service.add_task("Second Task")

        assert len(self.service.get_all_tasks()) == 2
        assert task1.id == 1
        assert task2.id == 2
        assert task1.title == "First Task"
        assert task1.description == "Description for first task"
        assert task2.title == "Second Task"
        assert task2.description is None

        # 2. View tasks
        all_tasks = self.service.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2

        # 3. Update task
        updated_task = self.service.update_task(1, title="Updated First Task", description="Updated description")
        assert updated_task.title == "Updated First Task"
        assert updated_task.description == "Updated description"

        # Verify update worked by getting the task again
        retrieved_task = self.service.get_task_by_id(1)
        assert retrieved_task.title == "Updated First Task"
        assert retrieved_task.description == "Updated description"

        # 4. Mark task as complete
        completed_task = self.service.update_task_status(2, True)
        assert completed_task.completed is True

        # Verify completion worked
        retrieved_task2 = self.service.get_task_by_id(2)
        assert retrieved_task2.completed is True

        # 5. Delete task
        result = self.service.delete_task(1)
        assert result is True

        # Verify deletion worked
        remaining_tasks = self.service.get_all_tasks()
        assert len(remaining_tasks) == 1
        assert remaining_tasks[0].id == 2

    def test_error_flow_validation_errors(self):
        """Test error flow for validation errors."""
        # Test adding task with empty title
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.add_task("")
        assert "Task title cannot be empty" in str(exc_info.value)

        # Test adding task with long title
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.add_task("A" * 101)  # 101 characters
        assert "exceeds 100 character limit" in str(exc_info.value)

        # Test adding task with long description
        with pytest.raises(TaskValidationError) as exc_info:
            self.service.add_task("Valid Title", "A" * 501)  # 501 characters
        assert "exceeds 500 character limit" in str(exc_info.value)

        # Verify no tasks were added due to validation errors
        assert len(self.service.get_all_tasks()) == 0

    def test_error_flow_nonexistent_task_operations(self):
        """Test error flow for operations on non-existent tasks."""
        # Try to get non-existent task
        with pytest.raises(TaskNotFoundError) as exc_info:
            self.service.get_task_by_id(999)
        assert "Task with ID 999 not found" in str(exc_info.value)

        # Try to update non-existent task
        with pytest.raises(TaskNotFoundError) as exc_info:
            self.service.update_task(999, title="New Title")
        assert "Task with ID 999 not found" in str(exc_info.value)

        # Try to delete non-existent task
        with pytest.raises(TaskNotFoundError) as exc_info:
            self.service.delete_task(999)
        assert "Task with ID 999 not found" in str(exc_info.value)

        # Try to update status of non-existent task
        with pytest.raises(TaskNotFoundError) as exc_info:
            self.service.update_task_status(999, True)
        assert "Task with ID 999 not found" in str(exc_info.value)

    def test_edge_case_empty_task_list(self):
        """Test edge case for empty task list."""
        # Initially should be empty
        tasks = self.service.get_all_tasks()
        assert len(tasks) == 0

        # View empty list
        empty_tasks = self.service.get_all_tasks()
        assert len(empty_tasks) == 0

    def test_unique_id_generation(self):
        """Test that unique IDs are generated sequentially."""
        task1 = self.service.add_task("Task 1")
        task2 = self.service.add_task("Task 2")
        task3 = self.service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # Delete a task and add another - ID should continue sequence
        self.service.delete_task(2)
        task4 = self.service.add_task("Task 4")
        assert task4.id == 4  # Should be next in sequence, not reuse ID 2

    def test_task_status_management(self):
        """Test complete task status management workflow."""
        task = self.service.add_task("Test Task")
        assert task.completed is False

        # Mark complete
        completed_task = self.service.update_task_status(1, True)
        assert completed_task.completed is True

        # Mark incomplete again
        incomplete_task = self.service.update_task_status(1, False)
        assert incomplete_task.completed is False

        # Mark complete again
        completed_task = self.service.update_task_status(1, True)
        assert completed_task.completed is True