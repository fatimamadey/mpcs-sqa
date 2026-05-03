# Happy Path Tests - Selenium
import time
import uuid
import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

# Shared test data
EXISTING_USER = {"username": "fatima_dada", "password": "123456"}
NEW_USER_PASSWORD = "newpassword123"

# Test 1 - Login (valid credentials)
class TestLogin:
    def test_login_valid_credentials(self, driver):
        # Arrange
        page = HomePage(driver)
        # Act
        page.load()
        page.login(EXISTING_USER["username"], EXISTING_USER["password"])
        time.sleep(1)  # wait for login to process
        # Assert
        assert page.is_logged_in(), "Expected to be logged in (nameofuser visible)"
        assert EXISTING_USER["username"] in page.navbar_username(), (f"Expected '{EXISTING_USER['username']}' in navbar username")

# Test 2 - Logout
class TestLogout:
    def test_logout(self, driver):
        # Arrange
        # log in first
        page = HomePage(driver)
        page.load()
        page.login(EXISTING_USER["username"], EXISTING_USER["password"])
        time.sleep(1)
        assert page.is_logged_in(), "Precondition failed: should be logged in before testing logout"
        # Act
        page.logout()
        time.sleep(1)
        # Assert
        assert not page.is_logged_in(), "Expected to be logged out"
        assert page.is_login_link_visible(), "Expected 'Log in' link to be visible after logout"

# Test 3 - Contact form submission
class TestContactForm:
    def test_contact_form_submission(self, driver):
        # Arrange
        page = HomePage(driver)
        page.load()
        # Act
        page.submit_contact(
            email="test@example.com",
            name="Test User",
            message="Ayyy this is a test message."
        )
        alert_text = page.accept_alert()
        # Assert
        assert "Thanks for the message!!" in alert_text, "Expected confirmation message in alert"

# Test 4 - Products list loads
class TestProductsList:
    def test_products_list_loads(self, driver):
        # Arrange
        page = HomePage(driver)
        # Act
        page.load()
        # Assert
        count = page.product_tile_count()
        assert count >= 9, f"Expected at least 9 product tiles on the home page, got {count}"

# Test 5 - Product details page
class TestProductDetailsPage:
    def test_product_details_page(self, driver):
        # Arrange
        home = HomePage(driver)
        home.load()
        product_names_before = home.product_names()
        expected_name = product_names_before[0]  # just click the first product
        # Act
        home.click_first_product()
        product_page = ProductPage(driver)
        # Assert
        assert "prod.html" in product_page.current_url(), (
            "URL should contain 'prod.html' for a product details page"
        )
        assert expected_name.lower() in product_page.title().lower(), (
            f"Product title mismatch: expected '{expected_name}', "
            f"got '{product_page.title()}'"
        )
        assert "$" in product_page.price() or product_page.price() != "", (
            "Product price should be non-empty"
        )
    
# Test 6 - Category filter
class TestCategoryFilter:
    # Known products per category (as of 5/2/26)
    PHONE_PRODUCTS = [
        "Samsung galaxy s6",
        "Nokia lumia 1520",
        "Nexus 6",
        "Samsung galaxy s7",
        "Iphone 6 32gb",
        "Sony xperia z5",
        "HTC One M9"
    ]
    def test_phone_category_filter(self, driver):
        # Arrange
        page = HomePage(driver)
        page.load()
        # Act
        page.filter_by_phones()
        displayed_products = page.product_names()
        # Assert
        assert len(displayed_products) > 0, "Expected some products to be displayed after filtering by phones"
        for name in displayed_products:
            assert any(expected.lower() in name.lower() for expected in self.PHONE_PRODUCTS), (
                f"Unexpected product '{name}' found after filtering by phones"
            )

# Test 7 - Add to cart
class TestAddToCart:
    def test_add_to_cart(self, driver):
        # Arrange
        home = HomePage(driver)
        home.load()
        home.click_first_product()
        product_page = ProductPage(driver)
        product_name = product_page.title()
        # Act
        alert_text = product_page.add_to_cart()
        time.sleep(1.5)  # allow server to persist the cart item
        # Assert
        assert "Product added" in alert_text, "Expected confirmation message in alert after adding to cart"
        # Navigate to cart and verify the product is there
        cart_page = CartPage(driver)
        cart_page.load()
        assert cart_page.is_product_in_cart(product_name), (
            f"Expected product '{product_name}' to be in cart, but it was not found"
        )

# Test 8 - Cart page loads
class TestCartPage:
    def test_cart_page_loads_with_item(self, driver):
        # Arrange — add a product first
        home = HomePage(driver)
        home.load()
        home.click_first_product()
        product_page = ProductPage(driver)
        product_title = product_page.title()
        product_page.add_to_cart()
        time.sleep(1.5)  # allow server to persist the cart item

        # Act
        cart = CartPage(driver)
        cart.load()

        # Assert
        assert cart.row_count() >= 1, "Cart table should have at least one row"
        assert cart.is_product_in_cart(product_title), (
            f"Expected '{product_title}' to be present in the cart"
        )

# Test 9 - Place order
class TestPlaceOrder:
    def test_place_order(self, driver):
        # Arrange - add a product to cart first
        home = HomePage(driver)
        home.load()
        home.click_first_product()
        product_page = ProductPage(driver)
        product_page.add_to_cart()
        time.sleep(1.5)  # allow server to persist the cart item

        cart = CartPage(driver)
        cart.load()
        cart.open_place_order()  # just to verify the cart page is interactive
        cart.fill_order_form(
            name="Test User",
            country="Testland",
            city="Testville",
            card="1234567890123456",
            month="12",
            year="2025"
        )
        # Act
        confirmation_text = cart.confirm_purchase()
        # Assert
        assert "Id: " in confirmation_text and "Amount: " in confirmation_text, (
            "Expected order confirmation text to contain 'Id' and 'Amount'"
        )
        cart.dismiss_confirmation()

# Test 10 - Remove product from cart
class TestRemoveProductFromCart:
    def test_remove_product_from_cart(self, driver):
        # Arrange — add a product first
        home = HomePage(driver)
        home.load()
        home.click_first_product()
        product_page = ProductPage(driver)
        product_title = product_page.title()
        product_page.add_to_cart()
        time.sleep(1.5)  # allow server to persist the cart item

        cart = CartPage(driver)
        cart.load()
        initial_count = cart.row_count()
        assert initial_count >= 1, "Pre-condition: cart must have at least 1 item"

        # Act
        cart.delete_first_item()

        # Assert
        assert not cart.is_product_in_cart(product_title), (
            f"'{product_title}' should have been removed from the cart"
        )

# Test 11 - Create account
class TestCreateAccount:
    def test_create_account(self, driver):
        # Arrange — generate a unique username so the account doesn't already exist
        unique_username = "testuser_" + uuid.uuid4().hex[:8]
        unique_password = NEW_USER_PASSWORD
        page = HomePage(driver)
        page.load()

        # Act — sign up
        page.signup(unique_username, unique_password)
        signup_alert = page.accept_alert()

        # Assert sign-up succeeded
        assert "Sign up successful" in signup_alert, (
            f"Unexpected sign-up alert: '{signup_alert}'"
        )

        # Act — log in with new credentials
        page.login(unique_username, unique_password)
        time.sleep(1.5)

        # Assert login succeeded
        assert page.is_logged_in(), "Login with new credentials should succeed"
        assert unique_username in page.navbar_username()

#  Test 12 - Pagination
class TestPagination:
    def test_next_then_previous_returns_original_set(self, driver):
        # Arrange
        page = HomePage(driver)
        page.load()
        original_names = page.product_names()
        assert len(original_names) > 0, "Pre-condition: products must load"

        # Act
        page.click_next()
        next_names = page.product_names()

        page.click_prev()
        returned_names = page.product_names()

        # Assert — product set changed on Next, then restored on Previous
        assert next_names != original_names, (
            "Next page should show a different product set"
        )
        assert returned_names != next_names, (
            "Previous should show different products than the next page"
        )
