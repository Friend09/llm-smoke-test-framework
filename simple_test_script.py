import pytest
from runners.crawler_runner import main
from config.config import Config

def test_crawler_basic():
    """Test basic crawler functionality with a simple website"""
    config = Config()
    config.BASE_URL = "https://example.com"
    config.MAX_DEPTH = 1
    config.HEADLESS = True

    result = main()
    assert result == 0

def test_crawler_with_auth():
    """Test crawler with authentication"""
    config = Config()
    config.BASE_URL = "https://github.com"
    config.AUTH_TYPE = "form"
    config.USERNAME = "test_user"  # Replace with actual test credentials
    config.PASSWORD = "test_pass"
    config.MAX_DEPTH = 1

    result = main()
    assert result == 0
