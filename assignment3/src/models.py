"""Domain models: Task and User."""

from datetime import date
from enum import Enum
from typing import Optional

from src.exceptions import InvalidTaskError

class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task:
    def __init__(
        self,
        task_id: int,
        owner_id: int,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[date] = None,
        category: str = "",
    ):
        if not title.strip():
            raise InvalidTaskError("Title cannot be blank.")
        
        self.task_id = task_id
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.category = category
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False


class User:
    def __init__(self, user_id: int, username: str, password_hash: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.tasks = []
