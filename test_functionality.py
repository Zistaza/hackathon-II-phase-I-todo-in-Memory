#!/usr/bin/env python3
"""
Basic functionality test for the Todo CLI application
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.task import Task
from src.services.task_service import TaskService
from src.exceptions import TaskNotFoundError, TaskValidationError

def test_task_model():
    """Test Task model functionality"""
    print("Testing Task model...")

    # Test creating a valid task
    task = Task(id=1, title="Test task", description="Test description")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False
    print("✓ Task creation works")

    # Test validation - empty title
    try:
        Task(id=2, title="", description="Test")
        assert False, "Empty title should raise ValueError"
    except ValueError as e:
        assert "Task title cannot be empty" in str(e)
        print("✓ Empty title validation works")

    # Test validation - long title
    try:
        Task(id=3, title="a" * 101, description="Test")
        assert False, "Long title should raise ValueError"
    except ValueError as e:
        assert "100 character limit" in str(e)
        print("✓ Title length validation works")

    # Test validation - long description
    try:
        Task(id=4, title="Test", description="a" * 501)
        assert False, "Long description should raise ValueError"
    except ValueError as e:
        assert "500 character limit" in str(e)
        print("✓ Description length validation works")

    # Test status methods
    task.mark_complete()
    assert task.completed == True
    print("✓ Mark complete works")

    task.mark_incomplete()
    assert task.completed == False
    print("✓ Mark incomplete works")

    # Test update methods
    task.update_title("Updated title")
    assert task.title == "Updated title"
    print("✓ Update title works")

    task.update_description("Updated description")
    assert task.description == "Updated description"
    print("✓ Update description works")

    print("All Task model tests passed!\n")

def test_task_service():
    """Test TaskService functionality"""
    print("Testing TaskService...")

    service = TaskService()

    # Test adding a task
    task = service.add_task("Test task", "Test description")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False
    print("✓ Add task works")

    # Test adding another task with sequential ID
    task2 = service.add_task("Second task")
    assert task2.id == 2
    print("✓ Sequential ID generation works")

    # Test getting all tasks
    tasks = service.get_all_tasks()
    assert len(tasks) == 2
    print("✓ Get all tasks works")

    # Test getting task by ID
    retrieved_task = service.get_task_by_id(1)
    assert retrieved_task.id == 1
    assert retrieved_task.title == "Test task"
    print("✓ Get task by ID works")

    # Test updating task
    updated_task = service.update_task(1, "Updated task", "Updated description")
    assert updated_task.title == "Updated task"
    assert updated_task.description == "Updated description"
    print("✓ Update task works")

    # Test updating status
    completed_task = service.update_task_status(1, True)
    assert completed_task.completed == True
    print("✓ Update task status works")

    # Test deleting task
    result = service.delete_task(2)
    assert result == True
    tasks_after_delete = service.get_all_tasks()
    assert len(tasks_after_delete) == 1
    print("✓ Delete task works")

    # Test error handling - non-existent task
    try:
        service.get_task_by_id(999)
        assert False, "Should raise TaskNotFoundError"
    except TaskNotFoundError:
        print("✓ Non-existent task error handling works")

    print("All TaskService tests passed!\n")

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("Testing edge cases...")

    service = TaskService()

    # Test validation in service layer
    try:
        service.add_task("")  # Empty title
        assert False, "Should raise TaskValidationError"
    except TaskValidationError:
        print("✓ Service layer validation works")

    # Add a task to test update validation
    task = service.add_task("Test task")

    try:
        service.update_task(task.id, "")  # Empty title update
        assert False, "Should raise TaskValidationError"
    except TaskValidationError:
        print("✓ Service layer update validation works")

    # Test non-existent task operations
    try:
        service.update_task(999, "New title")
        assert False, "Should raise TaskNotFoundError"
    except TaskNotFoundError:
        print("✓ Update non-existent task error handling works")

    try:
        service.delete_task(999)
        assert False, "Should raise TaskNotFoundError"
    except TaskNotFoundError:
        print("✓ Delete non-existent task error handling works")

    try:
        service.update_task_status(999, True)
        assert False, "Should raise TaskNotFoundError"
    except TaskNotFoundError:
        print("✓ Update status non-existent task error handling works")

    print("All edge case tests passed!\n")

if __name__ == "__main__":
    print("Running functionality tests...\n")

    test_task_model()
    test_task_service()
    test_edge_cases()

    print("🎉 All tests passed! The application is working correctly.")