import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.task_service import TaskService
from src.cli.cli_interface import CLIInterface


def main():
    """Application entry point."""
    # Initialize services
    task_service = TaskService()
    cli_interface = CLIInterface(task_service)

    # Start the CLI
    cli_interface.run()


if __name__ == "__main__":
    main()