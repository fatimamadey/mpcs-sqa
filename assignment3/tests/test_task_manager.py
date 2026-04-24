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

    # Act 

    # Assert 
    
    pass

def test_login_with_correct_credentials_returns_user(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_create_task_returns_task_with_correct_title(registered_user):
    # Arrange 

    # Act 

    # Assert 

    pass

def test_delete_task_removes_it_from_task_list(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_complete_task_sets_completed_true(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_incomplete_task_sets_completed_false(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass


# ── Invalid Input ──────────────────────────────────────────────────────────────

def test_create_task_with_blank_title_raises_invalid_task_error(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_register_duplicate_username_raises_duplicate_user_error(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_login_wrong_password_raises_unauthorized_error(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_sort_tasks_unknown_key_raises_invalid_task_error(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

# ── Boundary / Edge ────────────────────────────────────────────────────────────

def test_get_tasks_returns_empty_list_for_new_user(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_filter_tasks_keyword_matches_description_not_title(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_create_task_title_exactly_one_character_is_valid(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_complete_already_completed_task_stays_completed(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass


# ── Equivalence Classes ────────────────────────────────────────────────────────

def test_low_priority_task_sorts_after_high_priority(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_filter_by_category_returns_only_matching_tasks(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_tasks_from_different_users_are_independent(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass


# ── Exception Handling ─────────────────────────────────────────────────────────

def test_get_task_nonexistent_id_raises_task_not_found_error(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_get_task_wrong_user_raises_unauthorized_error(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_login_nonexistent_user_raises_user_not_found_error(manager):
    # Arrange 

    # Act 

    # Assert 
    
    pass


# ── Business Logic ─────────────────────────────────────────────────────────────

def test_sort_by_due_date_orders_tasks_ascending(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_sort_by_completed_puts_incomplete_tasks_first(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_update_task_persists_new_priority(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_set_reminder_delegates_to_reminder_service(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass

def test_delete_task_then_get_raises_task_not_found_error(registered_user):
    # Arrange 

    # Act 

    # Assert 
    
    pass
