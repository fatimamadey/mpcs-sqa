# Cart Page - read cart rows, place order form, delete items, confirm purchase

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

BASE_URL = "https://www.demoblaze.com"

class CartPage(BasePage):
    # Locators
    CART_TABLE         = (By.ID, "tbodyid")
    CART_ROWS          = (By.CSS_SELECTOR, "#tbodyid tr")
    PRODUCT_NAMES      = (By.CSS_SELECTOR, "#tbodyid td:nth-child(2)")

    PLACE_ORDER_BTN    = (By.XPATH, "//button[text()='Place Order']")

    ORDER_MODAL        = (By.ID, "orderModal")
    ORDER_NAME         = (By.ID, "name")
    ORDER_COUNTRY      = (By.ID, "country")
    ORDER_CITY         = (By.ID, "city")
    ORDER_CARD         = (By.ID, "card")
    ORDER_MONTH        = (By.ID, "month")
    ORDER_YEAR         = (By.ID, "year")
    ORDER_PURCHASE_BTN = (By.XPATH, "//button[text()='Purchase']")

    CONFIRM_MODAL      = (By.CSS_SELECTOR, ".sweet-alert")
    CONFIRM_TEXT       = (By.CSS_SELECTOR, ".sweet-alert p")
    CONFIRM_OK_BTN     = (By.CSS_SELECTOR, ".sweet-alert button.confirm")

    DELETE_LINKS       = (By.XPATH, "//a[text()='Delete']")

    # Nav
    def load(self):
        self.open("cart.html")
        self.wait_for_visible(self.CART_TABLE)
        return self
    
    # Reads
    def row_count(self) -> int:
        time.sleep(1)  # allow AJAX to populate rows
        return len(self.driver.find_elements(*self.CART_ROWS))

    def product_names(self) -> list[str]:
        time.sleep(2)
        return [el.text for el in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def is_product_in_cart(self, name: str) -> bool:
        return any(name.lower() in n.lower() for n in self.product_names())

    # Place Order
    def open_place_order(self):
        self.wait_for_clickable(self.PLACE_ORDER_BTN).click()
        self.wait_for_visible(self.ORDER_MODAL)

    def fill_order_form(
        self,
        name: str,
        country: str,
        city: str,
        card: str,
        month: str,
        year: str,
    ):
        self.driver.find_element(*self.ORDER_NAME).send_keys(name)
        self.driver.find_element(*self.ORDER_COUNTRY).send_keys(country)
        self.driver.find_element(*self.ORDER_CITY).send_keys(city)
        self.driver.find_element(*self.ORDER_CARD).send_keys(card)
        self.driver.find_element(*self.ORDER_MONTH).send_keys(month)
        self.driver.find_element(*self.ORDER_YEAR).send_keys(year)

    def confirm_purchase(self) -> str:
        """Click Purchase, wait for the success modal, return its text."""
        self.wait_for_clickable(self.ORDER_PURCHASE_BTN).click()
        confirmation = self.wait_for_visible(self.CONFIRM_MODAL)
        text = self.driver.find_element(*self.CONFIRM_TEXT).text
        return text

    def dismiss_confirmation(self):
        self.wait_for_clickable(self.CONFIRM_OK_BTN).click()

    # Delete from cart
    def delete_first_item(self):
        """Click the first 'Delete' link and wait for the row to disappear."""
        delete_links = self.driver.find_elements(*self.DELETE_LINKS)
        if not delete_links:
            raise AssertionError("No items in cart to delete.")
        delete_links[0].click()
        time.sleep(1.5)  # allow the AJAX delete to complete