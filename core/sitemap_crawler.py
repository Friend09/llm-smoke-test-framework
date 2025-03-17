import os
import re
import json
import logging
import time
import urllib.parse
from collections import deque
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .crawler import WebCrawler

logger = logging.getLogger(__name__)

class SitemapCrawler:
    """
    Crawler that discovers all accessible pages within a domain and creates a sitemap.
    """

    def __init__(self, config):
        self.config = config
        self.web_crawler = WebCrawler(config)
        self.visited_urls = set()
        self.url_queue = deque()
        self.sitemap = {}
        self.max_pages = 50  # Default limit
        self.output_dir = None

        # Create a dedicated WebDriver for link discovery
        self.use_selenium_for_discovery = True
        self.discovery_driver = None

    def extract_domain(self, url):
        """Extract the domain from a URL."""
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc

    def is_same_domain(self, url, base_domain):
        """Check if a URL belongs to the same domain."""
        return self.extract_domain(url) == base_domain

    def normalize_url(self, url, base_url):
        """Normalize relative URLs to absolute URLs."""
        if not url:
            return None

        # Remove any fragment identifiers
        url = url.split('#')[0]

        # Skip mail and javascript links
        if url.startswith(('mailto:', 'javascript:', 'tel:')):
            return None

        if url.startswith('/'):
            # Relative URL - join with base
            base_parts = urllib.parse.urlparse(base_url)
            return f"{base_parts.scheme}://{base_parts.netloc}{url}"
        elif not url.startswith(('http://', 'https://')):
            # Handle other relative paths
            return urllib.parse.urljoin(base_url, url)

        # Handle canonical forms (with/without trailing slash)
        if url.endswith('/'):
            url_without_slash = url[:-1]
            if url_without_slash in self.visited_urls:
                return None
        else:
            url_with_slash = url + '/'
            if url_with_slash in self.visited_urls:
                return None

        return url

    def should_visit(self, url):
        """Determine if a URL should be visited based on patterns and filters."""
        if not url:
            return False

        # Avoid known file types
        if re.search(r'\.(css|js|jpg|jpeg|png|gif|svg|pdf|zip|ico|xml|webp)$', url, re.I):
            return False

        # Avoid URLs with fragments
        if '#' in url:
            url = url.split('#')[0]
            if url in self.visited_urls:
                return False

        # Avoid specific paths that aren't relevant for test generation
        excluded_patterns = [
            '/wp-admin/',
            '/wp-content/',
            '/wp-includes/',
            '/feed/',
            '/comments/',
            '/trackback/',
            '/page/',  # Pagination URLs
            '/tag/',   # Tag archives
            '/category/', # Category archives
            '/author/',  # Author archives
            'redirect_to=',
            '/cdn-cgi/'
        ]

        for pattern in excluded_patterns:
            if pattern in url:
                return False

        # Avoid URLs with excessive query parameters
        if url.count('?') > 0 and url.count('&') > 5:
            return False

        return url not in self.visited_urls

    def discover_links(self, url):
        """Find all links on a page."""
        links = []

        try:
            # Use Selenium if available for better discovery
            if self.use_selenium_for_discovery:
                if not self.discovery_driver:
                    # Initialize WebDriver if not already done
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--disable-gpu')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')

                    self.discovery_driver = webdriver.Chrome(options=chrome_options)
                    self.discovery_driver.set_page_load_timeout(30)

                # Navigate to URL
                logger.info(f"Using Selenium to discover links on {url}")
                self.discovery_driver.get(url)

                # Wait for the page to load
                try:
                    WebDriverWait(self.discovery_driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(2)  # Give additional time for JS to run
                except TimeoutException:
                    logger.warning(f"Timeout waiting for page to load: {url}")

                # Extract links
                try:
                    elements = self.discovery_driver.find_elements(By.TAG_NAME, "a")
                    for element in elements:
                        try:
                            href = element.get_attribute("href")
                            if href:
                                links.append(href)
                        except StaleElementReferenceException:
                            continue
                except Exception as e:
                    logger.warning(f"Error extracting links with Selenium: {str(e)}")

            # Fallback to requests/BeautifulSoup if Selenium failed or is disabled
            if not links:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, timeout=10, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for a_tag in soup.find_all('a', href=True):
                        links.append(a_tag['href'])

            # Log discovered links
            logger.info(f"Discovered {len(links)} links on {url}")
            return links

        except Exception as e:
            logger.warning(f"Error discovering links for {url}: {str(e)}")
            return []

    def process_sitemap_xml(self, base_url):
        """Try to fetch and process sitemap.xml if available."""
        sitemap_url = urllib.parse.urljoin(base_url, '/sitemap.xml')
        sitemap_urls = [sitemap_url]

        # Try alternate sitemap locations
        alternate_locations = [
            '/sitemap_index.xml',
            '/wp-sitemap.xml',
            '/sitemap1.xml'
        ]

        for alt_path in alternate_locations:
            sitemap_urls.append(urllib.parse.urljoin(base_url, alt_path))

        for sitemap_url in sitemap_urls:
            try:
                logger.info(f"Checking for sitemap at {sitemap_url}")
                response = requests.get(sitemap_url, timeout=10)
                if response.status_code == 200:
                    # Try parsing as XML
                    soup = BeautifulSoup(response.text, 'xml')
                    if not soup.find('loc'):
                        soup = BeautifulSoup(response.text, 'html.parser')

                    urls = [loc.text for loc in soup.find_all('loc')]

                    if not urls:
                        logger.info(f"No URLs found in sitemap at {sitemap_url}")
                        continue

                    logger.info(f"Found {len(urls)} URLs in sitemap at {sitemap_url}")

                    base_domain = self.extract_domain(base_url)
                    for url in urls:
                        if self.is_same_domain(url, base_domain) and self.should_visit(url):
                            self.url_queue.append(url)

                    logger.info(f"Added {len(urls)} URLs from sitemap at {sitemap_url}")
                    return True
                else:
                    logger.info(f"No sitemap found at {sitemap_url} (Status: {response.status_code})")
            except Exception as e:
                logger.warning(f"Error processing sitemap at {sitemap_url}: {str(e)}")

        return False

    def crawl_site(self, base_url, max_pages=50, output_dir=None):
        """
        Crawl a website starting from the base URL, discovering all accessible pages.

        Args:
            base_url: The starting URL for crawling
            max_pages: Maximum number of pages to crawl
            output_dir: Directory to save crawled page data

        Returns:
            Dictionary mapping URLs to their page data
        """
        self.max_pages = max_pages
        self.output_dir = output_dir or self.config.OUTPUT_DIR

        # Reset crawling state
        self.visited_urls = set()
        self.url_queue = deque([base_url])
        self.sitemap = {}

        base_domain = self.extract_domain(base_url)
        logger.info(f"Starting site crawl for domain: {base_domain}, max pages: {max_pages}")

        # Try to use sitemap.xml first
        sitemap_found = self.process_sitemap_xml(base_url)
        if not sitemap_found:
            logger.info("No sitemap.xml found or processed, continuing with discovery crawling")

        page_count = 0

        # Create output directory if it doesn't exist
        os.makedirs(os.path.join(self.output_dir, "page_data"), exist_ok=True)

        try:
            while self.url_queue and page_count < self.max_pages:
                current_url = self.url_queue.popleft()

                # Skip if already visited
                if current_url in self.visited_urls:
                    continue

                logger.info(f"Crawling {current_url} ({page_count + 1}/{self.max_pages})")
                self.visited_urls.add(current_url)

                try:
                    # Extract page data using WebCrawler
                    page_data = self.web_crawler.extract_page_data(current_url)

                    # Save page data to file
                    safe_filename = re.sub(r'[\\/*?:"<>|]', "_", current_url.replace('https://', '').replace('http://', ''))
                    file_path = os.path.join(self.output_dir, "page_data", f"{safe_filename}.json")

                    with open(file_path, 'w') as f:
                        json.dump(page_data, f, indent=2)

                    # Store in sitemap
                    self.sitemap[current_url] = {
                        "title": page_data.get("title", ""),
                        "file_path": file_path
                    }

                    page_count += 1

                    # Discover outgoing links
                    links = self.discover_links(current_url)

                    # Process each discovered link
                    for link in links:
                        if not link:
                            continue

                        abs_url = self.normalize_url(link, current_url)

                        if abs_url and self.is_same_domain(abs_url, base_domain) and self.should_visit(abs_url):
                            logger.debug(f"Adding to queue: {abs_url}")
                            self.url_queue.append(abs_url)
                        elif abs_url:
                            logger.debug(f"Skipping URL: {abs_url}")

                    # Small delay to avoid overwhelming the server
                    time.sleep(1)

                except Exception as e:
                    logger.error(f"Error processing {current_url}: {str(e)}")

        finally:
            # Clean up the discovery driver
            if self.discovery_driver:
                try:
                    self.discovery_driver.quit()
                except:
                    pass
                self.discovery_driver = None

        logger.info(f"Site crawl complete. Visited {len(self.visited_urls)} pages.")

        # Save the sitemap
        sitemap_path = os.path.join(self.output_dir, "sitemap.json")
        with open(sitemap_path, 'w') as f:
            json.dump(self.sitemap, f, indent=2)

        logger.info(f"Sitemap saved to {sitemap_path}")

        return self.sitemap
