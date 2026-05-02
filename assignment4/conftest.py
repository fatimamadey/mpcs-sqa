# Written by Claude, edited by Fatima Madey
# Sources: https://pytest-selenium.readthedocs.io/en/latest/user_guide.html#chrome

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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

    if browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1280")
        options.add_argument("--height=900")
        return webdriver.Firefox(options=options)

    raise ValueError(f"Unsupported browser: {browser_name}")


# Parametrize all tests with a "browser" fixture, which will be set to the value of the --browser option (or both if not specified)
def pytest_addoption(parser):
    parser.addoption(
        "--sel-browser",
        action="store",
        default=None,
        help="Run only this browser (chrome | firefox). Omit to run both.",
    )


def pytest_generate_tests(metafunc):
    """Inject the 'browser' fixture parameter for every test that uses it."""
    if "browser" in metafunc.fixturenames:
        selected = metafunc.config.getoption("--sel-browser")
        browsers = [selected] if selected else ["chrome", "firefox"]
        metafunc.parametrize("browser", browsers)


@pytest.fixture
def driver(browser):
    """Selenium WebDriver — one fresh instance per test."""
    drv = _make_driver(browser)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
