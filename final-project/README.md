# Django Poll App – Final Project

> **MPCS Software Quality Assurance – Final Project**  
> Fatima Madey | Spring 2026

Applies QA concepts from the course to the open-source **Django Poll App**:  
<https://github.com/devmahmud/Django-Poll-App>

---

## AI / Tools Disclosure

- Used Claude to help create README below and analyze my results in Q4.

---

## Project Structure

```
final-project/
├── app/                          ← Cloned Django Poll App source
│   ├── polls/                    ← Main polls application
│   ├── accounts/                 ← Auth (register / login / logout)
│   ├── pollme/                   ← Django project settings + URLs
│   └── manage.py
│
├── tests/
│   ├── unit/
│   │   └── test_models.py        ← Q3: 11 unit tests (Stub, Mock, Fake, Dummy)
│   ├── integration/
│   │   └── test_integration.py   ← Q7: 2 integration tests (View ↔ DB / Template)
│   └── ui/
│       └── playwright/
│           ├── conftest.py       ← Screenshot-on-failure fixture
│           └── test_e2e.py       ← Q5: 5 Playwright end-to-end tests
│
├── performance/
│   ├── loadtest.js               ← Q4: k6 load test  (0→50 VUs, 2 min steady)
│   └── spiketest.js              ← Q4: k6 spike test (10→200 VUs instant spike)
│
├── .github/
│   └── workflows/
│       └── ci.yml                ← Q9: GitHub Actions CI/CD pipeline
│
├── screenshots/                  ← Auto-populated by UI test failures
├── htmlcov/                      ← Auto-generated coverage HTML report
├── .flake8                       ← Q1: flake8 linter configuration
├── conftest.py                   ← Root pytest fixtures
├── pytest.ini                    ← pytest settings + DJANGO_SETTINGS_MODULE
├── requirements.txt              ← All Python dependencies
└── README.md                     ← This file
```

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | `brew install python` |
| k6 | Latest | `brew install k6` |
| Chromium (Playwright) | auto | `playwright install chromium` |

---

## Setup

```bash
# 1. Enter the final-project directory
cd final-project

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install all Python dependencies
pip install -r requirements.txt

# 4. Install the app's own dependencies
pip install -r app/requirements.txt

# 5. Install Playwright browser
playwright install chromium

# 6. Apply Django migrations (creates the SQLite database)
cd app
python manage.py migrate
python manage.py createsuperuser   # follow prompts to create an admin account
cd ..
```

---

## Q1 – Lint (flake8)

```bash
# Run from the final-project/ root
flake8 app/ --config .flake8
```

The `.flake8` configuration enforces:
- Max line length 100
- Max complexity 10 (McCabe)
- `flake8-bugbear` opinionated warnings
- Skips auto-generated migration files

---

## Q3 – Unit Tests

```bash
pytest tests/unit/ -v --tb=short \
  --cov=polls.models --cov-report=term --cov-report=html:htmlcov
```

8 tests covering `Poll.__str__`, `Choice.__str__`, `Vote.__str__`, poll active default,
`Poll.user_can_vote`, `Poll.get_vote_count`, and `Poll.get_result_dict`.
Coverage is scoped to `polls/models.py` — views and forms are covered by Q7 and Q5.

**Test-double summary:**

| Test | Double type | Real dependency replaced |
|------|------------|--------------------------|
| `test_user_can_vote_no_prior_vote` | Stub | `user.vote_set` queryset |
| `test_user_can_vote_already_voted` | Stub | `user.vote_set` queryset |
| `test_user_can_vote_different_poll` | Stub | `user.vote_set` queryset |
| `test_get_vote_count_calls_count_once` | Mock | `Poll.vote_set.count()` |
| `test_get_vote_count_zero` | Mock | `Poll.vote_set.count()` |
| `test_get_result_dict_even_split` | Fake | `choice_set` queryset + Vote data |
| `test_get_result_dict_no_votes` | Stub | `vote_set` count → 0 |
| `test_poll_str_representation` | Dummy | Minimal Poll object |
| `test_choice_str_representation` | Dummy | Minimal Choice object |
| `test_vote_links_user_poll_and_choice` | Dummy | Minimal Vote/User/Poll/Choice |

---

## Q7 – Integration Tests

```bash
pytest tests/integration/ -v --tb=short
```

| Test | Components | What could go wrong |
|------|-----------|---------------------|
| `test_polls_list_view_returns_polls_from_database` | View ↔ DB | Wrong queryset scope; paginator hides rows; broken migration |
| `test_polls_list_view_renders_correct_template_with_context` | View ↔ Template | Renamed context key; missing template; `search_term` absent |

---

## Q5 – UI Automation (Playwright)

Start the Django development server first:

```bash
cd app && python manage.py runserver
```

Then in a new terminal:

```bash
pytest tests/ui/playwright/ -v --tb=short \
  --screenshot=only-on-failure --output=screenshots/
```

| Test | Interaction |
|------|------------|
| `test_register_new_user` | Fill registration form → verify redirect |
| `test_login_valid_credentials` | Enter credentials → verify not on login page |
| `test_create_poll_with_choices` | Add poll form → verify poll in list |
| `test_submit_vote_and_view_results` | Select choice + submit → verify results page |
| `test_logout_redirects_to_login` | Navigate to logout → verify login redirect |

Override credentials via env vars:

```bash
TEST_ADMIN_USER=myuser TEST_ADMIN_PASS=mypass pytest tests/ui/playwright/ -v
```

---

## Q4 – Performance Tests (k6)

Start the Django development server, then:

```bash
# Load test (0 → 50 VUs, 2-minute steady state)
BASE_URL=http://127.0.0.1:8000 k6 run performance/loadtest.js

# Spike test (10 → 200 VUs instant spike, 1-minute hold)
BASE_URL=http://127.0.0.1:8000 k6 run performance/spiketest.js
```

Both scripts output response-time percentiles (avg, p90, p95, p99), throughput (req/s), and error rate.

---

## Q9 – CI/CD Pipeline

Pipeline defined in [.github/workflows/ci.yml](.github/workflows/ci.yml).

Triggers: every push to `main`, every pull request.

| Job | Description |
|-----|-------------|
| `lint` | Runs `flake8` – fails on any lint error |
| `test` | Runs unit (Q3) + integration (Q7) tests with coverage |
| `ui-tests` | Spins up Django dev server, runs Playwright suite (Q5) |
| `performance` | Validates k6 scripts with `k6 inspect` (dry-run) |

---

## Running the Full Suite Locally

```bash
# From final-project/
pytest tests/unit/ tests/integration/ -v --tb=short \
  --cov=polls.models --cov-report=html:htmlcov

# UI tests (requires running server)
pytest tests/ui/playwright/ -v

# Lint
flake8 app/ --config .flake8
```
