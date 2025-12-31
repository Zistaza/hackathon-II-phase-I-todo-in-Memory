import pytest
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestIntegrationCombinedOperations:
    """Integration tests for combined filter operations and complex workflows (T031, T043)."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    # Tests for T031: Integration Tests for combined filter operations
    def test_combined_filter_status_and_priority(self):
        """Test filtering by both status and priority."""
        # Add tasks with different combinations of status and priority
        task1 = self.service.add_task("High Priority Complete", priority="high")
        task2 = self.service.add_task("High Priority Incomplete", priority="high")
        task3 = self.service.add_task("Low Priority Complete", priority="low")
        task4 = self.service.add_task("Low Priority Incomplete", priority="low")
        task5 = self.service.add_task("Medium Priority Incomplete", priority="medium")

        # Update statuses
        self.service.update_task_status(1, True)   # Complete
        self.service.update_task_status(2, False)  # Incomplete
        self.service.update_task_status(3, True)   # Complete
        self.service.update_task_status(4, False)  # Incomplete
        self.service.update_task_status(5, False)  # Incomplete

        # Filter for high priority AND incomplete
        results = self.service.filter_tasks(status="incomplete", priority="high")
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].priority == "high"
        assert results[0].completed is False

        # Filter for low priority AND complete
        results = self.service.filter_tasks(status="complete", priority="low")
        assert len(results) == 1
        assert results[0].id == 3
        assert results[0].priority == "low"
        assert results[0].completed is True

        # Filter for medium priority AND incomplete
        results = self.service.filter_tasks(status="incomplete", priority="medium")
        assert len(results) == 1
        assert results[0].id == 5
        assert results[0].priority == "medium"
        assert results[0].completed is False

    def test_combined_filter_status_and_tags(self):
        """Test filtering by both status and tags."""
        # Add tasks with different combinations of status and tags
        task1 = self.service.add_task("Complete Work Task", tags=["work"])
        task2 = self.service.add_task("Incomplete Work Task", tags=["work"])
        task3 = self.service.add_task("Complete Home Task", tags=["home"])
        task4 = self.service.add_task("Incomplete Home Task", tags=["home"])
        task5 = self.service.add_task("Incomplete Fun Task", tags=["fun"])

        # Update statuses
        self.service.update_task_status(1, True)   # Complete
        self.service.update_task_status(2, False)  # Incomplete
        self.service.update_task_status(3, True)   # Complete
        self.service.update_task_status(4, False)  # Incomplete
        self.service.update_task_status(5, False)  # Incomplete

        # Filter for incomplete AND work tag
        results = self.service.filter_tasks(status="incomplete", tags=["work"])
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].completed is False
        assert "work" in results[0].tags

        # Filter for complete AND home tag
        results = self.service.filter_tasks(status="complete", tags=["home"])
        assert len(results) == 1
        assert results[0].id == 3
        assert results[0].completed is True
        assert "home" in results[0].tags

    def test_combined_filter_priority_and_tags(self):
        """Test filtering by both priority and tags."""
        # Add tasks with different combinations of priority and tags
        task1 = self.service.add_task("High Work Task", priority="high", tags=["work"])
        task2 = self.service.add_task("High Home Task", priority="high", tags=["home"])
        task3 = self.service.add_task("Low Work Task", priority="low", tags=["work"])
        task4 = self.service.add_task("Medium Home Task", priority="medium", tags=["home"])
        task5 = self.service.add_task("High Fun Task", priority="high", tags=["fun"])

        # Filter for high priority AND work tag
        results = self.service.filter_tasks(priority="high", tags=["work"])
        assert len(results) == 1
        assert results[0].id == 1
        assert results[0].priority == "high"
        assert "work" in results[0].tags

        # Filter for high priority AND (work OR home)
        results = self.service.filter_tasks(priority="high", tags=["work", "home"])
        assert len(results) == 2
        assert all(task.priority == "high" for task in results)
        assert all("work" in task.tags or "home" in task.tags for task in results)

    def test_combined_filter_all_three_criteria(self):
        """Test filtering by status, priority, and tags simultaneously."""
        # Add tasks with different combinations of all three criteria
        task1 = self.service.add_task("High Priority Complete Work", priority="high", tags=["work"])
        task2 = self.service.add_task("High Priority Incomplete Work", priority="high", tags=["work"])
        task3 = self.service.add_task("High Priority Complete Home", priority="high", tags=["home"])
        task4 = self.service.add_task("Low Priority Incomplete Work", priority="low", tags=["work"])
        task5 = self.service.add_task("Medium Priority Incomplete Work", priority="medium", tags=["work"])

        # Update statuses
        self.service.update_task_status(1, True)   # Complete
        self.service.update_task_status(2, False)  # Incomplete
        self.service.update_task_status(3, True)   # Complete
        self.service.update_task_status(4, False)  # Incomplete
        self.service.update_task_status(5, False)  # Incomplete

        # Filter for high priority, incomplete, AND work tag
        results = self.service.filter_tasks(status="incomplete", priority="high", tags=["work"])
        assert len(results) == 1
        assert results[0].id == 2
        assert results[0].priority == "high"
        assert results[0].completed is False
        assert "work" in results[0].tags

    def test_combined_filter_no_matches(self):
        """Test combined filtering when no tasks match all criteria."""
        # Add tasks
        task1 = self.service.add_task("Complete Task", priority="high", tags=["work"])
        task2 = self.service.add_task("Incomplete Task", priority="low", tags=["home"])

        # Update statuses
        self.service.update_task_status(1, True)   # Complete
        self.service.update_task_status(2, False)  # Incomplete

        # Try to filter for high priority, incomplete, AND work tag
        # Task 1: high priority, complete, work tag -> doesn't match incomplete
        # Task 2: low priority, incomplete, home tag -> doesn't match high priority or work tag
        results = self.service.filter_tasks(status="incomplete", priority="high", tags=["work"])
        assert len(results) == 0

    # Tests for T043: Comprehensive integration tests for combined operations (filter + sort)
    def test_combined_filter_and_sort_priority(self):
        """Test filtering tasks and then sorting the results by priority."""
        # Add tasks with different priorities and tags
        task1 = self.service.add_task("Low Priority Work", priority="low", tags=["work"])
        task2 = self.service.add_task("High Priority Work", priority="high", tags=["work"])
        task3 = self.service.add_task("Medium Priority Work", priority="medium", tags=["work"])
        task4 = self.service.add_task("High Priority Home", priority="high", tags=["home"])
        task5 = self.service.add_task("Low Priority Fun", priority="low", tags=["fun"])

        # Filter for work tasks and sort by priority (high to low)
        filtered_tasks = self.service.filter_tasks(tags=["work"])
        sorted_tasks = self.service.sort_tasks(filtered_tasks, "priority")

        # Should have 3 work tasks, sorted high -> medium -> low
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"
        assert all("work" in task.tags for task in sorted_tasks)

    def test_combined_filter_and_sort_alpha(self):
        """Test filtering tasks and then sorting the results alphabetically."""
        # Add tasks with different titles and tags
        task1 = self.service.add_task("Zebra Work Task", tags=["work"])
        task2 = self.service.add_task("Alpha Work Task", tags=["work"])
        task3 = self.service.add_task("Mango Work Task", tags=["work"])
        task4 = self.service.add_task("Alpha Home Task", tags=["home"])

        # Filter for work tasks and sort alphabetically
        filtered_tasks = self.service.filter_tasks(tags=["work"])
        sorted_tasks = self.service.sort_tasks(filtered_tasks, "alpha")

        # Should have 3 work tasks, sorted alphabetically
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].title == "Alpha Work Task"
        assert sorted_tasks[1].title == "Mango Work Task"
        assert sorted_tasks[2].title == "Zebra Work Task"
        assert all("work" in task.tags for task in sorted_tasks)

    def test_combined_filter_and_sort_created(self):
        """Test filtering tasks and then sorting the results by creation order."""
        # Add tasks in specific order
        task1 = self.service.add_task("First Work", tags=["work"])
        task2 = self.service.add_task("Second Work", tags=["work"])
        task3 = self.service.add_task("Third Home", tags=["home"])
        task4 = self.service.add_task("Fourth Work", tags=["work"])

        # Filter for work tasks and sort by creation (oldest first)
        filtered_tasks = self.service.filter_tasks(tags=["work"])
        sorted_tasks = self.service.sort_tasks(filtered_tasks, "created")

        # Should have 3 work tasks, in creation order
        assert len(sorted_tasks) == 3
        assert sorted_tasks[0].id == 1  # First task added
        assert sorted_tasks[1].id == 2  # Second task added
        assert sorted_tasks[2].id == 4  # Fourth task added

    def test_get_filtered_sorted_tasks_end_to_end(self):
        """Test the end-to-end get_filtered_sorted_tasks method."""
        # Add various tasks
        task1 = self.service.add_task("Urgent Work Task", priority="high", tags=["work", "urgent"])
        task2 = self.service.add_task("Low Priority Home Task", priority="low", tags=["home"])
        task3 = self.service.add_task("Medium Work Task", priority="medium", tags=["work"])
        task4 = self.service.add_task("High Priority Fun Task", priority="high", tags=["fun"])
        task5 = self.service.add_task("Another Work Task", priority="low", tags=["work"])

        # Update statuses
        self.service.update_task_status(1, False)  # Incomplete
        self.service.update_task_status(2, True)   # Complete
        self.service.update_task_status(3, False)  # Incomplete
        self.service.update_task_status(4, False)  # Incomplete
        self.service.update_task_status(5, False)  # Incomplete

        # Get incomplete work tasks sorted by priority
        results = self.service.get_filtered_sorted_tasks(
            status="incomplete",
            tags=["work"],
            sort_by="priority"
        )

        # Should have 3 incomplete work tasks, sorted by priority
        assert len(results) == 3
        # High priority first, then medium, then low
        assert results[0].priority == "high"  # Urgent Work Task
        assert results[1].priority == "medium"  # Medium Work Task
        assert results[2].priority == "low"  # Another Work Task
        assert all("work" in task.tags for task in results)
        assert all(task.completed is False for task in results)

    def test_combined_operations_with_search(self):
        """Test combining search with filtering and sorting."""
        # Add tasks with various attributes
        task1 = self.service.add_task("Urgent Work Project", priority="high", tags=["work", "urgent"])
        task2 = self.service.add_task("Home Maintenance", priority="medium", tags=["home"])
        task3 = self.service.add_task("Work Meeting Prep", priority="high", tags=["work"])
        task4 = self.service.add_task("Fun Weekend Plan", priority="low", tags=["fun"])

        # Update statuses
        self.service.update_task_status(1, False)  # Incomplete
        self.service.update_task_status(2, False)  # Incomplete
        self.service.update_task_status(3, True)   # Complete
        self.service.update_task_status(4, False)  # Incomplete

        # First search for tasks containing "work"
        search_results = self.service.search_tasks("work")
        assert len(search_results) == 2  # "Urgent Work Project" and "Work Meeting Prep"

        # Then filter those results for incomplete tasks
        incomplete_from_search = [task for task in search_results if not task.completed]
        assert len(incomplete_from_search) == 1  # Only "Urgent Work Project"

        # Finally sort by priority
        sorted_results = self.service.sort_tasks(incomplete_from_search, "priority")
        assert len(sorted_results) == 1
        assert sorted_results[0].id == 1  # High priority urgent work task

    def test_complex_workflow_multiple_filters_and_sort(self):
        """Test a complex workflow with multiple filters and sorting."""
        # Add a comprehensive set of tasks
        task1 = self.service.add_task("High Priority Urgent Work", priority="high", tags=["work", "urgent"])
        task2 = self.service.add_task("Low Priority Home Chores", priority="low", tags=["home"])
        task3 = self.service.add_task("Medium Priority Work Report", priority="medium", tags=["work"])
        task4 = self.service.add_task("High Priority Fun Activity", priority="high", tags=["fun"])
        task5 = self.service.add_task("Low Priority Work Follow-up", priority="low", tags=["work"])
        task6 = self.service.add_task("Medium Priority Home Project", priority="medium", tags=["home"])
        task7 = self.service.add_task("High Priority Work Deadline", priority="high", tags=["work", "urgent"])

        # Update statuses
        self.service.update_task_status(1, False)  # Incomplete
        self.service.update_task_status(2, False)  # Incomplete
        self.service.update_task_status(3, False)  # Incomplete
        self.service.update_task_status(4, True)   # Complete
        self.service.update_task_status(5, False)  # Incomplete
        self.service.update_task_status(6, True)   # Complete
        self.service.update_task_status(7, False)  # Incomplete

        # Complex query: incomplete work tasks that are urgent or high priority, sorted by priority
        # This means:
        # 1. Filter by incomplete status
        # 2. Filter by work tag
        # 3. Filter by high priority OR urgent tag
        # 4. Sort by priority

        # First, manually identify what should match:
        # - "High Priority Urgent Work": incomplete, work tag, high priority -> matches
        # - "Low Priority Home Chores": not work tag -> doesn't match
        # - "Medium Priority Work Report": not high priority, not urgent tag -> doesn't match
        # - "High Priority Fun Activity": not work tag -> doesn't match
        # - "Low Priority Work Follow-up": not high priority, not urgent tag -> doesn't match
        # - "Medium Priority Home Project": not work tag -> doesn't match
        # - "High Priority Work Deadline": incomplete, work tag, high priority -> matches

        # Filter by status and tags first
        filtered_by_status_and_tags = self.service.filter_tasks(status="incomplete", tags=["work"])
        assert len(filtered_by_status_and_tags) == 4  # Tasks 1, 3, 5, 7

        # Manually filter for high priority OR urgent tag
        final_filtered = []
        for task in filtered_by_status_and_tags:
            if task.priority == "high" or "urgent" in task.tags:
                final_filtered.append(task)

        # Tasks 1, 3, 5, 7 filtered by work tag and incomplete status
        # Task 1: high priority, urgent tag -> matches
        # Task 3: medium priority, no urgent tag -> doesn't match
        # Task 5: low priority, no urgent tag -> doesn't match
        # Task 7: high priority, urgent tag -> matches
        assert len(final_filtered) == 2  # Tasks 1 and 7

        # Sort by priority
        sorted_final = self.service.sort_tasks(final_filtered, "priority")
        assert len(sorted_final) == 2
        # Both are high priority, so order doesn't change significantly

    def test_edge_case_empty_filters_and_sorts(self):
        """Test edge cases with empty filter lists and invalid sorts."""
        # Add some tasks
        self.service.add_task("Test Task 1", priority="high", tags=["work"])
        self.service.add_task("Test Task 2", priority="low", tags=["home"])

        # Filter with no criteria (should return all)
        all_tasks = self.service.filter_tasks()
        assert len(all_tasks) == 2

        # Sort empty list
        sorted_empty = self.service.sort_tasks([], "priority")
        assert len(sorted_empty) == 0

        # Sort with invalid sort_by (should return unchanged)
        tasks = self.service.get_all_tasks()
        sorted_invalid = self.service.sort_tasks(tasks, "invalid")
        assert len(sorted_invalid) == 2