import pytest
import time
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError


class TestPerformance:
    """Performance tests for search, filter, and sort operations with up to 1000 tasks (T044)."""

    def setup_method(self):
        """Set up a fresh TaskService instance for each test."""
        self.service = TaskService()

    def test_performance_add_tasks_1000(self):
        """Test performance of adding 1000 tasks."""
        start_time = time.time()

        # Add 1000 tasks
        for i in range(1000):
            self.service.add_task(f"Task {i}", description=f"Description for task {i}",
                                 priority="medium", tags=[f"tag{i % 10}"])

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Adding 1000 tasks should take less than 5 seconds (generous limit)
        assert elapsed_time < 5.0, f"Adding 1000 tasks took {elapsed_time:.2f} seconds, expected < 5.0 seconds"

        # Verify all tasks were added
        all_tasks = self.service.get_all_tasks()
        assert len(all_tasks) == 1000

    def test_performance_search_1000_tasks(self):
        """Test performance of search operation with 1000 tasks."""
        # Add 1000 tasks
        for i in range(1000):
            self.service.add_task(f"Task {i}", description=f"Description for task {i}",
                                 priority="medium", tags=[f"tag{i % 10}"])

        # Search for a common keyword
        start_time = time.time()
        results = self.service.search_tasks("Task")
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Search should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Search operation with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"
        assert len(results) == 1000  # All tasks contain "Task" in title

    def test_performance_filter_1000_tasks_by_status(self):
        """Test performance of filtering by status with 1000 tasks."""
        # Add 1000 tasks, alternating status
        for i in range(1000):
            completed = i % 2 == 0  # Alternate between complete/incomplete
            self.service.add_task(f"Task {i}", priority="medium")
            self.service.update_task_status(i + 1, completed)

        # Filter for incomplete tasks (should be about 500)
        start_time = time.time()
        results = self.service.filter_tasks(status="incomplete")
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Filter should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Filter operation with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"
        assert len(results) == 500  # Half of the tasks should be incomplete

    def test_performance_filter_1000_tasks_by_priority(self):
        """Test performance of filtering by priority with 1000 tasks."""
        # Add 1000 tasks with different priorities in rotation
        priorities = ["high", "medium", "low"]
        for i in range(1000):
            priority = priorities[i % 3]
            self.service.add_task(f"Task {i}", priority=priority)

        # Filter for high priority tasks (should be about 333)
        start_time = time.time()
        results = self.service.filter_tasks(priority="high")
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Filter should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Priority filter with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"
        assert len(results) == 334 or len(results) == 333  # About 1/3 of 1000

    def test_performance_filter_1000_tasks_by_tags(self):
        """Test performance of filtering by tags with 1000 tasks."""
        # Add 1000 tasks with different tags
        for i in range(1000):
            tags = [f"tag{i % 5}", f"category{i % 3}"]  # Each task gets 2 tags
            self.service.add_task(f"Task {i}", tags=tags)

        # Filter for tasks with a specific tag (should be about 200)
        start_time = time.time()
        results = self.service.filter_tasks(tags=["tag0"])
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Filter should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Tag filter with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"
        # About 1 in 5 tasks should have tag0 (every 5th task: 0, 5, 10, ...)
        expected_count = 1000 // 5  # 200 tasks
        assert len(results) == expected_count

    def test_performance_sort_1000_tasks_by_priority(self):
        """Test performance of sorting 1000 tasks by priority."""
        # Add 1000 tasks with different priorities in rotation
        priorities = ["high", "medium", "low"] * 334  # More than 1000
        for i in range(1000):
            priority = priorities[i]
            self.service.add_task(f"Task {i}", priority=priority)

        # Sort the tasks
        tasks = self.service.get_all_tasks()
        start_time = time.time()
        sorted_tasks = self.service.sort_tasks(tasks, "priority")
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Sort should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Sort by priority with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"

        # Verify the sort worked: high priority tasks should come first
        high_priority_count = sum(1 for task in sorted_tasks if task.priority == "high")
        medium_priority_count = sum(1 for task in sorted_tasks if task.priority == "medium")
        low_priority_count = sum(1 for task in sorted_tasks if task.priority == "low")

        # Check that the first high_priority_count tasks are high priority
        for i in range(high_priority_count):
            assert sorted_tasks[i].priority == "high"

        # Check that the next medium_priority_count tasks are medium priority
        for i in range(high_priority_count, high_priority_count + medium_priority_count):
            assert sorted_tasks[i].priority == "medium"

    def test_performance_sort_1000_tasks_by_alpha(self):
        """Test performance of sorting 1000 tasks alphabetically."""
        # Add 1000 tasks with titles that will sort differently than creation order
        for i in range(1000):
            # Use titles that will sort differently than numeric order
            title = f"Task {1000 - i:04d}"  # Reverse order: Task 1000, Task 0999, ..., Task 0001
            self.service.add_task(title)

        # Sort the tasks alphabetically
        tasks = self.service.get_all_tasks()
        start_time = time.time()
        sorted_tasks = self.service.sort_tasks(tasks, "alpha")
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Sort should take less than 1 second for 1000 tasks
        assert elapsed_time < 1.0, f"Sort alphabetically with 1000 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"

        # Verify the sort worked: tasks should be in alphabetical order
        for i in range(len(sorted_tasks) - 1):
            assert sorted_tasks[i].title <= sorted_tasks[i + 1].title

    def test_performance_combined_filter_and_sort_500_tasks(self):
        """Test performance of combined filtering and sorting with 500 tasks."""
        # Add 500 tasks with various attributes
        for i in range(500):
            priority = ["high", "medium", "low"][i % 3]
            tags = [f"tag{i % 10}"]
            completed = i % 2 == 0  # Even i values: completed=True, odd i values: completed=False
            self.service.add_task(f"Task {i}", priority=priority, tags=tags)
            self.service.update_task_status(i + 1, completed)

        # Filter and sort: incomplete tasks with specific tag, sorted by priority
        # Tasks with tag0: i=0,10,20,...,490 (every 10th task starting from 0) = 50 tasks total
        # For these tasks, i is even, so completed=True for all of them
        # So there should be 0 incomplete tasks with tag0
        start_time = time.time()
        results = self.service.get_filtered_sorted_tasks(
            status="incomplete",
            tags=["tag0"],
            sort_by="priority"
        )
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Combined operation should take less than 1 second for 500 tasks
        assert elapsed_time < 1.0, f"Combined filter and sort with 500 tasks took {elapsed_time:.2f} seconds, expected < 1.0 seconds"

        # Verify results: should have 0 incomplete tasks with tag0 (since all tasks with tag0 are completed)
        assert len(results) == 0  # All tasks with tag0 are completed (since their i values are even)

        # Let's try filtering for completed tasks with tag0 instead to verify the functionality works
        results_completed = self.service.get_filtered_sorted_tasks(
            status="complete",
            tags=["tag0"],
            sort_by="priority"
        )

        # Should have 50 completed tasks with tag0
        expected_count = 50  # Tasks with i=0,10,20,...,490 (every 10th task) = 50 tasks
        assert len(results_completed) == expected_count

        # Check that they're sorted by priority (high, medium, low)
        for i in range(len(results_completed) - 1):
            priority_order = {"high": 0, "medium": 1, "low": 2}
            current_priority = priority_order[results_completed[i].priority]
            next_priority = priority_order[results_completed[i + 1].priority]
            assert current_priority <= next_priority

    def test_performance_search_filter_sort_500_tasks(self):
        """Test performance of search, filter, and sort operations in sequence with 500 tasks."""
        # Add 500 tasks with various attributes
        for i in range(500):
            priority = ["high", "medium", "low"][i % 3]
            tags = [f"tag{i % 5}", f"category{i % 7}"]
            completed = i % 2 == 0
            title = f"Searchable Task {i} with keyword"
            self.service.add_task(title, description=f"Description {i} contains keyword",
                                 priority=priority, tags=tags)
            self.service.update_task_status(i + 1, completed)

        start_time = time.time()

        # Step 1: Search for keyword
        search_results = self.service.search_tasks("keyword")

        # Step 2: Filter incomplete high-priority tasks
        filtered_results = [task for task in search_results
                           if task.completed is False and task.priority == "high"]

        # Step 3: Sort by creation order
        final_results = self.service.sort_tasks(filtered_results, "created")

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Combined operations should take less than 2 seconds for 500 tasks
        assert elapsed_time < 2.0, f"Search-filter-sort sequence with 500 tasks took {elapsed_time:.2f} seconds, expected < 2.0 seconds"

        # Verify results: should have incomplete high-priority tasks containing "keyword", sorted by creation
        assert len(final_results) > 0  # Should have some results
        for task in final_results:
            assert task.completed is False
            assert task.priority == "high"
            assert "keyword" in task.title.lower() or "keyword" in (task.description or "").lower()

    def test_performance_edge_case_empty_operations(self):
        """Test performance with empty operations (should be very fast)."""
        start_time = time.time()

        # Test empty search
        empty_search = self.service.search_tasks("nonexistent")

        # Test empty filter
        empty_filter = self.service.filter_tasks(status="complete", priority="high")

        # Test empty sort
        empty_sort = self.service.sort_tasks([], "priority")

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Empty operations should be very fast (much less than 0.1 seconds)
        assert elapsed_time < 0.1, f"Empty operations took {elapsed_time:.2f} seconds, expected < 0.1 seconds"

        assert len(empty_search) == 0
        assert len(empty_filter) == 0
        assert len(empty_sort) == 0