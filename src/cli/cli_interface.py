import sys
from typing import List, Optional
from datetime import datetime
from src.services.task_service import TaskService
from src.models.task import Task, RecurrencePattern
from src.services.recurrence_service import RecurrenceService
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
            'recurring': self._handle_recurring,
            'reminders': self._handle_reminders,
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
            print("Usage: add <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...] [--due YYYY-MM-DD] [--remind YYYY-MM-DD HH:MM] [--recur daily|weekly|every N days|weeks]")
            return

        # Parse arguments with potential flags
        try:
            title, description, priority, tags, due_date, reminder_time, recurrence_pattern = self._parse_add_args(args)
        except ValueError as e:
            print(f"{RED}Error parsing arguments:{RESET} {str(e)}")
            return

        try:
            task = self.task_service.add_task(
                title, description, priority, tags,
                due_date=due_date,
                reminder_time=reminder_time,
                recurrence_pattern=recurrence_pattern
            )
            print(f"{GREEN}Task added successfully!{RESET} ID: {task.id}, Title: {task.title}")

            # If it's a recurring task, calculate when the next occurrence should be
            if recurrence_pattern:
                from src.services.recurrence_service import RecurrenceService
                from datetime import datetime
                recurrence_pattern.next_occurrence = RecurrenceService.calculate_next_occurrence(
                    recurrence_pattern, datetime.now()
                )
                # Update the task's recurrence pattern with the next occurrence
                task.recurrence_pattern = recurrence_pattern
        except TaskValidationError as e:
            print(f"{RED}Error adding task:{RESET} {str(e)}")

    def _parse_add_args(self, args: str):
        """Parse add command arguments including --priority, --tags, --due, --remind, --recur, and --recur-days flags."""
        import shlex

        # Split args to handle flags
        parts = shlex.split(args)
        title = ""
        description = None
        priority = "medium"  # default
        tags = []
        due_date = None
        reminder_time = None
        recurrence_pattern = None
        days_of_week = None  # For --recur-days

        i = 0
        while i < len(parts):
            part = parts[i]

            if part == '--priority' and i + 1 < len(parts):
                priority = parts[i + 1]
                i += 2
            elif part == '--tags' and i + 1 < len(parts):
                tags = [tag.strip() for tag in parts[i + 1].split(',') if tag.strip()]
                i += 2
            elif part == '--due' and i + 1 < len(parts):
                from src.services.datetime_utils import parse_datetime_string
                due_date = parse_datetime_string(parts[i + 1])
                if due_date is None:
                    raise ValueError(f"Invalid due date format: {parts[i + 1]}. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")
                i += 2
            elif part == '--remind' and i + 1 < len(parts):
                from src.services.datetime_utils import parse_datetime_string
                reminder_time = parse_datetime_string(parts[i + 1])
                if reminder_time is None:
                    raise ValueError(f"Invalid reminder time format: {parts[i + 1]}. Use YYYY-MM-DD HH:MM or HH:MM")
                i += 2
            elif part in ['--recur', '-r'] and i + 1 < len(parts):
                # Parse recurrence pattern
                recur_pattern = parts[i + 1]
                recurrence_pattern = self._parse_recurrence_pattern(recur_pattern)
                if recurrence_pattern is None:
                    raise ValueError(f"Invalid recurrence pattern: {parts[i + 1]}")
                i += 2
            elif part in ['--recur-days', '-rd'] and i + 1 < len(parts):
                # Parse days of week for weekly recurrence
                days_str = parts[i + 1].lower()
                days_of_week = self._parse_days_of_week(days_str)
                if days_of_week is None:
                    raise ValueError(f"Invalid days of week format: {parts[i + 1]}")
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

        # If we have both recurrence pattern and days of week, update the pattern
        if recurrence_pattern and days_of_week:
            # For weekly patterns, set the days of week
            if recurrence_pattern.type == "weekly":
                recurrence_pattern.days_of_week = days_of_week

        return title, description, priority, tags, due_date, reminder_time, recurrence_pattern

    def _parse_days_of_week(self, days_str: str):
        """Parse days of week string into a list of integers (0=Monday, 6=Sunday)."""
        day_map = {
            'mon': 0, 'monday': 0,
            'tue': 1, 'tuesday': 1,
            'wed': 2, 'wednesday': 2,
            'thu': 3, 'thursday': 3,
            'fri': 4, 'friday': 4,
            'sat': 5, 'saturday': 5,
            'sun': 6, 'sunday': 6
        }

        days = []
        day_parts = [d.strip() for d in days_str.split(',')]
        for day_part in day_parts:
            if day_part in day_map:
                days.append(day_map[day_part])
            else:
                # Try to see if it's a single character abbreviation
                for abbr, num in day_map.items():
                    if abbr.startswith(day_part.lower()):
                        days.append(num)
                        break
                else:
                    return None  # Invalid day

        return sorted(set(days))  # Return unique sorted days

    def _parse_recurrence_pattern(self, pattern_str: str):
        """Parse a recurrence pattern string into a RecurrencePattern object."""
        pattern_str = pattern_str.lower().strip()

        if pattern_str == "daily":
            return RecurrenceService.create_recurrence_pattern("daily")
        elif pattern_str == "weekly":
            return RecurrenceService.create_recurrence_pattern("weekly")
        elif pattern_str.startswith("every"):
            # Parse patterns like "every 2 days" or "every 3 weeks"
            parts = pattern_str.split()
            if len(parts) >= 3 and parts[1].isdigit():
                interval = int(parts[1])
                unit = parts[2]
                if unit.startswith("day"):
                    return RecurrenceService.create_recurrence_pattern("custom", interval=interval)
                elif unit.startswith("week"):
                    return RecurrenceService.create_recurrence_pattern("custom", interval=interval*7)
            else:
                # Handle just "every N" - assume days
                parts = pattern_str.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    interval = int(parts[1])
                    return RecurrenceService.create_recurrence_pattern("custom", interval=interval)
        return None

    def _handle_view(self, args: str):
        """Handle the view command with optional filters like --upcoming, --overdue, --recurring, etc."""
        import shlex
        parts = shlex.split(args) if args.strip() else []

        # Check for special options
        if '--upcoming' in parts or '-u' in parts:
            tasks = self.task_service.get_upcoming_tasks()
            if not tasks:
                print(f"{YELLOW}No upcoming tasks found.{RESET}")
                return
            print(f"\n{BOLD}{CYAN}Upcoming Tasks (sorted by due date):{RESET}")
        elif '--overdue' in parts or '-o' in parts:
            tasks = self.task_service.get_overdue_tasks()
            if not tasks:
                print(f"{YELLOW}No overdue tasks found.{RESET}")
                return
            print(f"\n{BOLD}{CYAN}Overdue Tasks:{RESET}")
        elif '--recurring' in parts or '-r' in parts:
            from src.services.task_storage import recurrence_templates
            tasks = list(recurrence_templates.values())
            if not tasks:
                print(f"{YELLOW}No recurring tasks found.{RESET}")
                return
            print(f"\n{BOLD}{CYAN}Recurring Tasks:{RESET}")
        elif '--due-before' in parts or '--due-after' in parts:
            # Parse due date filters
            due_before = None
            due_after = None
            i = 0
            while i < len(parts):
                part = parts[i]
                if part == '--due-before' and i + 1 < len(parts):
                    from src.services.datetime_utils import parse_datetime_string
                    due_before = parse_datetime_string(parts[i + 1])
                    i += 2
                elif part == '--due-after' and i + 1 < len(parts):
                    from src.services.datetime_utils import parse_datetime_string
                    due_after = parse_datetime_string(parts[i + 1])
                    i += 2
                else:
                    i += 1

            # Get all tasks and filter by due date
            all_tasks = self.task_service.get_all_tasks()
            tasks = []
            for task in all_tasks:
                if task.due_date:
                    include = True
                    if due_before and task.due_date > due_before:
                        include = False
                    if due_after and task.due_date < due_after:
                        include = False
                    if include:
                        tasks.append(task)

            if not tasks:
                print(f"{YELLOW}No tasks found matching due date criteria.{RESET}")
                return
            print(f"\n{BOLD}{CYAN}Tasks with due dates matching criteria:{RESET}")
        else:
            # Default view - all tasks
            tasks = self.task_service.get_all_tasks()
            if not tasks:
                print(f"{YELLOW}No tasks found.{RESET}")
                return
            print(f"\n{BOLD}{CYAN}Your Tasks:{RESET}")

        for task in tasks:
            self._print_task_box(task)

    def _handle_update(self, args: str):
        if not args:
            print("Usage: update <id> <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...] [--due YYYY-MM-DD] [--remind YYYY-MM-DD HH:MM] [--cancel-recur] [--update-recur daily|weekly|every N days]")
            return

        # Parse arguments with potential flags
        try:
            task_id, new_title, new_description, new_priority, new_tags, new_due_date, new_reminder_time, cancel_recurrence, update_recurrence = self._parse_update_args(args)
        except ValueError as e:
            print(f"{RED}Error parsing arguments:{RESET} {str(e)}")
            return

        try:
            # Handle recurrence operations first
            if cancel_recurrence:
                success = self.task_service.cancel_recurrence_for_task(task_id)
                if success:
                    print(f"{GREEN}Recurrence pattern canceled for task {task_id}.{RESET}")
                else:
                    print(f"{RED}Failed to cancel recurrence for task {task_id}.{RESET}")

            if update_recurrence:
                success = self.task_service.update_recurrence_for_task(task_id, update_recurrence)
                if success:
                    print(f"{GREEN}Recurrence pattern updated for task {task_id}.{RESET}")
                else:
                    print(f"{RED}Failed to update recurrence for task {task_id}.{RESET}")

            # Prepare update parameters for other fields
            update_kwargs = {}
            if new_title is not None:
                update_kwargs['title'] = new_title
            if new_description is not None:
                update_kwargs['description'] = new_description
            if new_priority is not None:
                update_kwargs['priority'] = new_priority
            if new_tags is not None:
                update_kwargs['tags'] = new_tags
            if new_due_date is not None:
                update_kwargs['due_date'] = new_due_date
            if new_reminder_time is not None:
                update_kwargs['reminder_time'] = new_reminder_time

            # Only update other fields if there are changes to make
            if update_kwargs:
                task = self.task_service.update_task(task_id, **update_kwargs)
                print(f"{GREEN}Task updated successfully!{RESET} ID: {task.id}, Title: {task.title}")
        except (TaskNotFoundError, TaskValidationError) as e:
            print(f"{RED}Error updating task:{RESET} {str(e)}")

    def _parse_update_args(self, args: str):
        """Parse update command arguments including --priority, --tags, --due, --remind, --cancel-recur, and --update-recur flags."""
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
        new_due_date = None
        new_reminder_time = None
        cancel_recurrence = False
        update_recurrence = None

        i = 1  # Start after task ID
        while i < len(parts):
            part = parts[i]

            if part == '--priority' and i + 1 < len(parts):
                new_priority = parts[i + 1]
                i += 2
            elif part == '--tags' and i + 1 < len(parts):
                new_tags = [tag.strip() for tag in parts[i + 1].split(',') if tag.strip()]
                i += 2
            elif part == '--due' and i + 1 < len(parts):
                from src.services.datetime_utils import parse_datetime_string
                new_due_date = parse_datetime_string(parts[i + 1])
                if new_due_date is None:
                    raise ValueError(f"Invalid due date format: {parts[i + 1]}")
                i += 2
            elif part == '--remind' and i + 1 < len(parts):
                from src.services.datetime_utils import parse_datetime_string
                new_reminder_time = parse_datetime_string(parts[i + 1])
                if new_reminder_time is None:
                    raise ValueError(f"Invalid reminder time format: {parts[i + 1]}")
                i += 2
            elif part in ['--cancel-recur', '-cr']:
                cancel_recurrence = True
                i += 1
            elif part in ['--update-recur', '-ur'] and i + 1 < len(parts):
                from src.services.recurrence_service import RecurrenceService
                update_recurrence = self._parse_recurrence_pattern(parts[i + 1])
                if update_recurrence is None:
                    raise ValueError(f"Invalid recurrence pattern: {parts[i + 1]}")
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

        return task_id, new_title, new_description, new_priority, new_tags, new_due_date, new_reminder_time, cancel_recurrence, update_recurrence

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
        print(f"  add <title> [description] [--priority high|medium|low] [--tags tag1,tag2,...] [--due YYYY-MM-DD] [--remind YYYY-MM-DD HH:MM] [--recur daily|weekly|every N days|weeks]     - Add a new task")
        print(f"  view                          - View all tasks")
        print(f"  update <id> <title> [desc] [--priority high|medium|low] [--tags tag1,tag2,...]  - Update task details")
        print(f"  delete <id>                   - Delete a task")
        print(f"  complete <id>                 - Mark task as complete")
        print(f"  incomplete <id>               - Mark task as incomplete")
        print(f"  list [--status complete|incomplete] [--priority high|medium|low] [--tag tag] [--sort priority|alpha|created] - List tasks with filters and sorting")
        print(f"  search <keyword> [--sort priority|alpha|created] - Search tasks by keyword")
        print(f"  recurring --list | --cancel ID | --next - Manage recurring tasks")
        print(f"  reminders --list | --triggered | --upcoming - Manage reminders")
        print(f"  stats                         - Show task statistics chart")
        print(f"  help                          - Show this help")
        print(f"  quit/exit                     - Exit the application")

    def _handle_quit(self, args: str):
        print(f"{YELLOW}Goodbye!{RESET}")
        return False

    def _handle_recurring(self, args: str):
        """Handle the recurring command with options like --list, --cancel, --next."""
        import shlex
        parts = shlex.split(args) if args.strip() else []

        if not parts or parts[0] in ['-h', '--help']:
            print("Usage: recurring --list | --cancel ID | --next")
            print("  --list, -l    List all recurring tasks")
            print("  --cancel ID   Cancel a recurring pattern")
            print("  --next        Show next occurrences of recurring tasks")
            return

        if parts[0] in ['--list', '-l']:
            from src.services.task_storage import recurrence_templates
            recurring_tasks = list(recurrence_templates.values())
            if not recurring_tasks:
                print(f"{YELLOW}No recurring tasks found.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}Recurring Tasks:{RESET}")
            for task in recurring_tasks:
                self._print_task_box(task)

        elif parts[0] in ['--cancel', '-c'] and len(parts) >= 2:
            try:
                task_id = int(parts[1])
                from src.services.recurrence_service import RecurrenceService
                success = RecurrenceService.cancel_recurrence_pattern(task_id)
                if success:
                    print(f"{GREEN}Recurring pattern canceled for task {task_id}.{RESET}")
                else:
                    print(f"{RED}Task {task_id} not found or not a recurring task.{RESET}")
            except ValueError:
                print(f"{RED}Error:{RESET} Task ID must be a number.")
        elif parts[0] in ['--next', '-n']:
            from src.services.recurrence_service import RecurrenceService
            # Generate any new recurring tasks that should be created
            new_tasks = RecurrenceService.generate_recurring_tasks()
            if new_tasks:
                print(f"{GREEN}Generated {len(new_tasks)} new recurring task instances.{RESET}")
                for task in new_tasks:
                    self._print_task_box(task)
            else:
                print(f"{YELLOW}No new recurring tasks to generate at this time.{RESET}")
        else:
            print(f"{RED}Unknown recurring command option.{RESET}")
            print("Usage: recurring --list | --cancel ID | --next")

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

    def _handle_reminders(self, args: str):
        """Handle the reminders command with options like --list, --triggered, --upcoming."""
        import shlex
        parts = shlex.split(args) if args.strip() else []

        if not parts or parts[0] in ['-h', '--help']:
            print("Usage: reminders --list | --triggered | --upcoming")
            print("  --list, -l       List all active reminders")
            print("  --triggered, -t  List triggered reminders")
            print("  --upcoming, -u   List upcoming reminders")
            return

        from src.services.reminder_service import ReminderService

        if parts[0] in ['--list', '-l']:
            # List all reminders (both upcoming and triggered)
            all_reminders = list(self._get_all_reminders().values())
            if not all_reminders:
                print(f"{YELLOW}No reminders found.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}All Reminders:{RESET}")
            for reminder in all_reminders:
                task = self.task_service.get_all_tasks()
                task_dict = {t.id: t for t in task}
                task = task_dict.get(int(reminder.task_id))
                if task:
                    status = "TRIGGERED" if reminder.triggered else "UPCOMING"
                    status_color = GREEN if reminder.triggered else YELLOW
                    print(f"  {status_color}Task {reminder.task_id}: {task.title} - Reminder at {reminder.reminder_time.strftime('%Y-%m-%d %H:%M')} ({status}){RESET}")

        elif parts[0] in ['--triggered', '-t']:
            triggered_reminders = ReminderService.get_triggered_reminders()
            if not triggered_reminders:
                print(f"{YELLOW}No triggered reminders found.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}Triggered Reminders:{RESET}")
            for reminder in triggered_reminders:
                task = self.task_service.get_all_tasks()
                task_dict = {t.id: t for t in task}
                task = task_dict.get(int(reminder.task_id))
                if task:
                    triggered_time = reminder.triggered_at.strftime('%Y-%m-%d %H:%M') if reminder.triggered_at else "Unknown"
                    print(f"  {GREEN}Task {reminder.task_id}: {task.title} - Triggered at {triggered_time}{RESET}")

        elif parts[0] in ['--upcoming', '-u']:
            upcoming_reminders = ReminderService.get_upcoming_reminders()
            if not upcoming_reminders:
                print(f"{YELLOW}No upcoming reminders found.{RESET}")
                return

            print(f"\n{BOLD}{CYAN}Upcoming Reminders:{RESET}")
            for reminder in upcoming_reminders:
                task = self.task_service.get_all_tasks()
                task_dict = {t.id: t for t in task}
                task = task_dict.get(int(reminder.task_id))
                if task:
                    print(f"  {YELLOW}Task {reminder.task_id}: {task.title} - Reminder at {reminder.reminder_time.strftime('%Y-%m-%d %H:%M')}{RESET}")
        else:
            print(f"{RED}Unknown reminders command option.{RESET}")
            print("Usage: reminders --list | --triggered | --upcoming")

    def _get_all_reminders(self):
        """Helper method to get all reminders from storage."""
        from src.services.task_storage import reminders
        return reminders

    # ------------------- Task Box ------------------- #
    def _print_task_box(self, task: Task):
        status = f"{GREEN}[✓]{RESET}" if task.completed else f"{RED}[ ]{RESET}"
        priority_display = f"[{task.priority.upper()}]"
        tags_display = " ".join([f"#{tag}" for tag in task.tags]) if task.tags else ""

        # Build main task info line
        task_info = f"ID: {task.id} {status} {priority_display} {task.title}"
        if tags_display:
            task_info += f" {tags_display}"

        print(f"{BOLD}{CYAN}+{'-'*60}+{RESET}")
        print(f"{BOLD}{CYAN}| {task_info:<58} |{RESET}")

        # Add additional info lines for advanced features
        additional_info = []

        if task.due_date:
            due_str = task.due_date.strftime("%Y-%m-%d %H:%M")
            # Check if task is overdue
            from datetime import datetime
            if not task.completed and task.due_date < datetime.now():
                additional_info.append(f"  {RED}DUE: {due_str} (OVERDUE){RESET}")
            else:
                additional_info.append(f"  DUE: {due_str}")

        if task.reminder_time:
            reminder_str = task.reminder_time.strftime("%Y-%m-%d %H:%M")
            additional_info.append(f"  REMINDER: {reminder_str}")

        if task.recurrence_pattern:
            pattern_info = f"  RECURRING: {task.recurrence_pattern.type}"
            if task.recurrence_pattern.interval:
                pattern_info += f" (every {task.recurrence_pattern.interval} days)"
            if task.recurrence_pattern.days_of_week:
                pattern_info += f" on days {task.recurrence_pattern.days_of_week}"
            additional_info.append(pattern_info)

        if task.parent_task_id:
            additional_info.append(f"  RECURRING INSTANCE (parent: {task.parent_task_id})")

        # Print additional info lines
        for info in additional_info:
            print(f"{BOLD}{CYAN}| {info:<58} |{RESET}")

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
