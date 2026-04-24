"""Domain models: Task and User."""

from datetime import date
from enum import Enum
from typing import Optional


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
        # TODO: validate title is non-empty, raise InvalidTaskError if not
        # TODO: assign all fields; set completed = False by default
        pass

    def mark_complete(self):
        # TODO: set self.completed = True
        pass

    def mark_incomplete(self):
        # TODO: set self.completed = False
        pass


class User:
    def __init__(self, user_id: int, username: str, password_hash: str):
        # TODO: assign fields; initialize tasks as empty list
        pass
