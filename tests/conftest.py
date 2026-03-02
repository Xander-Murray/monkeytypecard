import sys
import os

# Make src/ importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
import app as app_module
import services.monkeytype as mt_service


@pytest.fixture
def client():
    """Flask test client."""
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def _clear_rate_limits():
    """Reset rate-limit state between tests."""
    app_module._rate_limits.clear()
    yield
    app_module._rate_limits.clear()


@pytest.fixture(autouse=True)
def _clear_profile_cache():
    """Reset profile cache between tests."""
    mt_service._profile_cache.clear()
    yield
    mt_service._profile_cache.clear()
