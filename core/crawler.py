# core/crawler.py
import json
import logging
import os
from typing import Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from config.config import Config

logger = logging.getLogger(__name__)

class WebCrawler:
    """Web crawler for extracting page data for testing."""

    def __init__(self, config: Config):
        """Initialize the web crawler.

        Args:
            config (Config): Configuration object
        """
        self.config = config
        self.driver = None
        self._initialize_driver()

    def _initialize_driver(self):
        """Initialize the Selenium WebDriver."""
        try:
            options = Options()
            if self.config.HEADLESS:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            if self.config.CHROME_DRIVER_PATH:
                service = Service(executable_path=self.config.CHROME_DRIVER_PATH)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)

            self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def extract_page_data(self, url: str) -> Dict[str, Any]:
        """Extract relevant data from a webpage.

        Args:
            url (str): URL to crawl

        Returns:
            Dict[str, Any]: Extracted page data
        """
        if not self.driver:
            self._initialize_driver()

        try:
            logger.info(f"Crawling URL: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Basic page information
            page_data = {
                "url": url,
                "title": self.driver.title,
                "elements": [],
                "frames": [],
                "forms": [],
                "headings": []
            }

            # Extract interactive elements
            self._extract_elements(page_data)

            # Extract frames
            self._extract_frames(page_data)

            # Extract forms
            self._extract_forms(page_data)

            # Extract headings
            self._extract_headings(page_data)

            return page_data

        except TimeoutException:
            logger.error(f"Timeout while loading URL: {url}")
            return self._create_error_response(url, "Timeout while loading page")

        except WebDriverException as e:
            logger.error(f"WebDriver error: {str(e)}")
            return self._create_error_response(url, f"WebDriver error: {str(e)}")

        except Exception as e:
            logger.error(f"Error extracting page data: {str(e)}")
            return self._create_error_response(url, str(e))

    def _extract_elements(self, page_data: Dict[str, Any]):
        """Extract interactive elements from the page."""
        for elem_type, by_method in [
            ("button", By.TAG_NAME),
            ("a", By.TAG_NAME),
            ("input", By.TAG_NAME),
            ("select", By.TAG_NAME)
        ]:
            elements = self.driver.find_elements(by_method, elem_type)
            for elem in elements:
                try:
                    element_data = {
                        "type": elem_type,
                        "tag": elem.tag_name
                    }

                    # Try to get various attributes
                    for attr in ["id", "name", "class", "type", "value", "placeholder", "href"]:
                        try:
                            value = elem.get_attribute(attr)
                            if value:
                                element_data[attr] = value
                        except:
                            pass

                    # Get text content
                    try:
                        text = elem.text
                        if text:
                            element_data["text"] = text
                    except:
                        pass

                    # Add to elements list
                    page_data["elements"].append(element_data)
                except:
                    continue

    def _extract_frames(self, page_data: Dict[str, Any]):
        """Extract frames from the page."""
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for frame in frames:
            try:
                frame_data = {"tag": "iframe"}
                for attr in ["id", "name", "src", "width", "height"]:
                    value = frame.get_attribute(attr)
                    if value:
                        frame_data[attr] = value
                page_data["frames"].append(frame_data)
            except:
                continue

    def _extract_forms(self, page_data: Dict[str, Any]):
        """Extract forms from the page."""
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        for form in forms:
            try:
                form_data = {
                    "tag": "form",
                    "inputs": []
                }

                # Form attributes
                for attr in ["id", "name", "action", "method"]:
                    value = form.get_attribute(attr)
                    if value:
                        form_data[attr] = value

                # Form inputs
                inputs = form.find_elements(By.TAG_NAME, "input")
                for input_elem in inputs:
                    input_data = {}
                    for attr in ["id", "name", "type", "value", "placeholder"]:
                        value = input_elem.get_attribute(attr)
                        if value:
                            input_data[attr] = value
                    if input_data:
                        form_data["inputs"].append(input_data)

                page_data["forms"].append(form_data)
            except:
                continue

    def _extract_headings(self, page_data: Dict[str, Any]):
        """Extract headings from the page."""
        for h_level in range(1, 7):
            headings = self.driver.find_elements(By.TAG_NAME, f"h{h_level}")
            for heading in headings:
                try:
                    heading_text = heading.text
                    if heading_text:
                        page_data["headings"].append({
                            "level": h_level,
                            "text": heading_text
                        })
                except:
                    continue

    def _create_error_response(self, url: str, error_msg: str) -> Dict[str, Any]:
        """Create an error response when page crawling fails."""
        return {
            "url": url,
            "title": "Error",
            "error": error_msg,
            "elements": [],
            "frames": [],
            "forms": [],
            "headings": []
        }

    def save_page_data(self, page_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save page data to a JSON file.

        Args:
            page_data (Dict[str, Any]): Page data to save
            filename (Optional[str]): Custom filename, defaults to URL-based name

        Returns:
            str: Path to the saved file
        """
        if filename is None:
            # Create a filename based on the URL
            import re
            from urllib.parse import urlparse

            parsed_url = urlparse(page_data["url"])
            domain = parsed_url.netloc.replace(".", "_")
            path = re.sub(r'[^\w]', '_', parsed_url.path)
            if not path:
                path = "home"
            filename = f"{domain}_{path}.json"

        # Ensure the path exists
        output_path = os.path.join(self.config.page_data_path, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(page_data, indent=2, fp=f)

        logger.info(f"Saved page data to {output_path}")
        return output_path

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver closed")
