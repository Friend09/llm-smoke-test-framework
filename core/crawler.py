# core/crawler.py - Add your implementation here

"""4. Web Crawler"""

# core/crawler.py
import os
import json
import time
import logging
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import Config
from core.auth_handler import AuthHandler
from utils.url_extractor import URLExtractor
from utils.element_finder import ElementFinder

logger = logging.getLogger(__name__)


class WebCrawler:
    """
    Web crawler that discovers all pages and interactive elements
    in a web application, handling authentication as needed.
    """

    def __init__(self, base_url: str, config: Config):
        """Initialize the WebCrawler with base URL and configuration."""
        self.base_url = base_url
        self.config = config
        self.driver = None
        self.visited_urls = set()
        self.page_data = {}  # Store page data
        self.url_queue = []  # Queue for URLs to visit
        self.setup_driver()

    def setup_driver(self):
        """Configure and initialize the WebDriver"""
        options = ChromeOptions()
        if self.config.HEADLESS:
            options.add_argument('--headless')

        # Add any additional Chrome options from config
        for option in self.config.BROWSER_OPTIONS:
            if option:
                options.add_argument(option)

        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(
                    ChromeDriverManager().install()
                ),
                options=options
            )

            # Set timeouts
            self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)

            logger.debug("WebDriver initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

        # Initialize auth handler
        self.auth_handler = AuthHandler(self.driver)

    def start_crawling(self, max_depth=None, auth_type=None):
        """
        Start crawling the web application.

        Args:
            max_depth (int): Maximum depth to crawl
            auth_type (str): Authentication type to use

        Returns:
            dict: Discovered pages and their data
        """
        max_depth = max_depth or self.config.MAX_DEPTH
        self.page_data = {}  # Reset page data
        self.url_queue = []  # Reset URL queue

        try:
            logger.info(f"Starting crawl at {self.base_url}")
            self.driver.get(self.base_url)

            if auth_type or self.config.AUTH_TYPE:
                auth_successful = self.auth_handler.authenticate(auth_type or self.config.AUTH_TYPE)
                if not auth_successful:
                    logger.error("Authentication failed, continuing crawl without authentication")
                    self._take_screenshot("auth_failed")

            # Start with the base URL
            self.url_queue.append({
                "url": self.base_url,
                "depth": 0,
                "source": "initial"
            })

            while self.url_queue and self.url_queue[0]["depth"] <= max_depth:
                current = self.url_queue.pop(0)
                current_url = current["url"]
                current_depth = current["depth"]

                if current_url in self.visited_urls:
                    continue

                logger.info(f"Crawling {current_url} (depth {current_depth})")

                try:
                    self.driver.get(current_url)
                    WebDriverWait(self.driver, self.config.PAGE_LOAD_TIMEOUT).until(
                        lambda d: d.execute_script("return document.readyState") == "complete"
                    )

                    self.visited_urls.add(current_url)
                    page_data = self._extract_page_data(current_url, current_depth, current["source"])
                    self.page_data[current_url] = page_data

                    if current_depth < max_depth:
                        self._extract_and_queue_urls(current_url, current_depth)

                except (TimeoutException, WebDriverException) as e:
                    logger.warning(f"Error accessing {current_url}: {str(e)}")
                    self._take_screenshot(f"error_{current_url.replace('/', '_')}")
                    continue

                time.sleep(1)

            logger.info(f"Crawl completed. Visited {len(self.visited_urls)} pages.")
            self._save_results()
            return self.page_data

        finally:
            if self.driver:
                self.driver.quit()

    def _extract_page_data(self, url, depth, source):
        """
        Extract data from the current page.

        Args:
            url (str): URL of the page
            depth (int): Depth of the page in the crawl
            source (str): Source URL or element that led to this page

        Returns:
            dict: Page data
        """
        # Initialize the data structure
        page_data = {
            "url": url,
            "title": self.driver.title,
            "depth": depth,
            "source": source,
            "elements": [],
        }

        # Use the ElementFinder to identify important UI elements
        element_finder = ElementFinder(self.driver)

        # Get interactive elements
        interactive_elements = element_finder.find_interactive_elements()
        page_data["elements"] = interactive_elements

        # Detect frames/iframes
        frames = element_finder.find_frames()
        page_data["frames"] = frames

        # Detect form elements
        forms = element_finder.find_forms()
        page_data["forms"] = forms

        # Capture page structure (heading hierarchy)
        headings = element_finder.find_headings()
        page_data["headings"] = headings

        return page_data

    def _extract_and_queue_urls(self, current_url, current_depth):
        """
        Extract URLs from the current page and add them to the queue.

        Args:
            current_url (str): URL of the current page
            current_depth (int): Depth of the current page
        """
        # Extract URLs
        url_extractor = URLExtractor(
            self.driver,
            self.config.BASE_URL,
            self.config.EXCLUDE_PATTERNS,
            self.config.INCLUDE_SUBDOMAINS,
        )

        new_urls = url_extractor.extract_urls()

        # Add new URLs to the queue
        for url in new_urls:
            if url not in self.visited_urls and url not in [
                item["url"] for item in self.url_queue
            ]:
                self.url_queue.append(
                    {"url": url, "depth": current_depth + 1, "source": current_url}
                )

    def _save_results(self):
        """Save crawl results to file."""
        # Create output directory if it doesn't exist
        output_dir = os.path.join(self.config.OUTPUT_DIR, "discovered_pages")
        os.makedirs(output_dir, exist_ok=True)

        # Save all pages data
        output_file = os.path.join(output_dir, "all_pages.json")
        with open(output_file, "w") as f:
            json.dump(self.page_data, f, indent=2)

        # Save page map (showing the relationship between pages)
        page_map = {}
        for url, data in self.page_data.items():
            page_map[url] = {
                "title": data["title"],
                "depth": data["depth"],
                "source": data["source"],
            }

        map_file = os.path.join(output_dir, "page_map.json")
        with open(map_file, "w") as f:
            json.dump(page_map, f, indent=2)

        # Save HTML content of each page
        for url, data in self.page_data.items():
            self._save_page_content(url, data.get("html_content", ""))

        logger.info(f"Saved crawl results to {output_dir}")

    def _save_page_content(self, url, content):
        """Save the HTML content of the page to a file."""
        # Create a safe filename from the URL
        safe_filename = self._safe_filename(url)
        output_dir = os.path.join(self.config.OUTPUT_DIR, "discovered_pages")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{safe_filename}.html")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Saved page content to {output_file}")

    def _safe_filename(self, url):
        """Convert URL to a safe filename."""
        # Remove protocol and replace special characters
        filename = url.split("://")[-1].replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
        return filename

    def _take_screenshot(self, name):
        """Take a screenshot for debugging purposes."""
        screenshot_path = os.path.join(self.config.OUTPUT_DIR, "screenshots", f"{name}.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"Saved screenshot: {screenshot_path}")

    def _is_valid_url(self, url: str) -> bool:
        """Check if a URL should be crawled."""
        if not url:
            return False

        parsed_url = urllib.parse.urlparse(url)
        base_parsed = urllib.parse.urlparse(self.base_url)

        # Check if URL is in same domain
        if not self.config.INCLUDE_SUBDOMAINS:
            if parsed_url.netloc != base_parsed.netloc:
                return False
        else:
            if not parsed_url.netloc.endswith(base_parsed.netloc):
                return False

        # Check exclude patterns
        for pattern in self.config.EXCLUDE_PATTERNS:
            if pattern in url:
                return False

        return True

    def _normalize_url(self, url: str) -> str:
        """Normalize URL to avoid duplicates."""
        parsed = urllib.parse.urlparse(url)
        # Remove fragments
        normalized = parsed._replace(fragment='')
        # Remove trailing slash
        path = normalized.path
        if path.endswith('/'):
            path = path[:-1]
        return urllib.parse.urlunparse(normalized._replace(path=path))
