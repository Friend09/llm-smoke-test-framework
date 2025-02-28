# tests/unit/test_url_extractor.py - Add your implementation here

import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.url_extractor import URLExtractor

class TestURLExtractor:
    """Unit tests for the URLExtractor class."""

    @pytest.fixture
    def mock_driver(self):
        """Create a mock Selenium WebDriver."""
        driver = MagicMock()
        driver.page_source = """
        <html>
            <body>
                <a href="https://example.com/page1">Page 1</a>
                <a href="/relative/path">Relative Link</a>
                <a href="#">Anchor</a>
                <a href="javascript:void(0)">JavaScript Link</a>
                <form action="/submit">
                    <input type="text" name="query">
                    <button type="submit">Submit</button>
                </form>
                <iframe src="/iframe-content"></iframe>
            </body>
        </html>
        """
        driver.current_url = "https://example.com/"
        return driver

    def test_extract_with_beautifulsoup(self, mock_driver):
        """Test URL extraction using BeautifulSoup."""
        extractor = URLExtractor(mock_driver, "https://example.com", [], True)

        # Mock BeautifulSoup
        with patch('utils.url_extractor.BeautifulSoup') as mock_bs:
            # Set up mock soup
            mock_soup = MagicMock()
            mock_bs.return_value = mock_soup

            # Set up mock anchor tags
            a1, a2 = MagicMock(), MagicMock()
            a1.__getitem__.return_value = "https://example.com/page1"
            a2.__getitem__.return_value = "/relative/path"
            mock_soup.find_all.return_value = [a1, a2]

            # Call the method
            result = extractor._extract_with_beautifulsoup()

            # Verify calls
            mock_bs.assert_called_once_with(mock_driver.page_source, 'html.parser')
            assert mock_soup.find_all.call_count >= 1

            # Verify results
            assert "https://example.com/page1" in result
            assert "/relative/path" in result

    def test_normalize_urls(self, mock_driver):
        """Test URL normalization."""
        extractor = URLExtractor(mock_driver, "https://example.com", ["logout", "#"], True)

        # Test URLs to normalize
        test_urls = [
            "https://example.com/page1",  # Absolute URL - keep
            "/relative/path",             # Relative URL - convert to absolute
            "#anchor",                    # Anchor - exclude
            "javascript:void(0)",         # JavaScript - exclude
            "https://example.com/logout", # Contains excluded pattern - exclude
            "other/page",                 # Relative without leading slash - convert to absolute
            "https://other-domain.com"    # Different domain - exclude if not including subdomains
        ]

        # Call the method
        result = extractor._normalize_urls(test_urls)

        # Verify results
        assert "https://example.com/page1" in result
        assert "https://example.com/relative/path" in result
        assert "https://example.com/other/page" in result
        assert "#anchor" not in result
        assert "javascript:void(0)" not in result
        assert "https://example.com/logout" not in result

        # Test with subdomains disabled
        extractor.include_subdomains = False
        result = extractor._normalize_urls(["https://other-domain.com"])
        assert "https://other-domain.com" not in result
