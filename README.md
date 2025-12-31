# In-Memory Todo CLI Application

A simple command-line interface application for managing todo tasks in memory. This application provides core functionality to add, view, update, delete, and mark tasks as complete/incomplete.

## Features

- Add tasks with unique IDs, titles, and optional descriptions
- View all tasks with status indicators ([✓] for complete, [ ] for incomplete)
- Update task details by ID
- Delete tasks by ID
- Mark tasks as complete or incomplete by ID
- In-memory storage (no persistent storage)
- Input validation with character limits (100 chars for title, 500 chars for description)
- Error handling with clear user feedback
- Sequential ID generation starting from 1

## Commands

- `add <title> [description]` - Add a new task
- `view` - View all tasks with status indicators
- `update <id> <title> [description]` - Update task details
- `delete <id>` - Delete a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete
- `help` - Show available commands
- `quit` or `exit` - Exit the application

## Requirements

- Python >= 3.13

## Usage

### Running the Application

Run the application using Python:

```bash
python3 -m src.main
```

### Example Usage

```
Welcome to the In-Memory Todo CLI Application!
Type 'help' for available commands or 'quit' to exit.

> add Buy groceries Shopping for dinner ingredients
Task added successfully! ID: 1, Title: Buy groceries

> add Clean the house
Task added successfully! ID: 2, Title: Clean the house

> view

Your Tasks:
------------------------------------------------------------
ID: 1 [ ] Buy groceries
     Description: Shopping for dinner ingredients
ID: 2 [ ] Clean the house
------------------------------------------------------------

> complete 1
Task 1 marked as complete!

> update 2 Updated cleaning task Thorough cleaning including vacuuming
Task updated successfully! ID: 2, Title: Updated cleaning task

> view

Your Tasks:
------------------------------------------------------------
ID: 1 [✓] Buy groceries
     Description: Shopping for dinner ingredients
ID: 2 [ ] Updated cleaning task
     Description: Thorough cleaning including vacuuming
------------------------------------------------------------

> quit
Goodbye!
```

## Error Handling

The application provides clear error messages for various scenarios:
- Attempting to operate on non-existent task IDs
- Providing empty titles (must be non-empty)
- Exceeding character limits (100 for title, 500 for description)
- Providing invalid task IDs (non-numeric values)

## Project Structure

- `src/models/task.py` - Task data model with validation
- `src/services/task_service.py` - Business logic and in-memory storage
- `src/cli/cli_interface.py` - Command parsing and user interaction
- `src/main.py` - Application entry point
- `src/exceptions.py` - Custom exception definitions
- `tests/` - Unit and integration tests