"""Reminder service — outgoing side-effect seam (injectable)."""


class ReminderService:
    def send_reminder(self, user_id: int, task_id: int, message: str) -> None:
        # TODO: delivery mechanism (email, push, etc.) — real impl is out of scope
        # In production this would call an external service.
        # For testing, we will mock this method to verify it was called with correct params.
        pass
