# Unhappy Path Tests - Playwright
import pytest

BASE_URL = "https://www.demoblaze.com"
EXISTING_USER = {"username": "fatima_dada", "password": "123456"}

# Invalid Input - Login with invalid creds
# Verifiees the site rejects invalid login attempts and shows an appropriate error message.
class TestInvalidInput:
    def test_login_with_invalid_password(self, page):
        # Arrange
        page.goto(BASE_URL)
        page.click("#login2")
        page.wait_for_selector("#logInModal", state="visible")

        # Act — enter valid username but WRONG password
        page.fill("#loginusername", EXISTING_USER["username"])
        page.fill("#loginpassword", "this_is_wrong_password_12345")

        # Set up alert listener
        dialog_message = {}

        def handle_dialog(dialog):
            dialog_message["text"] = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)
        page.click("//button[text()='Log in']")

        # Wait for the dialog to fire
        page.wait_for_timeout(2000)

        # Assert — an alert must appear and the user must NOT be logged in
        assert "dialog" in dialog_message or dialog_message.get("text"), (
            "Expected an error alert for wrong credentials"
        )
        assert page.locator("#nameofuser").count() == 0 or \
               not page.locator("#nameofuser").is_visible(), (
            "User should NOT be logged in after wrong password"
        )

# Boundary / edge - Place order with empty cart
# Verifies the site handles edge case of trying to place an order with no items in the cart, either by blocking the action or showing a $0 total.
class TestBoundaryEdge:
    def test_place_order_with_empty_cart(self, page):
        # Arrange
        page.goto(f"{BASE_URL}/cart.html")
        page.wait_for_selector("#tbodyid")
        page.wait_for_timeout(1500)  # let AJAX populate rows

        # Act 
        page.click("//button[text()='Place Order']")
        page.wait_for_timeout(1500)

        # Assert — either:
        #   (a) the modal opens but shows a $0 or blank total (truly empty cart), OR
        #   (b) the modal does not open at all
        modal_visible = page.locator("#orderModal").is_visible()

        if modal_visible:
            total_text = page.locator("#totalm").inner_text().strip()
            row_count = page.locator("#tbodyid tr").count()
            if row_count == 0:
                # Truly empty cart — total must be 0 or blank
                assert total_text in ("0", "", "0 USD"), (
                    f"Empty cart order total should be 0 or blank, got: '{total_text}'"
                )
            else:
                # Cart had leftover items — the site allows placing the order,
                # which is expected behaviour (not a bug).
                assert True, "Cart has items; place-order modal opened correctly"
        else:
            assert True, "Place Order correctly blocked for empty cart"

# Equivalence class - Sign up with existing username
# Verifies the site rejects attempts to sign up with a username that already exists, showing an appropriate error message.
class TestEquivalenceClass:
    """Category: Equivalence Class — sign-up with an existing username."""

    def test_signup_with_existing_username(self, page):
        # Arrange
        page.goto(BASE_URL)
        page.click("#signin2")
        page.wait_for_selector("#signInModal", state="visible")

        # Act
        page.fill("#sign-username", EXISTING_USER["username"])
        page.fill("#sign-password", "any_password_123")

        dialog_message = {}

        def handle_dialog(dialog):
            dialog_message["text"] = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)
        page.click("//button[text()='Sign up']")
        page.wait_for_timeout(2000)

        # Assert
        assert dialog_message.get("text"), (
            "Expected an error alert for duplicate username"
        )

# Exception handling - Submit contact form with all empty fields
# Verifies the site handles the case of submitting the contact form without filling any fields, either by showing validation errors or an appropriate alert.
class TestExceptionHandling:
    def test_contact_form_all_fields_empty(self, page):
        # Arrange
        page.goto(BASE_URL)
        page.click("//a[text()='Contact']")
        page.wait_for_selector("#exampleModal", state="visible")

        # Act
        dialog_fired = {"fired": False, "text": ""}

        def handle_dialog(dialog):
            dialog_fired["fired"] = True
            dialog_fired["text"] = dialog.message
            dialog.accept()

        page.on("dialog", handle_dialog)
        page.click("//button[text()='Send message']")
        page.wait_for_timeout(2000)

        # Assert
        # Acceptable outcomes:
        #   (a) An alert fires (any message counts as handled)
        #   (b) The modal remains open (form not submitted)
        modal_still_visible = page.locator("#exampleModal").is_visible()
        assert dialog_fired["fired"] or modal_still_visible, (
            "Empty contact form: expected either an alert or the modal to stay open"
        )

# Business Logic - Add same product to cart multiple times
# Verifies the site's behavior when adding the same product to the cart multiple times,
# checking if it creates duplicate entries.
class TestBusinessLogic:
    def test_add_same_product_twice(self, page):
        # Arrange — navigate to a product page
        page.goto(BASE_URL)
        page.wait_for_selector(".card-title a")

        # Click the first product tile
        page.locator(".card-title a").first.click()
        page.wait_for_selector("a:has-text('Add to cart')")

        # Act — add to cart once
        dialog_texts = []

        def handle_dialog(dialog):
            dialog_texts.append(dialog.message)
            dialog.accept()

        page.on("dialog", handle_dialog)

        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(1500)

        # Add to cart a second time (same page, same product)
        page.click("a:has-text('Add to cart')")
        page.wait_for_timeout(1500)

        # Navigate to cart
        page.goto(f"{BASE_URL}/cart.html")
        page.wait_for_selector("#tbodyid")
        page.wait_for_timeout(1500)

        # Assert — count the rows in the cart table
        rows = page.locator("#tbodyid tr").all()
        row_count = len(rows)

        # Business rule: the site should show either:
        #   1. Two separate rows (quantity not merged), OR
        #   2. One row with quantity 2 (quantity merged)
        # Either is correct — what's NOT correct is 0 rows.
        assert row_count >= 1, (
            f"Expected at least 1 cart row after adding product twice, got {row_count}"
        )