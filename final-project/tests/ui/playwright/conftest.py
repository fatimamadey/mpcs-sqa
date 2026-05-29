import os
import subprocess
import sys
import pytest

# Resolve the path to manage.py relative to this file
_MANAGE_PY = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "app", "manage.py"
)
_TEST_USER = os.environ.get("TEST_ADMIN_USER", "uitestuser_reg")


@pytest.fixture(scope="session", autouse=True)
def grant_poll_permission():
    """Grant polls.add_poll to the E2E test user and clear any prior votes so
    test_create_poll_with_choices and test_submit_vote_and_view_results always
    start from a clean state."""
    code = (
        "from django.contrib.auth.models import User, Permission; "
        "from polls.models import Vote; "
        f"u = User.objects.filter(username='{_TEST_USER}').first(); "
        "p = Permission.objects.filter(codename='add_poll').first(); "
        "[u.user_permissions.add(p)] if u and p else None; "
        "Vote.objects.filter(user=u).delete() if u else None"
    )
    subprocess.run(
        [sys.executable, _MANAGE_PY, "shell", "-c", code],
        check=False,
        capture_output=True,
    )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Run Playwright tests in a 1280×900 viewport."""
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}


@pytest.fixture(autouse=True)
def screenshot_after_test(page, request):
    """
    Capture a screenshot at the end of every UI test (pass or fail).
    Saved to  final-project/screenshots/<test_name>.png
    """
    yield
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "screenshots"
    )
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, f"{request.node.name}.png")
    page.screenshot(path=screenshot_path)
    print(f"\nScreenshot saved: {screenshot_path}")
