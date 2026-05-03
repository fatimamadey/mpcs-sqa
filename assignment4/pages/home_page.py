# Home Page - login, logout, signup, contact form, product list, category filter, pagination
import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    # Locators
    NAV_LOGIN      = (By.ID, "login2")
    NAV_LOGOUT     = (By.ID, "logout2")
    NAV_SIGNUP     = (By.ID, "signin2")
    NAV_CONTACT    = (By.XPATH, "//a[text()='Contact']")
    LOGIN_MODAL    = (By.ID, "logInModal")
    LOGIN_USER     = (By.ID, "loginusername")
    LOGIN_PASS     = (By.ID, "loginpassword")
    LOGIN_BTN      = (By.XPATH, "//button[text()='Log in']")

    SIGNUP_MODAL   = (By.ID, "signInModal")
    SIGNUP_USER    = (By.ID, "sign-username")
    SIGNUP_PASS    = (By.ID, "sign-password")
    SIGNUP_BTN     = (By.XPATH, "//button[text()='Sign up']")
    CONTACT_MODAL  = (By.ID, "exampleModal")
    CONTACT_EMAIL  = (By.ID, "recipient-email")
    CONTACT_NAME   = (By.ID, "recipient-name")
    CONTACT_MSG    = (By.ID, "message-text")
    CONTACT_SEND   = (By.XPATH, "//button[text()='Send message']")
    PRODUCT_TILES  = (By.CLASS_NAME, "card")
    PRODUCT_LINKS  = (By.CSS_SELECTOR, ".card-title a")

    CAT_PHONES     = (By.XPATH, "//a[text()='Phones']")

    NEXT_BTN       = (By.ID, "next2")
    PREV_BTN       = (By.ID, "prev2")

    # Navigation
    def load(self):
        self.open("")
        # Wait until at least one product tile is present
        self.wait_for_visible(self.PRODUCT_TILES)
        return self
    
    # Auth
    def open_login_modal(self):
        self.wait_for_clickable(self.NAV_LOGIN).click()
        self.wait_for_visible(self.LOGIN_MODAL)

    def login(self, username: str, password: str):
        self.open_login_modal()
        self.driver.find_element(*self.LOGIN_USER).clear()
        self.driver.find_element(*self.LOGIN_USER).send_keys(username)
        self.driver.find_element(*self.LOGIN_PASS).clear()
        self.driver.find_element(*self.LOGIN_PASS).send_keys(password)
        self.wait_for_clickable(self.LOGIN_BTN).click()

    def logout(self):
        self.wait_for_clickable(self.NAV_LOGOUT).click()

    def open_signup_modal(self):
        self.wait_for_clickable(self.NAV_SIGNUP).click()
        self.wait_for_visible(self.SIGNUP_MODAL)

    def signup(self, username: str, password: str):
        self.open_signup_modal()
        self.driver.find_element(*self.SIGNUP_USER).clear()
        self.driver.find_element(*self.SIGNUP_USER).send_keys(username)
        self.driver.find_element(*self.SIGNUP_PASS).clear()
        self.driver.find_element(*self.SIGNUP_PASS).send_keys(password)
        self.wait_for_clickable(self.SIGNUP_BTN).click()

    def open_contact_modal(self):
        self.wait_for_clickable(self.NAV_CONTACT).click()
        self.wait_for_visible(self.CONTACT_MODAL)

    def submit_contact(self, email: str, name: str, message: str):
        self.open_contact_modal()
        self.driver.find_element(*self.CONTACT_EMAIL).send_keys(email)
        self.driver.find_element(*self.CONTACT_NAME).send_keys(name)
        self.driver.find_element(*self.CONTACT_MSG).send_keys(message)
        self.wait_for_clickable(self.CONTACT_SEND).click()

    # Products
    def product_tile_count(self) -> int:
        """Return the number of product cards currently visible."""
        tiles = self.driver.find_elements(*self.PRODUCT_TILES)
        return len(tiles)

    def product_names(self) -> list[str]:
        """Return the text of every visible product link."""
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_LINKS)]

    def click_first_product(self):
        """Click the very first product tile (any category)."""
        self.wait_for_clickable(self.PRODUCT_LINKS).click()

    # Categories
    def filter_by_phones(self):
        self.wait_for_clickable(self.CAT_PHONES).click()
        # Brief pause for the AJAX filter to settle
        time.sleep(1.5)

    # Pagination
    def click_next(self):
        self.wait_for_clickable(self.NEXT_BTN).click()
        time.sleep(1.5)

    def click_prev(self):
        self.wait_for_clickable(self.PREV_BTN).click()
        time.sleep(1.5)
