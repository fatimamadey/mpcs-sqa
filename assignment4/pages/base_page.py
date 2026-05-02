from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://www.demoblaze.com"
DEFAULT_TIMEOUT = 10

class BasePage:
    def __init__(self, driver):
        self.driver = driver # driver is the Selenium WebDriver instance (e.g., Chrome, Safari)
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT) # wait 12 sec before throwing a TimeoutException
    
    # Nav Helpers
    def open(self, path: str = ""):
        self.driver.get(f"{BASE_URL}/{path}")

    def current_url(self) -> str:
        return self.driver.current_url
    
    # Wait Helpers (so code is easier to read in page objects)
    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_text_in_element(self, locator, text: str):
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))
    
    # Alert Helpers
    def accept_alert(self) -> str:
        """Wait for an alert, capture its text, then dismiss it."""
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        return text

    def dismiss_alert(self) -> str:
        """Wait for an alert, capture its text, then dismiss it."""
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text
        alert.dismiss()
        return text
    
    # Nav Bar State Helpers
    def navbar_username(self) -> str:
        """Return the text of the logged-in username element in the navbar."""
        el = self.wait_for_visible((By.ID, "nameofuser"))
        return el.text

    def is_logged_in(self) -> bool:
        """True when the 'Welcome, <user>' span is visible in the navbar."""
        try:
            self.wait_for_visible((By.ID, "nameofuser"))
            return True
        except Exception:
            return False

    def is_login_link_visible(self) -> bool:
        """True when the 'Log in' nav link is present and visible."""
        try:
            el = self.driver.find_element(By.ID, "login2")
            return el.is_displayed()
        except Exception:
            return False
