import os
import sys
import django
import pytest

APP_DIR = os.path.join(os.path.dirname(__file__), "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")


# ── shared fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "http://127.0.0.1:8000")
