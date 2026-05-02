# Product Page - read the title and price, click Add to cart
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE  = (By.CSS_SELECTOR, ".name")
    PRODUCT_PRICE  = (By.CSS_SELECTOR, ".price-container")
    ADD_TO_CART    = (By.XPATH, "//a[text()='Add to cart']")

    # Reads
    def title(self) -> str:
        return self.wait_for_visible(self.PRODUCT_TITLE).text

    def price(self) -> str:
        return self.wait_for_visible(self.PRODUCT_PRICE).text
    
    # Actions
    def add_to_cart(self) -> str:
        """Click 'Add to cart', accept the alert, return the alert text."""
        self.wait_for_clickable(self.ADD_TO_CART).click()
        return self.accept_alert()