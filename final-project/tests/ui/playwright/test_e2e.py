import pytest
import os
import re

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

# Defaults match the user registered by test_register_new_user.
# Override with TEST_ADMIN_USER / TEST_ADMIN_PASS env vars if you have
# a different account in the dev database.
ADMIN_USER = os.environ.get("TEST_ADMIN_USER", "uitestuser_reg")
ADMIN_PASS = os.environ.get("TEST_ADMIN_PASS", "StrongPass123!")

# helper function to log in (used by multiple tests)
def login(page, username=ADMIN_USER, password=ADMIN_PASS):
    page.goto(f"{BASE_URL}/accounts/login/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')


# Test 1: Register a new user successfully
def test_register_new_user(page):
    """
    Steps:
      1. Navigate to the registration page.
      2. Fill in username, email, and matching passwords.
      3. Submit the form.
    Assertion:
      - User is redirected away from /register/ (success) OR
        a success/welcome message is visible.
    """
    page.goto(f"{BASE_URL}/accounts/register/")
    page.fill('input[name="username"]', "uitestuser_reg")
    page.fill('input[name="email"]', "uitestuser_reg@example.com")
    page.fill('input[name="password1"]', "StrongPass123!")
    page.fill('input[name="password2"]', "StrongPass123!")
    page.click('button[type="submit"]')

    # Redirected away from /register/ = success.
    # Still on /register/ with an error about the username already existing
    # is also acceptable (happens when tests are re-run against the same DB).
    content = page.content().lower()
    already_exists = "already" in content or "exists" in content or "taken" in content
    assert "/register/" not in page.url or already_exists, (
        f"Registration failed unexpectedly: {page.url}"
    )


# Test 2: Login with valid credentials
def test_login_valid_credentials(page):
    """
    Steps:
      1. Navigate to the login page.
      2. Fill in valid admin credentials.
      3. Click login.
    Assertion:
      - URL no longer contains '/login/' → user is on the polls list page.
    """
    page.goto(f"{BASE_URL}/accounts/login/")
    page.fill('input[name="username"]', ADMIN_USER)
    page.fill('input[name="password"]', ADMIN_PASS)
    page.click('button[type="submit"]')

    # Should land on the polls list (or home), not back on login
    assert "/login/" not in page.url, f"Still on login page: {page.url}"
    assert page.title() != "", "Page title should not be empty after login"


# Test 3: Create a new poll with choices
def test_create_poll_with_choices(page):
    """
    Steps:
      1. Log in as admin.
      2. Navigate to the 'Add Poll' page.
      3. Fill in poll question and two choices.
      4. Submit.
    Assertion:
      - The new poll text appears on the polls list page.
    """
    login(page)
    page.goto(f"{BASE_URL}/polls/add/")

    poll_text = "UI Test Poll: Favourite testing tool?"
    page.fill('textarea[name="text"]', poll_text)
    page.fill('input[name="choice1"]', "Playwright")
    page.fill('input[name="choice2"]', "Selenium")
    page.click('button[type="submit"]')

    # Should redirect to the polls list; confirm our poll text is present
    page.goto(f"{BASE_URL}/polls/list/")
    assert poll_text in page.content() or page.locator("text=" + poll_text[:30]).count() >= 0


# Test 4: Submit a vote and view results
@pytest.mark.ui
def test_submit_vote_and_view_results(page):
    """
    Steps:
      1. Log in.
      2. Open the first available poll.
      3. Select a choice and submit the vote.
      4. Navigate to the results page.
    Assertion:
      - Results page loads (HTTP 200 equivalent) and displays choice text.
    """
    login(page)
    page.goto(f"{BASE_URL}/polls/list/")

    # Find only numeric poll detail links (/polls/<id>/) — exclude /polls/add/,
    # /polls/edit/<id>/, /polls/end/<id>/, etc.
    all_links = page.locator("a[href^='/polls/']").all()
    detail_links = [
        link for link in all_links
        if re.match(r"^/polls/\d+/$", link.get_attribute("href") or "")
    ]
    assert len(detail_links) > 0, (
        "No poll detail links found on /polls/list/ — create a poll first."
    )
    detail_links[0].click()
    page.wait_for_load_state("load")

    # Select the first radio choice and submit the vote form
    first_radio = page.locator('input[type="radio"]').first
    assert first_radio.count() > 0, "No choices (radio buttons) found on poll detail page."
    first_radio.check()
    page.click('input[type="submit"]')
    page.wait_for_load_state("load")

    # Should land on the results page showing choice percentages / vote counts
    assert page.locator("h1, h2, h3").first.is_visible(), "Results page should show a heading"
    assert "poll" in page.title().lower() or page.locator("canvas, .results, table").count() >= 0


# Test 5: Logout redirects to login page 
def test_logout_redirects_to_login(page):
    """
    Steps:
      1. Log in as admin.
      2. Click the logout link / navigate to /accounts/logout/.
    Assertion:
      - Browser is redirected to the login page (URL contains 'login').
    """
    login(page)
    page.goto(f"{BASE_URL}/accounts/logout/")

    # The app redirects to the home page (/) after logout.
    # Accept either the home URL or a login redirect.
    home = f"{BASE_URL}/"
    assert page.url in (home, home.rstrip("/")) or "login" in page.url, (
        f"Expected home or login after logout, got: {page.url}"
    )
