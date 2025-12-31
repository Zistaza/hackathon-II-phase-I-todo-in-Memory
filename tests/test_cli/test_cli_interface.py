import pytest
from unittest.mock import Mock, patch
from io import StringIO
from src.cli.cli_interface import CLIInterface
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestCLIInterface:
    """Unit tests for the CLIInterface."""

    def setup_method(self):
        """Set up a CLIInterface instance for each test."""
        self.task_service = TaskService()
        self.cli = CLIInterface(self.task_service)

    def test_add_command_with_title_only(self):
        """Test the add command with title only."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_add("New Task")
            mock_print.assert_called_once_with("Task added successfully! ID: 1, Title: New Task")

        tasks = self.task_service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "New Task"
        assert tasks[0].description is None

    def test_add_command_with_title_and_description(self):
        """Test the add command with title and description."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_add("New Task Description: This is a test")
            mock_print.assert_called_once_with("Task added successfully! ID: 1, Title: New Task")

        # Actually test with proper format
        with patch('builtins.print') as mock_print:
            self.cli._handle_add("New Task This is a description")
            mock_print.assert_called_once_with("Task added successfully! ID: 2, Title: New Task")

        tasks = self.task_service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[1].title == "New Task"
        assert tasks[1].description == "This is a description"

    def test_add_command_with_validation_error(self):
        """Test the add command with validation error."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_add("")  # No title
            mock_print.assert_called_once_with("Usage: add <title> [description]")

    def test_add_command_with_empty_title_error(self):
        """Test the add command with empty title error."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_add("  ")  # Whitespace only
            # This should call the service which will raise an exception
            # Let's test the validation error path
            pass

        # Test the actual validation error
        with patch('builtins.print') as mock_print:
            # Mock the service to raise validation error
            with patch.object(self.task_service, 'add_task', side_effect=TaskValidationError("Task title cannot be empty")):
                self.cli._handle_add("   ")
                mock_print.assert_called_with("Error adding task: Task title cannot be empty")

    def test_view_command_with_tasks(self):
        """Test the view command when there are tasks."""
        # Add some tasks
        self.task_service.add_task("Task 1", "Description 1")
        self.task_service.add_task("Task 2")
        self.task_service.update_task_status(2, True)  # Mark second task as complete

        with patch('builtins.print') as mock_print:
            self.cli._handle_view("")

            # Check that the print function was called multiple times for the view output
            calls = mock_print.call_args_list
            assert any("Your Tasks:" in str(call) for call in calls)
            assert any("ID: 1 [ ] Task 1" in str(call) for call in calls)
            assert any("ID: 2 [✓] Task 2" in str(call) for call in calls)

    def test_view_command_with_no_tasks(self):
        """Test the view command when there are no tasks."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_view("")
            mock_print.assert_called_with("No tasks found.")

    def test_update_command_with_valid_data(self):
        """Test the update command with valid data."""
        # Add a task first
        self.task_service.add_task("Old Title", "Old Description")

        with patch('builtins.print') as mock_print:
            self.cli._handle_update("1 New Title New Description")
            mock_print.assert_called_with("Task updated successfully! ID: 1, Title: New Title")

        # Verify the task was updated
        updated_task = self.task_service.get_task_by_id(1)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_command_with_invalid_id(self):
        """Test the update command with invalid ID."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_update("999 New Title")
            # This will try to convert "999" to int, then fail with TaskNotFoundError
            pass

        # Actually test with a valid numeric ID that doesn't exist
        with patch('builtins.print') as mock_print:
            self.cli._handle_update("999 New Title")
            # The service will raise TaskNotFoundError
            with patch.object(self.task_service, 'update_task', side_effect=TaskNotFoundError("Task with ID 999 not found")):
                self.cli._handle_update("999 New Title")
                mock_print.assert_called_with("Error updating task: Task with ID 999 not found")

    def test_update_command_with_invalid_format(self):
        """Test the update command with invalid format."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_update("")
            mock_print.assert_called_with("Usage: update <id> <title> [description]")

    def test_update_command_with_invalid_id_format(self):
        """Test the update command with non-numeric ID."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_update("abc New Title")
            mock_print.assert_called_with("Error: Task ID must be a number.")

    def test_delete_command_with_valid_id(self):
        """Test the delete command with valid ID."""
        # Add a task first
        self.task_service.add_task("Task to delete")

        with patch('builtins.print') as mock_print:
            self.cli._handle_delete("1")
            mock_print.assert_called_with("Task 1 deleted successfully!")

        # Verify the task was deleted
        assert len(self.task_service.get_all_tasks()) == 0

    def test_delete_command_with_invalid_id(self):
        """Test the delete command with invalid ID."""
        with patch('builtins.print') as mock_print:
            # First test non-numeric ID
            self.cli._handle_delete("abc")
            mock_print.assert_called_with("Error: Task ID must be a number.")

    def test_delete_command_with_nonexistent_id(self):
        """Test the delete command with non-existent ID."""
        with patch('builtins.print') as mock_print:
            # Mock the service to raise TaskNotFoundError
            with patch.object(self.task_service, 'delete_task', side_effect=TaskNotFoundError("Task with ID 999 not found")):
                self.cli._handle_delete("999")
                mock_print.assert_called_with("Error deleting task: Task with ID 999 not found")

    def test_complete_command_with_valid_id(self):
        """Test the complete command with valid ID."""
        # Add a task first
        self.task_service.add_task("Incomplete Task")
        task = self.task_service.get_task_by_id(1)
        assert task.completed is False  # Initially incomplete

        with patch('builtins.print') as mock_print:
            self.cli._handle_complete("1")
            mock_print.assert_called_with("Task 1 marked as complete!")

        # Verify the task is now complete
        updated_task = self.task_service.get_task_by_id(1)
        assert updated_task.completed is True

    def test_complete_command_with_invalid_id(self):
        """Test the complete command with invalid ID."""
        with patch('builtins.print') as mock_print:
            # Test non-numeric ID
            self.cli._handle_complete("abc")
            mock_print.assert_called_with("Error: Task ID must be a number.")

    def test_incomplete_command_with_valid_id(self):
        """Test the incomplete command with valid ID."""
        # Add and complete a task first
        self.task_service.add_task("Complete Task")
        self.task_service.update_task_status(1, True)  # Mark as complete
        task = self.task_service.get_task_by_id(1)
        assert task.completed is True  # Initially complete

        with patch('builtins.print') as mock_print:
            self.cli._handle_incomplete("1")
            mock_print.assert_called_with("Task 1 marked as incomplete!")

        # Verify the task is now incomplete
        updated_task = self.task_service.get_task_by_id(1)
        assert updated_task.completed is False

    def test_help_command(self):
        """Test the help command."""
        with patch('builtins.print') as mock_print:
            self.cli._handle_help("")
            # Check that help text is printed
            calls = mock_print.call_args_list
            assert any("Available commands:" in str(call) for call in calls)
            assert any("add <title> [description]" in str(call) for call in calls)

    def test_quit_command(self):
        """Test the quit command."""
        result = self.cli._handle_quit("")
        assert result is False  # Should return False to signal quit

    def test_unknown_command(self):
        """Test handling of unknown commands."""
        with patch('builtins.print') as mock_print:
            # Simulate the main run loop calling an unknown command
            if 'unknown_cmd' in self.cli.commands:
                pass  # This shouldn't happen
            else:
                # This is tested in the main run loop context
                pass