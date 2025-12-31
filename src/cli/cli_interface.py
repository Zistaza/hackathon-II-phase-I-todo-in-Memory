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
            'list': self._handle_list,
            'search': self._handle_search,
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
            print("Usage: add <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...]")
            return

        # Parse arguments with potential flags
        title, description, priority, tags = self._parse_add_args(args)

        try:
            task = self.task_service.add_task(title, description, priority, tags)
            print(f"{GREEN}Task added successfully!{RESET} ID: {task.id}, Title: {task.title}")
        except TaskValidationError as e:
            print(f"{RED}Error adding task:{RESET} {str(e)}")

    def _parse_add_args(self, args: str):
        """Parse add command arguments including --priority and --tags flags."""
        import shlex

        # Split args to handle flags
        parts = shlex.split(args)
        title = ""
        description = None
        priority = "medium"  # default
        tags = []

        i = 0
        while i < len(parts):
            part = parts[i]

            if part == '--priority' and i + 1 < len(parts):
                priority = parts[i + 1]
                i += 2
            elif part == '--tags' and i + 1 < len(parts):
                tags = [tag.strip() for tag in parts[i + 1].split(',') if tag.strip()]
                i += 2
            else:
                # If it's the first non-flag argument, treat as title
                if not title:
                    title = part
                    # Everything else becomes description
                    if i + 1 < len(parts):
                        description = ' '.join(parts[i + 1:])
                        break
                else:
                    # This shouldn't happen in normal usage, but just in case
                    if not description:
                        description = part
                    else:
                        description += " " + part
                i += 1
        else:
            # If we didn't encounter any flags and title is still empty, use the first part as title
            if not title and parts:
                title = parts[0]
                if len(parts) > 1:
                    description = ' '.join(parts[1:])

        return title, description, priority, tags

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
            print("Usage: update <id> <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...]")
            return

        # Parse arguments with potential flags
        try:
            task_id, new_title, new_description, new_priority, new_tags = self._parse_update_args(args)
        except ValueError as e:
            print(f"{RED}Error parsing arguments:{RESET} {str(e)}")
            return

        try:
            # Prepare update parameters
            update_kwargs = {}
            if new_title is not None:
                update_kwargs['title'] = new_title
            if new_description is not None:
                update_kwargs['description'] = new_description
            if new_priority is not None:
                update_kwargs['priority'] = new_priority
            if new_tags is not None:
                update_kwargs['tags'] = new_tags

            task = self.task_service.update_task(task_id, **update_kwargs)
            print(f"{GREEN}Task updated successfully!{RESET} ID: {task.id}, Title: {task.title}")
        except (TaskNotFoundError, TaskValidationError) as e:
            print(f"{RED}Error updating task:{RESET} {str(e)}")

    def _parse_update_args(self, args: str):
        """Parse update command arguments including --priority and --tags flags."""
        import shlex

        # Split args to handle flags
        parts = shlex.split(args)
        if not parts:
            raise ValueError("No arguments provided")

        # First argument should be the task ID
        task_id = int(parts[0])
        new_title = None
        new_description = None
        new_priority = None
        new_tags = None

        i = 1  # Start after task ID
        while i < len(parts):
            part = parts[i]

            if part == '--priority' and i + 1 < len(parts):
                new_priority = parts[i + 1]
                i += 2
            elif part == '--tags' and i + 1 < len(parts):
                new_tags = [tag.strip() for tag in parts[i + 1].split(',') if tag.strip()]
                i += 2
            else:
                # If we haven't set the title yet, this is the new title
                if new_title is None:
                    new_title = part
                    # Everything after title becomes description if there are more parts
                    if i + 1 < len(parts):
                        new_description = ' '.join(parts[i + 1:])
                        break
                else:
                    # This shouldn't happen in normal usage, but just in case
                    if new_description is None:
                        new_description = part
                    else:
                        new_description += " " + part
                i += 1

        return task_id, new_title, new_description, new_priority, new_tags

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

    def _handle_list(self, args: str):
        """Handle the list command with optional filters and sorting."""
        # Parse arguments for filters and sorting
        status, priority, tags, sort_by = self._parse_list_args(args)

        try:
            tasks = self.task_service.get_filtered_sorted_tasks(
                status=status, priority=priority, tags=tags, sort_by=sort_by
            )

            if not tasks:
                print(f"{YELLOW}No tasks found matching the criteria.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}Filtered Tasks:{RESET}")
            for task in tasks:
                self._print_task_box(task)
        except TaskValidationError as e:
            print(f"{RED}Error listing tasks:{RESET} {str(e)}")

    def _parse_list_args(self, args: str):
        """Parse list command arguments for filters and sorting."""
        import shlex

        if not args.strip():
            return None, None, None, 'created'  # Default: no filters, sort by creation

        parts = shlex.split(args)
        status = None
        priority = None
        tags = None
        sort_by = 'created'  # Default sort

        i = 0
        while i < len(parts):
            part = parts[i]

            if part == '--status' and i + 1 < len(parts):
                status = parts[i + 1]
                i += 2
            elif part == '--priority' and i + 1 < len(parts):
                priority = parts[i + 1]
                i += 2
            elif part == '--tag' and i + 1 < len(parts):
                tags = [parts[i + 1]]  # Single tag for --tag flag
                i += 2
            elif part == '--sort' and i + 1 < len(parts):
                sort_by = parts[i + 1]
                i += 2
            else:
                # Unrecognized argument
                print(f"{RED}Unknown argument: {part}{RESET}")
                i += 1

        return status, priority, tags, sort_by

    def _handle_search(self, args: str):
        """Handle the search command."""
        if not args.strip():
            print("Usage: search <keyword> [--sort priority|alpha|created]")
            return

        import shlex
        parts = shlex.split(args)
        keyword = None
        sort_by = 'created'  # Default sort

        i = 0
        while i < len(parts):
            part = parts[i]

            if part == '--sort' and i + 1 < len(parts):
                sort_by = parts[i + 1]
                i += 2
            else:
                # First non-flag argument is the keyword
                if keyword is None:
                    keyword = part
                i += 1

        if not keyword:
            print("Usage: search <keyword> [--sort priority|alpha|created]")
            return

        try:
            tasks = self.task_service.search_tasks(keyword)

            # Sort the results if needed
            if sort_by != 'created' and tasks:
                tasks = self.task_service.sort_tasks(tasks, sort_by)

            if not tasks:
                print(f"{YELLOW}No tasks found matching '{keyword}'.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}Search Results for '{keyword}':{RESET}")
            for task in tasks:
                self._print_task_box(task)
        except TaskValidationError as e:
            print(f"{RED}Error searching tasks:{RESET} {str(e)}")

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
        print(f"  add <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...]     - Add a new task")
        print(f"  view                          - View all tasks")
        print(f"  update <id> <title> [desc] [--priority high|medium|low] [--tags tag1,tag2,...]  - Update task details")
        print(f"  delete <id>                   - Delete a task")
        print(f"  complete <id>                 - Mark task as complete")
        print(f"  incomplete <id>               - Mark task as incomplete")
        print(f"  list [--status complete|incomplete] [--priority high|medium|low] [--tag tag] [--sort priority|alpha|created] - List tasks with filters and sorting")
        print(f"  search <keyword> [--sort priority|alpha|created] - Search tasks by keyword")
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
        priority_display = f"[{task.priority.upper()}]"
        tags_display = " ".join([f"#{tag}" for tag in task.tags]) if task.tags else ""
        task_info = f"ID: {task.id} {status} {priority_display} {task.title}"
        if tags_display:
            task_info += f" {tags_display}"

        print(f"{BOLD}{CYAN}+{'-'*60}+{RESET}")
        print(f"{BOLD}{CYAN}| {task_info:<58} |{RESET}")
        if task.description:
            desc_lines = self._split_text(task.description, 58)
            for line in desc_lines:
                print(f"{BOLD}{CYAN}| {line:<58} |{RESET}")
        print(f"{BOLD}{CYAN}+{'-'*60}+{RESET}")

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
