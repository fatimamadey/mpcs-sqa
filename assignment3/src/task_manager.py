"""TaskManager — core application logic."""

from datetime import date
from typing import List, Optional

from src.exceptions import (
    DuplicateUserError,
    InvalidTaskError,
    TaskNotFoundError,
    UnauthorizedError,
    UserNotFoundError,
)
from src.models import Priority, Task, User
from src.reminder_service import ReminderService


class TaskManager:
    def __init__(self, reminder_service: ReminderService):
        # users: dict[int, User], tasks: dict[int, Task], counters for ids
        self._reminder_service = reminder_service
        self.users = {}
        self.tasks = {}
        self.next_user_id = 1
        self.next_task_id = 1

    # ── User Auth ──────────────────────────────────────────────────────────────

    def register_user(self, username: str, password: str) -> User:
        for user in self.users.values():
            if user.username == username:
                raise DuplicateUserError(f"Username '{username}' is already taken.")

        password_hash = hash(password)
        user = User(user_id=self.next_user_id, username=username, password_hash=password_hash)
        self.users[self.next_user_id] = user
        self.next_user_id += 1
        return user

    def login(self, username: str, password: str) -> User:
        for user in self.users.values():
            if user.username == username:
                if user.password_hash != hash(password):
                    raise UnauthorizedError("Incorrect password.")
                return user
        raise UserNotFoundError(f"User '{username}' not found.")

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
        if user_id not in self.users:
            raise UserNotFoundError(f"User ID {user_id} not found.")
        task = Task(
            task_id=self.next_task_id,
            owner_id=user_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            category=category,
        )
        self.tasks[self.next_task_id] = task
        self.users[user_id].tasks.append(task)
        self.next_task_id += 1
        return task

    def get_task(self, user_id: int, task_id: int) -> Task:
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Task ID {task_id} not found.")
        task = self.tasks[task_id]
        if task.owner_id != user_id:
            raise UnauthorizedError("You do not have permission to access this task.")
        return task

    def update_task(self, user_id: int, task_id: int, **fields) -> Task:
        task = self.get_task(user_id, task_id)
        allowed_fields = ["title", "description", "priority", "due_date", "category"]
        for field, value in fields.items():
            if field in allowed_fields:
                if field == "title" and not value:
                    raise InvalidTaskError("Title cannot be blank.")
                setattr(task, field, value)
        return task

    def delete_task(self, user_id: int, task_id: int) -> None:
        task = self.get_task(user_id, task_id)
        del self.tasks[task_id]
        self.users[user_id].tasks.remove(task)

    def complete_task(self, user_id: int, task_id: int) -> Task:
        task = self.get_task(user_id, task_id)
        task.completed = True
        return task

    def incomplete_task(self, user_id: int, task_id: int) -> Task:
        task = self.get_task(user_id, task_id)
        task.completed = False
        return task

    # ── Sorting & Filtering ────────────────────────────────────────────────────

    def get_tasks(self, user_id: int) -> List[Task]:
        if user_id not in self.users:
            raise UserNotFoundError(f"User ID {user_id} not found.")
        return self.users[user_id].tasks

    def sort_tasks(self, user_id: int, by: str) -> List[Task]:
        if by not in ["priority", "due_date", "completed"]:
            raise InvalidTaskError(f"Unknown sort key: {by}")
        tasks = self.get_tasks(user_id)
        if by == "priority":
            priority_order = {
                Priority.LOW: 0,
                Priority.MEDIUM: 1,
                Priority.HIGH: 2,
            }
            return sorted(tasks, key=lambda t: priority_order[t.priority])
        elif by == "due_date":
            return sorted(tasks, key=lambda t: (t.due_date or date.max))
        elif by == "completed":
            return sorted(tasks, key=lambda t: t.completed)

    def filter_tasks(self, user_id: int, category: str = "", keyword: str = "") -> List[Task]:
        tasks = self.get_tasks(user_id)
        if category:
            tasks = [t for t in tasks if t.category == category]
        if keyword:
            tasks = [t for t in tasks if keyword in t.title or keyword in t.description]
        return tasks

    # ── Reminders ─────────────────────────────────────────────────────────────

    def set_reminder(self, user_id: int, task_id: int, message: str) -> None:
        self.get_task(user_id, task_id)
        self._reminder_service.send_reminder(user_id, task_id, message)
