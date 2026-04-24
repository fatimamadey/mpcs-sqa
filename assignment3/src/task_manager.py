"""TaskManager — core application logic."""

from datetime import date
from typing import List, Optional

from src.models import Priority, Task, User
from src.reminder_service import ReminderService


class TaskManager:
    def __init__(self, reminder_service: ReminderService):
        # TODO: store reminder_service; initialize in-memory dicts for users and tasks
        # users: dict[int, User], tasks: dict[int, Task], counters for ids
        pass

    # ── User Auth ──────────────────────────────────────────────────────────────

    def register_user(self, username: str, password: str) -> User:
        # TODO: raise DuplicateUserError if username taken
        # TODO: hash password (lightweight — e.g. hash()), create and store User, return it
        pass

    def login(self, username: str, password: str) -> User:
        # TODO: raise UserNotFoundError if username missing
        # TODO: raise UnauthorizedError if password wrong
        # TODO: return matching User
        pass

    # ── Task CRUD ──────────────────────────────────────────────────────────────

    def create_task(
        self,
        user_id: int,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[date] = None,
        category: str = "",
    ) -> Task:
        # TODO: raise UserNotFoundError if user_id unknown
        # TODO: create Task, store it, return it
        pass

    def get_task(self, user_id: int, task_id: int) -> Task:
        # TODO: raise TaskNotFoundError if task_id unknown
        # TODO: raise UnauthorizedError if task.owner_id != user_id
        # TODO: return task
        pass

    def update_task(self, user_id: int, task_id: int, **fields) -> Task:
        # TODO: call get_task (handles not-found + auth)
        # TODO: apply allowed field updates (title, description, priority, due_date, category)
        # TODO: re-validate; return updated task
        pass

    def delete_task(self, user_id: int, task_id: int) -> None:
        # TODO: call get_task (handles not-found + auth)
        # TODO: remove from storage
        pass

    def complete_task(self, user_id: int, task_id: int) -> Task:
        # TODO: call get_task; mark complete; return task
        pass

    def incomplete_task(self, user_id: int, task_id: int) -> Task:
        # TODO: call get_task; mark incomplete; return task
        pass

    # ── Sorting & Filtering ────────────────────────────────────────────────────

    def get_tasks(self, user_id: int) -> List[Task]:
        # TODO: raise UserNotFoundError if user_id unknown
        # TODO: return all tasks owned by user_id
        pass

    def sort_tasks(self, user_id: int, by: str) -> List[Task]:
        # TODO: accepted values: "priority", "due_date", "completed"
        # TODO: raise InvalidTaskError for unknown sort key
        # TODO: return sorted list
        pass

    def filter_tasks(self, user_id: int, category: str = "", keyword: str = "") -> List[Task]:
        # TODO: filter by category (exact match) and/or keyword (title/description substring)
        # TODO: return matching tasks
        pass

    # ── Reminders ─────────────────────────────────────────────────────────────

    def set_reminder(self, user_id: int, task_id: int, message: str) -> None:
        # TODO: call get_task (handles not-found + auth)
        # TODO: delegate to self._reminder_service.send_reminder(...)
        pass
