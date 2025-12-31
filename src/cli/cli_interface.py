import sys
from typing import List, Optional
from src.services.task_service import TaskService
from src.models.task import Task
from src.exceptions import TaskNotFoundError, TaskValidationError

# ------------------- Colors / Styles ------------------- #
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

# ------------------- CLI Interface ------------------- #
class CLIInterface:
    """Professional CLI interface for In-Memory Todo App"""

    def __init__(self, task_service: TaskService):
        self.task_service = task_service
        self.commands = {
            'add': self._handle_add,
            'view': self._handle_view,
            'update': self._handle_update,
            'delete': self._handle_delete,
            'complete': self._handle_complete,
            'incomplete': self._handle_incomplete,
            'stats': self._handle_stats,
            'help': self._handle_help,
            'quit': self._handle_quit,
            'exit': self._handle_quit
        }

    def run(self):
        """Start CLI loop"""
        self._print_banner()
        while True:
            try:
                user_input = input(f"\n{CYAN}> {RESET}").strip()
                if not user_input:
                    continue

                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if command in self.commands:
                    result = self.commands[command](args)
                    if result is False:
                        break
                else:
                    print(f"{RED}Unknown command:{RESET} {command}. Type 'help' for commands.")

            except (KeyboardInterrupt, EOFError):
                print(f"\n{YELLOW}Goodbye!{RESET}")
                sys.exit(0)
            except Exception as e:
                print(f"{RED}Error:{RESET} {str(e)}")

    # ------------------- Banner ------------------- #
    def _print_banner(self):
        print(f"{BOLD}{MAGENTA}=============================={RESET}")
        print(f"{BOLD}{MAGENTA}   In-Memory Todo CLI App   {RESET}")
        print(f"{BOLD}{MAGENTA}=============================={RESET}")
        print(f"Type '{BOLD}help{RESET}' to view commands\n")

    # ------------------- Command Handlers ------------------- #
    def _handle_add(self, args: str):
        if not args:
            print("Usage: add <title> [description]")
            return

        parts = args.split(maxsplit=1)
        title = parts[0]
        description = parts[1] if len(parts) > 1 else None

        try:
            task = self.task_service.add_task(title, description)
            print(f"{GREEN}Task added successfully!{RESET} ID: {task.id}, Title: {task.title}")
        except TaskValidationError as e:
            print(f"{RED}Error adding task:{RESET} {str(e)}")

    def _handle_view(self, args: str):
        tasks = self.task_service.get_all_tasks()
        if not tasks:
            print(f"{YELLOW}No tasks found.{RESET}")
            return

        print(f"\n{BOLD}{CYAN}Your Tasks:{RESET}")
        for task in tasks:
            self._print_task_box(task)

    def _handle_update(self, args: str):
        if not args:
            print("Usage: update <id> <title> [description]")
            return

        parts = args.split(maxsplit=2)
        if len(parts) < 2:
            print("Usage: update <id> <title> [description]")
            return

        try:
            task_id = int(parts[0])
            new_title = parts[1]
            new_description = parts[2] if len(parts) > 2 else None

            task = self.task_service.update_task(task_id, new_title, new_description)
            print(f"{GREEN}Task updated successfully!{RESET} ID: {task.id}, Title: {task.title}")
        except ValueError:
            print(f"{RED}Error:{RESET} Task ID must be a number.")
        except (TaskNotFoundError, TaskValidationError) as e:
            print(f"{RED}Error updating task:{RESET} {str(e)}")

    def _handle_delete(self, args: str):
        if not args:
            print("Usage: delete <id>")
            return

        try:
            task_id = int(args.strip())
            self.task_service.delete_task(task_id)
            print(f"{GREEN}Task {task_id} deleted successfully!{RESET}")
        except ValueError:
            print(f"{RED}Error:{RESET} Task ID must be a number.")
        except TaskNotFoundError as e:
            print(f"{RED}Error deleting task:{RESET} {str(e)}")

    def _handle_complete(self, args: str):
        if not args:
            print("Usage: complete <id>")
            return

        try:
            task_id = int(args.strip())
            task = self.task_service.update_task_status(task_id, True)
            print(f"{GREEN}Task {task.id} marked as complete!{RESET}")
        except ValueError:
            print(f"{RED}Error:{RESET} Task ID must be a number.")
        except TaskNotFoundError as e:
            print(f"{RED}Error marking task complete:{RESET} {str(e)}")

    def _handle_incomplete(self, args: str):
        if not args:
            print("Usage: incomplete <id>")
            return

        try:
            task_id = int(args.strip())
            task = self.task_service.update_task_status(task_id, False)
            print(f"{YELLOW}Task {task.id} marked as incomplete!{RESET}")
        except ValueError:
            print(f"{RED}Error:{RESET} Task ID must be a number.")
        except TaskNotFoundError as e:
            print(f"{RED}Error marking task incomplete:{RESET} {str(e)}")

    def _handle_help(self, args: str):
        print(f"\n{BOLD}{CYAN}Available commands:{RESET}")
        print(f"  add <title> [description]     - Add a new task")
        print(f"  view                          - View all tasks")
        print(f"  update <id> <title> [desc]    - Update task details")
        print(f"  delete <id>                   - Delete a task")
        print(f"  complete <id>                 - Mark task as complete")
        print(f"  incomplete <id>               - Mark task as incomplete")
        print(f"  stats                         - Show task statistics chart")
        print(f"  help                          - Show this help")
        print(f"  quit/exit                     - Exit the application")

    def _handle_quit(self, args: str):
        print(f"{YELLOW}Goodbye!{RESET}")
        return False

    # ------------------- Stats / Charts ------------------- #
    def _handle_stats(self, args: str):
        tasks = self.task_service.get_all_tasks()
        total = len(tasks)
        completed = sum(t.completed for t in tasks)
        pending = total - completed

        print(f"\n{BOLD}Task Statistics:{RESET}")
        print(f"Total Tasks     : {total}")
        print(f"{GREEN}Completed Tasks : {completed}{RESET}")
        print(f"{RED}Pending Tasks   : {pending}{RESET}")

        # ASCII mini bar chart
        bar_length = 30
        completed_len = int((completed / total) * bar_length) if total else 0
        pending_len = bar_length - completed_len
        bar = f"{GREEN}{'█'*completed_len}{RED}{'█'*pending_len}{RESET}"
        print(f"[{bar}]")

    # ------------------- Task Box ------------------- #
    def _print_task_box(self, task: Task):
        status = f"{GREEN}[✓]{RESET}" if task.completed else f"{RED}[ ]{RESET}"
        print(f"{BOLD}{CYAN}+{'-'*50}+{RESET}")
        print(f"{BOLD}{CYAN}| ID: {task.id} {status} Title: {task.title:<30}|{RESET}")
        if task.description:
            desc_lines = self._split_text(task.description, 48)
            for line in desc_lines:
                print(f"{BOLD}{CYAN}| {line:<48} |{RESET}")
        print(f"{BOLD}{CYAN}+{'-'*50}+{RESET}")

    def _split_text(self, text: str, width: int) -> List[str]:
        """Split text into lines of max width for box display"""
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= width:
                line += (" " if line else "") + word
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines
