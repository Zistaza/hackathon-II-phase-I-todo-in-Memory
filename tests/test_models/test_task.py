import pytest
from datetime import datetime
from src.models.task import Task
from src.exceptions import TaskValidationError


class TestTask:
    """Unit tests for the Task model."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(id=1, title="Test Task", description="Test Description", completed=False)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.priority == "medium"  # Default priority
        assert task.tags == []  # Default tags
        assert task.created_at is not None  # Should have a timestamp

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False
        assert task.priority == "medium"  # Default priority
        assert task.tags == []  # Default tags
        assert task.created_at is not None  # Should have a timestamp

    def test_task_creation_with_priority_and_tags(self):
        """Test creating a task with priority and tags."""
        task = Task(id=1, title="Test Task", priority="high", tags=["work", "urgent"])
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.priority == "high"
        assert task.tags == ["work", "urgent"]

    def test_task_creation_fails_with_empty_title(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_task_creation_fails_with_whitespace_only_title(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="   ")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_task_creation_fails_with_long_title(self):
        """Test that creating a task with title exceeding 100 chars raises ValueError."""
        long_title = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title=long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_task_creation_fails_with_long_description(self):
        """Test that creating a task with description exceeding 500 chars raises ValueError."""
        long_description = "A" * 501
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="Test Task", description=long_description)
        assert "exceeds 500 character limit" in str(exc_info.value)

    def test_task_creation_fails_with_invalid_priority(self):
        """Test that creating a task with invalid priority raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="Test Task", priority="invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

    def test_task_creation_fails_with_invalid_tags(self):
        """Test that creating a task with invalid tags raises ValueError."""
        # Test empty tag
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="Test Task", tags=["", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(ValueError) as exc_info:
            Task(id=1, title="Test Task", tags=["valid", "with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_mark_complete_method(self):
        """Test the mark_complete method."""
        task = Task(id=1, title="Test Task", completed=False)
        task.mark_complete()
        assert task.completed is True

    def test_mark_incomplete_method(self):
        """Test the mark_incomplete method."""
        task = Task(id=1, title="Test Task", completed=True)
        task.mark_incomplete()
        assert task.completed is False

    def test_update_title_with_valid_data(self):
        """Test updating task title with valid data."""
        task = Task(id=1, title="Old Title")
        task.update_title("New Title")
        assert task.title == "New Title"

    def test_update_title_fails_with_empty_title(self):
        """Test that updating task title with empty title raises ValueError."""
        task = Task(id=1, title="Old Title")
        with pytest.raises(ValueError) as exc_info:
            task.update_title("")
        assert "Task title cannot be empty" in str(exc_info.value)

    def test_update_title_fails_with_long_title(self):
        """Test that updating task title with title exceeding 100 chars raises ValueError."""
        task = Task(id=1, title="Old Title")
        long_title = "A" * 101
        with pytest.raises(ValueError) as exc_info:
            task.update_title(long_title)
        assert "exceeds 100 character limit" in str(exc_info.value)

    def test_update_description_with_valid_data(self):
        """Test updating task description with valid data."""
        task = Task(id=1, title="Test Task", description="Old Description")
        task.update_description("New Description")
        assert task.description == "New Description"

    def test_update_description_fails_with_long_description(self):
        """Test that updating task description with description exceeding 500 chars raises ValueError."""
        task = Task(id=1, title="Test Task")
        long_description = "A" * 501
        with pytest.raises(ValueError) as exc_info:
            task.update_description(long_description)
        assert "exceeds 500 character limit" in str(exc_info.value)

    def test_update_priority_with_valid_data(self):
        """Test updating task priority with valid data."""
        task = Task(id=1, title="Test Task", priority="medium")
        task.update_priority("high")
        assert task.priority == "high"

        task.update_priority("low")
        assert task.priority == "low"

    def test_update_priority_fails_with_invalid_priority(self):
        """Test that updating task priority with invalid value raises ValueError."""
        task = Task(id=1, title="Test Task", priority="medium")
        with pytest.raises(ValueError) as exc_info:
            task.update_priority("invalid")
        assert "Priority must be one of: high, medium, low" in str(exc_info.value)

    def test_update_tags_with_valid_data(self):
        """Test updating task tags with valid data."""
        task = Task(id=1, title="Test Task", tags=["old"])
        task.update_tags(["new", "tags"])
        assert task.tags == ["new", "tags"]

    def test_update_tags_fails_with_invalid_tags(self):
        """Test that updating task tags with invalid data raises ValueError."""
        task = Task(id=1, title="Test Task", tags=["valid"])

        # Test empty tag
        with pytest.raises(ValueError) as exc_info:
            task.update_tags(["", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(ValueError) as exc_info:
            task.update_tags(["valid", "with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_add_tag_method(self):
        """Test adding a single tag to a task."""
        task = Task(id=1, title="Test Task", tags=["existing"])

        # Add a new tag
        task.add_tag("new_tag")
        assert "new_tag" in task.tags
        assert len(task.tags) == 2

        # Add a duplicate tag (should not be added)
        task.add_tag("new_tag")
        assert task.tags.count("new_tag") == 1  # Should only appear once
        assert len(task.tags) == 2

    def test_add_tag_fails_with_invalid_tag(self):
        """Test that adding invalid tags raises ValueError."""
        task = Task(id=1, title="Test Task")

        # Test empty tag
        with pytest.raises(ValueError) as exc_info:
            task.add_tag("")
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(ValueError) as exc_info:
            task.add_tag("with spaces")
        assert "Tag cannot contain spaces" in str(exc_info.value)

    def test_remove_tag_method(self):
        """Test removing a tag from a task."""
        task = Task(id=1, title="Test Task", tags=["tag1", "tag2", "tag3"])

        # Remove existing tag
        task.remove_tag("tag2")
        assert "tag2" not in task.tags
        assert len(task.tags) == 2
        assert task.tags == ["tag1", "tag3"]

        # Remove non-existing tag (should not error)
        task.remove_tag("nonexistent")
        assert len(task.tags) == 2  # Should remain unchanged

    def test_created_at_is_set_on_initialization(self):
        """Test that created_at is set automatically on initialization."""
        before_creation = datetime.now()
        task = Task(id=1, title="Test Task")
        after_creation = datetime.now()

        assert task.created_at is not None
        assert before_creation <= task.created_at <= after_creation