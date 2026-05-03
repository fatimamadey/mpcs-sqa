# Playwright fixtures for Exercise 2 unhappy-path tests that takes screenshots for every test
# Written by Claude, edited by Fatima Madey

import os
import pytest

SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "screenshots"
)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Maps test function name → screenshot filename prefix (category-based naming)
_SCREENSHOT_NAMES = {
    "test_login_with_invalid_password":   "01_invalid_input",
    "test_place_order_with_empty_cart":   "02_boundary_edge",
    "test_signup_with_existing_username": "03_equivalence_class",
    "test_contact_form_all_fields_empty": "04_exception_handling",
    "test_add_same_product_twice":        "05_business_logic",
}


@pytest.fixture(autouse=True)
def capture_screenshot(request, page):
    """
    Auto-used fixture: takes a screenshot of every Playwright test result
    and saves it to /screenshots/ using a category-based filename.
    """
    yield  # run the test
    base_name = _SCREENSHOT_NAMES.get(request.node.originalname, request.node.originalname)
    path = os.path.join(SCREENSHOTS_DIR, f"{base_name}.png")
    try:
        page.screenshot(path=path, full_page=True)
    except Exception as exc:
        print(f"Warning: could not take screenshot — {exc}")
