"""Unit tests for TaskManager — happy path, CRUD, sorting, filtering, reminders."""

import pytest
from src.reminder_service import ReminderService
from src.task_manager import TaskManager
from src.models import Priority
from src.exceptions import (
    TaskNotFoundError,
    UnauthorizedError,
    UserNotFoundError,
    DuplicateUserError,
    InvalidTaskError,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def manager():
    # Dummy ReminderService — real object, no delivery side effects; replaced with a Mock in reminder tests
    return TaskManager(reminder_service=ReminderService())


@pytest.fixture
def registered_user(manager):
    # Returns (manager, user) so tests can call manager methods with user.user_id
    user = manager.register_user(username="testuser", password="password123")
    return manager, user


# ── Happy Path ─────────────────────────────────────────────────────────────────
def test_register_user_returns_user_with_correct_username(manager):
    # Arrange 
    username = "testuser"
    password = "password123"

    # Act 
    user = manager.register_user(username=username, password=password)

    # Assert 
    assert user.username == username

def test_login_with_correct_credentials_returns_user(manager):
    # Arrange 
    username = "testuser"
    password = "password123"
    manager.register_user(username=username, password=password)

    # Act 
    user = manager.login(username=username, password=password)

    # Assert 
    assert user.username == username
    assert user.password_hash == f"stubbed:{password}"

def test_create_task_returns_task_with_correct_title(registered_user):
    # Arrange 
    manager, user = registered_user
    title = "Test Task"
    description = "This is a test task."
    priority = Priority.MEDIUM

    # Act 
    task = manager.create_task(user_id=user.user_id, title=title, description=description, priority=priority)

    # Assert 
    assert task.title == title
    assert task.description == description
    assert task.priority == priority

def test_delete_task_removes_it_from_task_list(registered_user):
    # Arrange 
    manager, user = registered_user
    title = "Test Task"
    description = "This is a test task."
    priority = Priority.MEDIUM
    task = manager.create_task(user_id=user.user_id, title=title, description=description, priority=priority)

    # Act 
    manager.delete_task(user_id=user.user_id, task_id=task.task_id)

    # Assert 
    tasks = manager.get_tasks(user_id=user.user_id)
    assert task not in tasks

def test_complete_task_sets_completed_true(registered_user):
    # Arrange
    manager, user = registered_user
    title = "Test Task"
    task = manager.create_task(user_id=user.user_id, title=title)

    # Act 
    manager.complete_task(user_id=user.user_id, task_id=task.task_id)
    tasks = manager.get_tasks(user_id=user.user_id)

    # Assert 
    assert tasks[0].completed is True

def test_incomplete_task_sets_completed_false(registered_user):
    # Arrange 
    manager, user = registered_user
    title = "Test Task"
    task = manager.create_task(user_id=user.user_id, title=title)
    manager.complete_task(user_id=user.user_id, task_id=task.task_id)

    # Act 
    manager.incomplete_task(user_id=user.user_id, task_id=task.task_id)

    # Assert 
    tasks = manager.get_tasks(user_id=user.user_id)
    assert tasks[0].completed is False


# ── Invalid Input ──────────────────────────────────────────────────────────────

def test_create_task_with_blank_title_raises_invalid_task_error(registered_user):
    # Arrange
    manager, user = registered_user

    # Act / Assert
    with pytest.raises(InvalidTaskError):
        manager.create_task(user_id=user.user_id, title="   ")

def test_register_duplicate_username_raises_duplicate_user_error(manager):
    # Arrange
    username = "testuser"
    password = "password123"
    manager.register_user(username=username, password=password)

    # Act / Assert
    with pytest.raises(DuplicateUserError):
        manager.register_user(username=username, password=password)

def test_login_wrong_password_raises_unauthorized_error(manager):
    # Arrange
    username = "testuser"
    password = "password123"
    manager.register_user(username=username, password=password)

    # Act / Assert
    with pytest.raises(UnauthorizedError):
        manager.login(username=username, password="wrongpassword")

def test_sort_tasks_unknown_key_raises_invalid_task_error(registered_user):
    # Arrange 
    manager, user = registered_user

    # Act / Assert
    with pytest.raises(InvalidTaskError):
        manager.sort_tasks(user_id=user.user_id, by="unknownkey")

# ── Boundary / Edge ────────────────────────────────────────────────────────────

def test_get_tasks_returns_empty_list_for_new_user(registered_user):
    # Arrange 
    manager, user = registered_user

    # Act
    tasks = manager.get_tasks(user_id=user.user_id)

    # Assert
    assert tasks == []

def test_filter_tasks_keyword_matches_description_not_title(registered_user):
    # Arrange 
    manager, user = registered_user
    title = "Test Task"
    description = "This is a test task with a unique keyword: foobar."
    manager.create_task(user_id=user.user_id, title=title, description=description)

    # Act 
    tasks = manager.filter_tasks(user_id=user.user_id, keyword="foobar")

    # Assert 
    assert len(tasks) == 1
    assert tasks[0].description == description
    assert tasks[0].title == title

def test_create_task_title_exactly_one_character_is_valid(registered_user):
    # Arrange 
    manager, user = registered_user
    title = "A"
    description = "This is a test task with a one-character title."
    
    # Act 
    task = manager.create_task(user_id=user.user_id, title=title, description=description)

    # Assert 
    assert task.title == title
    assert task.description == description

def test_complete_already_completed_task_stays_completed(registered_user):
    # Arrange
    manager, user = registered_user
    title = "Test Task"
    task = manager.create_task(user_id=user.user_id, title=title)
    manager.complete_task(user_id=user.user_id, task_id=task.task_id)

    # Act
    manager.complete_task(user_id=user.user_id, task_id=task.task_id)
    tasks = manager.get_tasks(user_id=user.user_id)

    # Assert
    assert tasks[0].completed is True


# ── Equivalence Classes ────────────────────────────────────────────────────────

def test_low_priority_task_sorts_after_high_priority(registered_user):
    # Arrange 
    manager, user = registered_user
    manager.create_task(user_id=user.user_id, title="Low Priority Task", priority=Priority.LOW)
    manager.create_task(user_id=user.user_id, title="High Priority Task", priority=Priority.HIGH)

    # Act
    sorted_tasks = manager.sort_tasks(user_id=user.user_id, by="priority")

    # Assert 
    assert sorted_tasks[0].priority == Priority.HIGH
    assert sorted_tasks[1].priority == Priority.LOW

def test_filter_by_category_returns_only_matching_tasks(registered_user):
    # Arrange 
    manager, user = registered_user
    manager.create_task(user_id=user.user_id, title="Work Task", category="Work")
    manager.create_task(user_id=user.user_id, title="Home Task", category="Home")

    # Act
    work_tasks = manager.filter_tasks(user_id=user.user_id, category="Work")

    # Assert
    assert len(work_tasks) == 1
    assert work_tasks[0].category == "Work"

def test_tasks_from_different_users_are_independent(manager):
    # Arrange 
    user1 = manager.register_user(username="user1", password="password1")
    user2 = manager.register_user(username="user2", password="password2")
    manager.create_task(user_id=user1.user_id, title="User 1 Task")
    manager.create_task(user_id=user2.user_id, title="User 2 Task")

    # Act
    user1_tasks = manager.get_tasks(user_id=user1.user_id)
    user2_tasks = manager.get_tasks(user_id=user2.user_id)

    # Assert
    assert len(user1_tasks) == 1
    assert user1_tasks[0].title == "User 1 Task"
    assert len(user2_tasks) == 1
    assert user2_tasks[0].title == "User 2 Task"


# ── Exception Handling ─────────────────────────────────────────────────────────

def test_get_task_nonexistent_id_raises_task_not_found_error(registered_user):
    # Arrange 
    manager, user = registered_user

    # Act / Assert
    with pytest.raises(TaskNotFoundError):
        manager.get_task(user_id=user.user_id, task_id=999)

def test_get_task_wrong_user_raises_unauthorized_error(manager):
    # Arrange
    user1 = manager.register_user(username="user1", password="password1")
    user2 = manager.register_user(username="user2", password="password2")
    task = manager.create_task(user_id=user1.user_id, title="User 1 Task")

    # Act / Assert
    with pytest.raises(UnauthorizedError):
        manager.get_task(user_id=user2.user_id, task_id=task.task_id)

def test_login_nonexistent_user_raises_user_not_found_error(manager):
    # Arrange
    username = "nonexistent"
    password = "password123"

    # Act / Assert
    with pytest.raises(UserNotFoundError):
        manager.login(username=username, password=password)

# ── Business Logic ─────────────────────────────────────────────────────────────

def test_sort_by_due_date_orders_tasks_ascending(registered_user):
    # Arrange
    from datetime import date
    manager, user = registered_user
    manager.create_task(user_id=user.user_id, title="Task 1", due_date=date(2024, 6, 1))
    manager.create_task(user_id=user.user_id, title="Task 2", due_date=date(2024, 5, 1))

    # Act
    tasks = manager.sort_tasks(user_id=user.user_id, by="due_date")

    # Assert
    assert tasks[0].title == "Task 2"
    assert tasks[1].title == "Task 1"

def test_sort_by_completed_puts_incomplete_tasks_first(registered_user):
    # Arrange 
    manager, user = registered_user
    task1 = manager.create_task(user_id=user.user_id, title="Task 1")
    task2 = manager.create_task(user_id=user.user_id, title="Task 2")
    manager.complete_task(user_id=user.user_id, task_id=task2.task_id)

    # Act 
    tasks = manager.sort_tasks(user_id=user.user_id, by="completed")

    # Assert 
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

def test_update_task_persists_new_priority(registered_user):
    # Arrange
    manager, user = registered_user
    task = manager.create_task(user_id=user.user_id, title="Test Task", priority=Priority.MEDIUM)

    # Act 
    manager.update_task(user_id=user.user_id, task_id=task.task_id, priority=Priority.HIGH)
    updated_task = manager.get_task(user_id=user.user_id, task_id=task.task_id)

    # Assert 
    assert updated_task.priority == Priority.HIGH

def test_set_reminder_delegates_to_reminder_service(registered_user):
    # Arrange  [Mock: verify send_reminder is called with correct args — outgoing side-effect]
    from unittest.mock import MagicMock
    manager, user = registered_user
    mock_reminder = MagicMock()
    manager = TaskManager(reminder_service=mock_reminder)
    user = manager.register_user(username="testuser", password="password123")
    
    task = manager.create_task(user_id=user.user_id, title="Test Task")
    message = "Don't forget your task!"

    # Act
    manager.set_reminder(user_id=user.user_id, task_id=task.task_id, message=message)

    # Assert
    mock_reminder.send_reminder.assert_called_once_with(user.user_id, task.task_id, message)

def test_delete_task_then_get_raises_task_not_found_error(registered_user):
    # Arrange 
    manager, user = registered_user
    task = manager.create_task(user_id=user.user_id, title="Test Task")
    manager.delete_task(user_id=user.user_id, task_id=task.task_id)

    # Act / Assert
    with pytest.raises(TaskNotFoundError):
        manager.get_task(user_id=user.user_id, task_id=task.task_id)


