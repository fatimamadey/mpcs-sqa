# Written by Claude, edited by Fatima Madey
# Sources: https://pytest-selenium.readthedocs.io/en/latest/user_guide.html#chrome

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

BASE_URL = "https://www.demoblaze.com"

# Helper function to create WebDriver instances based on the requested browser
def _make_driver(browser_name: str):
    """Return an initialised WebDriver for the requested browser."""
    if browser_name == "chrome":
        options = ChromeOptions()
        # Remove --headless if you want to watch the tests run live
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        return webdriver.Chrome(options=options)

    if browser_name == "safari":
        # Safari must be run with Allow Remote Automation enabled in the
        # Develop menu.  SafariDriver does NOT support headless mode.
        options = SafariOptions()
        return webdriver.Safari(options=options)

    raise ValueError(f"Unsupported browser: {browser_name}")


# Parametrize all tests with a "browser" fixture, which will be set to the value of the --browser option (or both if not specified)
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Run only this browser (chrome | safari). Omit to run both.",
    )


def pytest_generate_tests(metafunc):
    """Inject the 'browser' fixture parameter for every test that uses it."""
    if "browser" in metafunc.fixturenames:
        selected = metafunc.config.getoption("--browser")
        browsers = [selected] if selected else ["chrome", "safari"]
        metafunc.parametrize("browser", browsers)


@pytest.fixture
def driver(browser):
    """Selenium WebDriver — one fresh instance per test."""
    drv = _make_driver(browser)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
