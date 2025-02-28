# core/crawler.py - Add your implementation here

"""4. Web Crawler"""

# core/crawler.py
import os
import json
import time
import logging
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

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

    def __init__(self, start_url=None, config=None):
        """
        Initialize the crawler.

        Args:
            start_url (str): URL to start crawling from
            config (Config): Configuration object
        """
        self.config = config or Config()
        self.start_url = start_url or self.config.BASE_URL
        self.driver = None
        self.auth_handler = None
        self.visited_urls = set()
        self.url_queue = []
        self.page_data = {}
        self.setup_driver()

    def setup_driver(self):
        """Set up the Selenium WebDriver."""
        if self.config.BROWSER.lower() == "chrome":
            options = Options()
            if self.config.HEADLESS:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=options)
        else:
            # Support for other browsers can be added here
            raise ValueError(f"Unsupported browser: {self.config.BROWSER}")

        # Set timeouts
        self.driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)

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

        try:
            # Navigate to start URL
            logger.info(f"Starting crawl at {self.start_url}")
            self.driver.get(self.start_url)

            # Handle authentication if needed
            if auth_type or self.config.AUTH_TYPE:
                auth_successful = self.auth_handler.authenticate(auth_type)
                if not auth_successful:
                    logger.error("Authentication failed, aborting crawl")
                    return {}

            # Add start URL to queue
            self.url_queue.append(
                {"url": self.driver.current_url, "depth": 0, "source": "initial"}
            )

            # Process URL queue breadth-first
            while self.url_queue and self.url_queue[0]["depth"] <= max_depth:
                current = self.url_queue.pop(0)
                current_url = current["url"]
                current_depth = current["depth"]

                # Skip if already visited
                if current_url in self.visited_urls:
                    continue

                logger.info(f"Crawling {current_url} (depth {current_depth})")

                try:
                    # Visit the URL
                    self.driver.get(current_url)

                    # Wait for page to load
                    WebDriverWait(self.driver, self.config.PAGE_LOAD_TIMEOUT).until(
                        lambda d: d.execute_script("return document.readyState")
                        == "complete"
                    )

                    # Mark as visited
                    self.visited_urls.add(current_url)

                    # Extract page data
                    page_data = self._extract_page_data(
                        current_url, current_depth, current["source"]
                    )
                    self.page_data[current_url] = page_data

                    # Extract URLs from the page
                    if current_depth < max_depth:
                        self._extract_and_queue_urls(current_url, current_depth)

                except (TimeoutException, WebDriverException) as e:
                    logger.warning(f"Error accessing {current_url}: {str(e)}")
                    continue

                # Small delay to avoid overloading the server
                time.sleep(1)

            logger.info(f"Crawl completed. Visited {len(self.visited_urls)} pages.")
            self._save_results()
            return self.page_data

        finally:
            # Clean up
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

        logger.info(f"Saved crawl results to {output_dir}")
