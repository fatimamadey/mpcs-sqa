# Demoblaze E2E Test Suite

Automated end-to-end tests for [demoblaze.com](https://www.demoblaze.com/).

- **Exercise 1** — 12 happy-path tests using **Selenium**, run against **Chrome** and **Firefox**.
- **Exercise 2** — 5 unhappy-path tests using **Playwright**, with automatic screenshots.

---

## Project Structure

```
assignment4/
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # Shared helpers (waits, alert utils, navbar checks)
│   ├── home_page.py        # Home / product list / auth / contact / pagination
│   ├── product_page.py     # Individual product details page
│   └── cart_page.py        # Shopping cart + order flow
│
├── tests/
│   ├── selenium/
│   │   └── test_happy_path.py   # Exercise 1 — 12 happy-path Selenium tests
│   └── playwright/
│       ├── conftest.py          # Screenshot fixture
│       └── test_unhappy_path.py # Exercise 2 — 5 unhappy-path Playwright tests
│
├── screenshots/             # Auto-populated by Exercise 2 tests
├── reports/                 # Generated HTML reports
├── conftest.py              # Root conftest — Selenium browser parametrization
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9+ |
| Chrome | Latest (ChromeDriver managed automatically by Selenium 4) |
| Firefox | Latest (GeckoDriver managed automatically by Selenium 4) |

---

## Setup

```bash
# 1. Clone / unzip the project and enter the folder
cd assignment4

# 2. (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright's Chromium browser
python3 -m playwright install chromium
```

---

## Running the Tests

### Run ALL tests (both exercises)

```bash
pytest
```

### Run only Exercise 1 (Selenium, both browsers)

```bash
pytest tests/selenium/
```

### Run only Exercise 2 (Playwright)

```bash
pytest tests/playwright/
```

### Run a single test by name

```bash
pytest tests/selenium/test_happy_path.py::TestLogin::test_login_valid_credentials
pytest tests/playwright/test_unhappy_path.py::TestInvalidInput::test_login_with_invalid_password
```

### Generate an HTML report

```bash
pytest tests/selenium/ --html=reports/selenium_report.html --self-contained-html
pytest tests/playwright/ --html=reports/playwright_report.html --self-contained-html
```

---

## Switching Browsers (Exercise 1)

By default every Selenium test runs against **both Chrome and Firefox**.

```bash
# Chrome only
pytest tests/selenium/ --sel-browser=chrome

# Firefox only
pytest tests/selenium/ --sel-browser=firefox
```

The `--sel-browser` option is defined in `conftest.py` and parametrizes all
tests that use the `driver` fixture automatically — no changes to the test
files are needed.

---

## Screenshots (Exercise 2)

A screenshot is captured **after every Playwright test** (pass or fail) and
saved to `screenshots/` with a category-based filename.

```
screenshots/
├── 01_invalid_input.png       # Invalid input     — login with wrong password
├── 02_boundary_edge.png       # Boundary / edge   — place order with empty cart
├── 03_equivalence_class.png   # Equivalence class — sign-up with duplicate username
├── 04_exception_handling.png  # Exception handling — contact form with empty fields
└── 05_business_logic.png      # Business logic    — add same product to cart twice
```

---

## Test Overview

### Exercise 1 — Happy Path (Selenium)

| # | Test class | Area |
|---|---|---|
| 1 | `TestLogin` | Login with valid credentials |
| 2 | `TestLogout` | Logout |
| 3 | `TestContactForm` | Contact form submission |
| 4 | `TestProductsList` | Products list loads (≥ 9 tiles) |
| 5 | `TestProductDetailsPage` | Product details page |
| 6 | `TestCategoryFilter` | Category filter (Phones) |
| 7 | `TestAddToCart` | Add to cart |
| 8 | `TestCartPage` | Cart page loads with item |
| 9 | `TestPlaceOrder` | Place order |
| 10 | `TestRemoveProductFromCart` | Remove product from cart |
| 11 | `TestCreateAccount` | Create account + login |
| 12 | `TestPagination` | Next → Previous pagination |

### Exercise 2 — Unhappy Path (Playwright)

| # | Category | Test class | Area tested |
|---|---|---|---|
| 1 | Invalid input | `TestInvalidInput` | Login — wrong password |
| 2 | Boundary / edge | `TestBoundaryEdge` | Cart — place order with empty cart |
| 3 | Equivalence class | `TestEquivalenceClass` | Sign-up — duplicate username |
| 4 | Exception handling | `TestExceptionHandling` | Contact — empty form submission |
| 5 | Business logic | `TestBusinessLogic` | Cart — add same product twice |

---

## Sources

- https://selenium-python.readthedocs.io/index.html
- https://playwright.dev/python/docs/intro
- Copilot autocomplete to help write page object and scaffolding.
- I also consulted Claude on a few issues I ran into as well as writing my conftest.py.
- I used autocomplete for the top portion of this README as well but wrote the reflection myself!

---

## Reflection

**Which framework was easier to set up?** Playwright was much easier. `playwright install chromium`
genuinely handles everything. Selenium wasn't *hard*, but it had so many extra steps I didn't expect 
as I began to implement it. The one that really got me and took me embarassingly long to debug was 
the fact that `pytest-playwright` registers its own `--browser` CLI option, and my custom
Selenium option in `conftest.py` was also named `--browser`. Pytest crashed at startup with an
`ArgumentError` that traced to `argparse`. I stared at the traceback for a while before I realized
the collision wasn't in my code at all but the two plugins were fighting over the same flag name. Renaming
mine to `--sel-browser` and scoping `pytest_generate_tests` to only fire for tests that also request
a `driver` fixture fixed it.

**Hardest test:** `TestPagination` was the hardest for me. The demoblaze product grid is AJAX-driven 
and doesn't trigger a page reload, so I couldn't use a navigation event to know when the new products 
had settled. I tried `WebDriverWait` but the list sometimes updates in place without the
elements going stale. I instead used `time.sleep()`, which felt like cheating, and even then I had to 
loosen the assertion. I originally wanted to verify that "Previous" returned the exact same products I started 
with. But it doesn't the demo site returns products non-deterministically on each AJAX call. So I asserted that the
product set changed when navigating, which is weaker but at least checks something.

**Browser difference:** The `add_to_cart` test was reliable on Chrome but occasionally timed out on
Firefox. The confirmation alert fires almost immediately after clicking "Add to cart," and Firefox's
driver was still settling from the page navigation when the alert appeared, causing a
`TimeoutException` that Chrome never hit. Adding `time.sleep(1.5)` after the add resolved it for both
browsers. 

**Where I got stuck:** `TestCreateAccount`. The first run passed but the second run failed. The site
rejected the signup with "This user already exist." I had hardcoded `"newuser"` as the test credential,
and demoblaze persists accounts between runs. I first tried to add a teardown that deleted the account, 
but demoblaze has no delete-user endpoint. My second idea was a timestamp suffix, which works
but litters the server with test accounts forever. I asked claude and it recommended using `uuid.uuid4().hex[:8]` 
as a random suffix since it is cheap, collision-resistant, no cleanup needed.

**Framework for my next project:** Playwright. It was much easier to set up and use without much thought.
