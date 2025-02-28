# tests/integration/test_crawler_basic.py - Add your implementation here

import pytest
import os
import sys
import json
from unittest.mock import patch

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.config import Config
from core.crawler import WebCrawler

# Skip these tests if no real browser is available
pytestmark = pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Skipping browser tests in CI environment"
)

class TestCrawlerBasic:
    """Integration tests for the WebCrawler class."""

    @pytest.fixture
    def test_config(self):
        """Create a test configuration."""
        with patch.dict(os.environ, {
            "BASE_URL": "https://example.com",
            "HEADLESS": "True",
            "MAX_DEPTH": "1",
            "OUTPUT_DIR": "test_output"
        }):
            return Config()

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for tests."""
        # Setup
        os.makedirs("test_output/discovered_pages", exist_ok=True)

        yield

        # Teardown - clean up test output
        try:
            import shutil
            if os.path.exists("test_output"):
                shutil.rmtree("test_output")
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def test_crawler_initialization(self, test_config):
        """Test crawler initialization."""
        crawler = WebCrawler(test_config.BASE_URL, test_config)

        assert crawler.start_url == "https://example.com"
        assert crawler.driver is not None
        assert crawler.auth_handler is not None
        assert len(crawler.visited_urls) == 0
        assert len(crawler.url_queue) == 0

    @pytest.mark.skip(reason="Requires internet connection and external site")
    def test_basic_crawl(self, test_config):
        """Test basic crawling functionality."""
        # This is marked as skip since it would make actual network requests
        # In a real implementation, you might use a local test server

        test_config.MAX_DEPTH = 1  # Limit depth for test
        crawler = WebCrawler(test_config.BASE_URL, test_config)

        try:
            page_data = crawler.start_crawling(test_config.MAX_DEPTH)

            # Verify crawler discovered at least the start page
            assert len(page_data) >= 1
            assert test_config.BASE_URL in page_data

            # Verify output files were created
            assert os.path.exists("test_output/discovered_pages/all_pages.json")
            assert os.path.exists("test_output/discovered_pages/page_map.json")

            # Verify content of output files
            with open("test_output/discovered_pages/all_pages.json", "r") as f:
                saved_data = json.load(f)
                assert len(saved_data) >= 1

        finally:
            # Ensure driver is quit even if test fails
            if crawler.driver:
                crawler.driver.quit()
