# utils/url_extractor.py - Add your implementation here
"""3. Enhanced URL Extractor"""

# utils/url_extractor.py
import re
import logging
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

logger = logging.getLogger(__name__)


class URLExtractor:
    """
    Enhanced URL extractor that uses multiple methods to find all URLs in a page,
    including JavaScript-generated links, buttons, and other interactive elements.
    """

    def __init__(
        self, driver, base_url, exclude_patterns=None, include_subdomains=True
    ):
        """
        Initialize the URL extractor.

        Args:
            driver: Selenium WebDriver instance
            base_url: Base URL of the application
            exclude_patterns: List of patterns to exclude from extraction
            include_subdomains: Whether to include subdomains of the base URL
        """
        self.driver = driver
        self.base_url = base_url
        self.exclude_patterns = exclude_patterns or []
        self.include_subdomains = include_subdomains
        self.base_domain = urllib.parse.urlparse(base_url).netloc

    def extract_urls(self):
        """
        Extract all URLs from the current page using multiple methods.

        Returns:
            set: Set of normalized URLs found on the page
        """
        all_urls = set()

        # Method 1: Extract URLs using BeautifulSoup
        soup_urls = self._extract_with_beautifulsoup()
        all_urls.update(soup_urls)

        # Method 2: Extract URLs using Selenium directly
        selenium_urls = self._extract_with_selenium()
        all_urls.update(selenium_urls)

        # Method 3: Extract URLs from JavaScript event handlers
        js_urls = self._extract_from_javascript()
        all_urls.update(js_urls)

        # Normalize and filter URLs
        normalized_urls = self._normalize_urls(all_urls)

        return normalized_urls

    def _extract_with_beautifulsoup(self):
        """Extract URLs using BeautifulSoup."""
        urls = set()
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract href attributes from anchor tags
        for a_tag in soup.find_all("a", href=True):
            urls.add(a_tag["href"])

        # Extract form actions
        for form in soup.find_all("form", action=True):
            urls.add(form["action"])

        # Extract iframe sources
        for iframe in soup.find_all("iframe", src=True):
            urls.add(iframe["src"])

        # Extract image map areas
        for area in soup.find_all("area", href=True):
            urls.add(area["href"])

        return urls

    def _extract_with_selenium(self):
        """Extract URLs directly using Selenium."""
        urls = set()

        # Find all elements that might contain URLs
        try:
            # Anchor tags
            anchors = self.driver.find_elements(By.TAG_NAME, "a")
            for anchor in anchors:
                try:
                    href = anchor.get_attribute("href")
                    if href:
                        urls.add(href)
                except StaleElementReferenceException:
                    continue

            # Forms
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            for form in forms:
                try:
                    action = form.get_attribute("action")
                    if action:
                        urls.add(action)
                except StaleElementReferenceException:
                    continue

            # Buttons (look for onclick handlers)
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            buttons.extend(
                self.driver.find_elements(By.XPATH, '//input[@type="button"]')
            )
            buttons.extend(
                self.driver.find_elements(By.XPATH, '//input[@type="submit"]')
            )

            for button in buttons:
                try:
                    onclick = button.get_attribute("onclick")
                    if onclick and ("location" in onclick or "window.open" in onclick):
                        # Extract URL from onclick handler
                        matches = re.findall(r"(\'|\")(.+?)(\'|\")", onclick)
                        for match in matches:
                            potential_url = match[1]
                            if self._looks_like_url(potential_url):
                                urls.add(potential_url)
                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.error(f"Error extracting URLs with Selenium: {str(e)}")

        return urls

    def _extract_from_javascript(self):
        """Extract URLs from JavaScript event handlers and other JS elements."""
        urls = set()

        # Execute JavaScript to find URLs in event handlers
        js_script = """
        var links = [];

        // Get all elements with onclick handlers
        var elements = document.querySelectorAll('[onclick]');
        for (var i = 0; i < elements.length; i++) {
            var onclick = elements[i].getAttribute('onclick');
            if (onclick && (onclick.includes('location') || onclick.includes('window.open'))) {
                var matches = onclick.match(/(\'|\")(.+?)(\'|\")/g);
                if (matches) {
                    for (var j = 0; j < matches.length; j++) {
                        var url = matches[j].replace(/[\'\"]/g, '');
                        if (url && url.length > 1 && !url.startsWith('javascript:')) {
                            links.push(url);
                        }
                    }
                }
            }
        }

        // Find all other elements with href-like attributes
        var allElements = document.querySelectorAll('*');
        for (var i = 0; i < allElements.length; i++) {
            var el = allElements[i];
            var attributes = ['href', 'src', 'action', 'data-url', 'data-href'];

            for (var j = 0; j < attributes.length; j++) {
                var attr = el.getAttribute(attributes[j]);
                if (attr && attr.length > 1 && !attr.startsWith('javascript:')) {
                    links.push(attr);
                }
            }
        }

        // Find URLs in inline scripts
        var scripts = document.querySelectorAll('script');
        for (var i = 0; i < scripts.length; i++) {
            var content = scripts[i].textContent;
            if (content) {
                var urlMatches = content.match(/(https?:\\/\\/[^\\s\'"]+)|(\\/'[^']*\\')|(\\"[^"]*\\")/g);
                if (urlMatches) {
                    for (var j = 0; j < urlMatches.length; j++) {
                        var url = urlMatches[j].replace(/[\'\"]/g, '');
                        if (url && url.length > 1 && !url.startsWith('javascript:')) {
                            links.push(url);
                        }
                    }
                }
            }
        }

        return links;
        """

        try:
            js_results = self.driver.execute_script(js_script)
            if js_results and isinstance(js_results, list):
                urls.update(js_results)
        except Exception as e:
            logger.error(f"Error extracting URLs from JavaScript: {str(e)}")

        return urls

    def _normalize_urls(self, urls):
        """
        Normalize and filter URLs.

        Args:
            urls: Set of URLs to normalize

        Returns:
            set: Set of normalized URLs
        """
        normalized = set()

        for url in urls:
            # Skip empty URLs or None values
            if not url:
                continue

            # Skip excluded patterns
            if any(pattern in url for pattern in self.exclude_patterns):
                continue

            # Handle relative URLs
            if url.startswith("/"):
                # Convert to absolute URL
                url = urllib.parse.urljoin(self.base_url, url)
            elif not url.startswith(("http://", "https://")):
                # Handle cases like "page.html" or "folder/page.html"
                # Skip if it starts with javascript: or #
                if url.startswith(("javascript:", "#")):
                    continue
                url = urllib.parse.urljoin(self.driver.current_url, url)

            # Parse the URL
            parsed_url = urllib.parse.urlparse(url)

            # Skip URLs that are not in the same domain if include_subdomains is False
            if not self.include_subdomains and parsed_url.netloc != self.base_domain:
                continue

            # Check if URL is in a subdomain of the base URL if include_subdomains is True
            if (
                self.include_subdomains
                and not parsed_url.netloc.endswith(self.base_domain)
                and self.base_domain not in parsed_url.netloc
            ):
                continue

            # Remove fragments (e.g., #section) for deduplication purposes
            url = url.split("#")[0]

            # Add to normalized set
            normalized.add(url)

        return normalized

    def _looks_like_url(self, text):
        """Check if a string looks like a URL."""
        return bool(re.match(r"^(https?:\/\/|\/|\.\/|\.\.\/).*$", text))
