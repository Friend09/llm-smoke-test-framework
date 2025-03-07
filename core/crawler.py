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
from datetime import datetime
import time

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

    def extract_page_data(self, url: str, with_screenshots: bool = False) -> Dict[str, Any]:
        """
        Extract data from a webpage.

        Args:
            url (str): URL to crawl
            with_screenshots (bool): Whether to capture screenshots

        Returns:
            Dict[str, Any]: Extracted page data
        """
        if not self.driver:
            self._initialize_driver()

        logger.info(f"Crawling URL: {url}")
        try:
            # Load page
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, self.config.PAGE_LOAD_TIMEOUT).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            except Exception as e:
                logger.warning(f"Timeout waiting for page to load: {str(e)}")

            # Initialize page data
            page_data = {
                "url": url,
                "title": self.driver.title,
                "timestamp": datetime.now().isoformat(),
                "elements": [],
                "forms": [],
                "frames": [],
                "headings": []
            }

            try:
                # Extract elements and their attributes (limit to maximum of 100 important elements)
                self._extract_elements(page_data)

                # Only keep top N elements to avoid token limits
                if len(page_data["elements"]) > 100:
                    # Sort by importance
                    page_data["elements"].sort(
                        key=lambda e: (
                            e.get("tag") in ["button", "a", "input", "select", "textarea"],  # Interactive first
                            bool(e.get("id", "")),  # Then with ID
                            bool(e.get("name", "")),  # Then with name
                            bool(e.get("text", ""))  # Then with text
                        ),
                        reverse=True
                    )
                    # Keep only the top 100
                    page_data["elements"] = page_data["elements"][:100]

                # Extract frames
                self._extract_frames(page_data)

                # Extract form elements - very important for testing
                self._extract_forms(page_data)

                # Extract headings for page structure
                self._extract_headings(page_data)

                # Add selectors for elements
                self._add_selectors_to_elements(page_data)

                # Extract element relationships and hierarchy
                self._extract_elements_with_hierarchy(page_data)

                # Extract form relationships (labels, etc.)
                self._extract_forms_with_relationships(page_data)

                # Identify logical sections
                self._identify_logical_sections(page_data)

                # Capture screenshots if requested
                if with_screenshots:
                    self._capture_screenshots(page_data)

                # Add HTML content (truncated to avoid token issues)
                page_source = self.driver.page_source
                if page_source:
                    # Only include the first 100KB of HTML to avoid token limits
                    page_data["html_content"] = page_source[:100000] if len(page_source) > 100000 else page_source

            except Exception as section_error:
                logger.error(f"Error extracting section data: {str(section_error)}")

            return page_data

        except Exception as e:
            logger.error(f"Error extracting page data from {url}: {str(e)}")
            return self._create_error_response(url, str(e))

    def _extract_elements_with_hierarchy(self, page_data):
        """Extract page elements while preserving DOM hierarchy."""
        # Get the entire page DOM structure
        dom_structure = {}

        # Use JavaScript to get a hierarchical representation
        script = """
        function getElementInfo(element) {
            const result = {
                tag: element.tagName.toLowerCase(),
                id: element.id || null,
                class: element.className || null,
                type: element.type || null,
                name: element.name || null,
                text: element.textContent.trim() || null,
                attributes: {},
                children: []
            };

            // Get all attributes
            for (let attr of element.attributes) {
                result.attributes[attr.name] = attr.value;
            }

            // Get children elements (only interesting ones)
            const interestingTags = ['div', 'form', 'button', 'a', 'input', 'select', 'textarea', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label'];
            for (let child of element.children) {
                if (interestingTags.includes(child.tagName.toLowerCase())) {
                    result.children.push(getElementInfo(child));
                }
            }

            return result;
        }

        return getElementInfo(document.body);
        """

        dom_structure = self.driver.execute_script(script)
        page_data["dom_structure"] = dom_structure

    def _extract_forms_with_relationships(self, page_data):
        """Extract forms with their associated elements."""
        forms = self.driver.find_elements(By.TAG_NAME, "form")

        page_data["forms"] = []

        for form in forms:
            try:
                form_data = {
                    "tag": "form",
                    "id": form.get_attribute("id"),
                    "name": form.get_attribute("name"),
                    "action": form.get_attribute("action"),
                    "method": form.get_attribute("method"),
                    "elements": []
                }

                # Extract all interactive elements in the form
                for elem_type in ["input", "select", "textarea", "button"]:
                    elements = form.find_elements(By.TAG_NAME, elem_type)
                    for elem in elements:
                        elem_data = {
                            "tag": elem.tag_name,
                            "type": elem.get_attribute("type"),
                            "id": elem.get_attribute("id"),
                            "name": elem.get_attribute("name"),
                            "value": elem.get_attribute("value"),
                            "placeholder": elem.get_attribute("placeholder"),
                        }

                        # Add label text if there's an associated label
                        if elem.get_attribute("id"):
                            label = self.driver.execute_script(
                                f"return document.querySelector('label[for=\"{elem.get_attribute('id')}\"]')?.textContent"
                            )
                            if label:
                                elem_data["label_text"] = label.strip()

                        form_data["elements"].append(elem_data)

                page_data["forms"].append(form_data)
            except Exception as e:
                logger.error(f"Error extracting form: {str(e)}")
                continue

    def _capture_screenshots(self, page_data):
        """Capture full page and element screenshots."""

        # Capture full page screenshot
        screenshot_dir = os.path.join(self.config.OUTPUT_DIR, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Generate a safe filename from URL
        from urllib.parse import urlparse
        import re
        parsed_url = urlparse(page_data["url"])
        domain = parsed_url.netloc.replace(".", "_")
        path = re.sub(r'[^\w]', '_', parsed_url.path)
        if not path:
            path = "home"
        filename = f"{domain}_{path}.png"

        # Save full page screenshot
        full_page_path = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(full_page_path)
        page_data["screenshot_path"] = full_page_path

        # Optionally capture screenshots of key elements (forms, buttons, etc.)
        element_screenshots = {}

        # Capture form screenshots
        for i, form in enumerate(self.driver.find_elements(By.TAG_NAME, "form")):
            try:
                form_name = form.get_attribute("id") or form.get_attribute("name") or f"form_{i}"
                form_path = os.path.join(screenshot_dir, f"{domain}_{path}_{form_name}.png")
                form.screenshot(form_path)
                element_screenshots[f"form_{i}"] = form_path
            except:
                pass

        page_data["element_screenshots"] = element_screenshots

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

    def _add_selectors_to_elements(self, page_data):
        """Add XPath and CSS selectors to elements for better locators."""

        for element_type in ["elements", "forms"]:
            for i, element in enumerate(page_data.get(element_type, [])):
                try:
                    # Generate a unique identifier for the element
                    elem_id = element.get("id") or element.get("name")

                    if elem_id:
                        # Add CSS selector
                        element["css_selector"] = f"#{elem_id}" if element.get("id") else f"[name='{elem_id}']"

                        # Add XPath
                        element["xpath"] = f"//*[@id='{element.get('id')}']" if element.get("id") else f"//*[@name='{elem_id}']"
                    elif element.get("text") and element.get("tag"):
                        # For elements with text but no ID/name
                        element["xpath"] = f"//{element['tag']}[contains(text(), '{element['text']}')]"

                        # Try to create a more precise CSS selector
                        if element.get("class"):
                            classes = element["class"].split()
                            if classes:
                                element["css_selector"] = f"{element['tag']}.{classes[0]}"
                except:
                    continue

    def _identify_logical_sections(self, page_data):
        """Identify logical sections/groups in the page."""

        # Use JavaScript to find logical sections based on semantic HTML
        script = """
        function findLogicalSections() {
            const sections = [];

            // Find semantic sections
            const semanticTags = [
                'header', 'footer', 'main', 'nav', 'section', 'article',
                'aside', 'form', 'div.container', 'div.section', 'div.row'
            ];

            semanticTags.forEach(selector => {
                document.querySelectorAll(selector).forEach(element => {
                    // Don't include elements that are too small or empty
                    if (element.textContent.trim() &&
                        element.getBoundingClientRect().width > 100 &&
                        element.getBoundingClientRect().height > 50) {

                        // Get heading if available
                        let heading = '';
                        const headingElem = element.querySelector('h1, h2, h3, h4, h5, h6');
                        if (headingElem) {
                            heading = headingElem.textContent.trim();
                        }

                        sections.push({
                            tag: element.tagName.toLowerCase(),
                            id: element.id || null,
                            class: element.className || null,
                            heading: heading,
                            position: {
                                x: element.getBoundingClientRect().x,
                                y: element.getBoundingClientRect().y,
                                width: element.getBoundingClientRect().width,
                                height: element.getBoundingClientRect().height
                            },
                            elements: Array.from(element.querySelectorAll('button, a, input, select')).length
                        });
                    }
                });
            });

            return sections;
        }

        return findLogicalSections();
        """

        logical_sections = self.driver.execute_script(script)
        page_data["logical_sections"] = logical_sections

    def crawl_with_user_flow(self, url, flow_description):
        """Crawl a page while simulating a user flow."""

        # First get the base page
        page_data = self.extract_page_data(url)

        # Parse the flow description and execute it
        steps = flow_description.strip().split('\n')

        # Record the flow steps and their results
        page_data["user_flow"] = []

        for step in steps:
            try:
                step = step.strip()
                if not step:
                    continue

                step_result = {"description": step, "success": False}

                # Parse the step and execute it
                if step.startswith("click "):
                    element_desc = step[6:].strip()
                    self._click_element(element_desc)
                    step_result["success"] = True

                elif step.startswith("type "):
                    parts = step[5:].strip().split(" into ")
                    if len(parts) == 2:
                        text, element_desc = parts
                        self._type_text(element_desc, text)
                        step_result["success"] = True

                elif step.startswith("select "):
                    parts = step[7:].strip().split(" from ")
                    if len(parts) == 2:
                        option, element_desc = parts
                        self._select_option(element_desc, option)
                        step_result["success"] = True

                # Take screenshot after each step
                screenshot_path = f"{self.config.OUTPUT_DIR}/screenshots/step_{len(page_data['user_flow'])}.png"
                self.driver.save_screenshot(screenshot_path)
                step_result["screenshot"] = screenshot_path

                # Add current URL
                step_result["url"] = self.driver.current_url

                # Capture page state after step
                step_result["page_state"] = {
                    "title": self.driver.title,
                    "url": self.driver.current_url
                }

                page_data["user_flow"].append(step_result)

            except Exception as e:
                logger.error(f"Error executing step '{step}': {str(e)}")
                step_result["error"] = str(e)
                page_data["user_flow"].append(step_result)

        return page_data

    def save_page_data(self, page_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """
        Save page data to a file.

        Args:
            page_data (Dict[str, Any]): Page data to save
            filename (Optional[str]): Filename to save to (optional)

        Returns:
            str: Path to the saved file
        """
        try:
            # Check if page_data is None or empty
            if page_data is None:
                logger.error("Cannot save None page data")
                fallback_path = os.path.join(self.config.OUTPUT_DIR, "page_data", f"error_none_{int(time.time())}.json")
                with open(fallback_path, "w", encoding="utf-8") as f:
                    json.dump({"error": "None page data", "timestamp": str(datetime.now())}, f)
                return fallback_path

            # Create output directory if it doesn't exist
            output_dir = os.path.join(self.config.OUTPUT_DIR, "page_data")
            os.makedirs(output_dir, exist_ok=True)

            # Generate filename from URL if not provided
            if not filename:
                url = page_data.get("url", "unknown")
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
                filename = f"{safe_url}.json"

            # Ensure the filename has a .json extension
            if not filename.endswith(".json"):
                filename += ".json"

            # Full path to the output file
            output_path = os.path.join(output_dir, filename)

            # Create a copy of the page data to avoid modifying the original
            data_to_save = page_data.copy()

            # Handle large HTML content to avoid token issues later
            if "html_content" in data_to_save and isinstance(data_to_save["html_content"], str):
                html_content = data_to_save["html_content"]
                # If HTML content is very large, truncate it
                if len(html_content) > 100000:  # 100KB limit
                    data_to_save["html_content"] = html_content[:100000] + "... [truncated]"
                    logger.info(f"HTML content truncated from {len(html_content)} to 100000 characters")

            # Save the data to a JSON file
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved page data to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error saving page data: {str(e)}")
            # Create a fallback file
            fallback_path = os.path.join(self.config.OUTPUT_DIR, "page_data", f"error_{int(time.time())}.json")
            try:
                with open(fallback_path, "w", encoding="utf-8") as f:
                    # Include minimal information if page_data is valid
                    error_data = {
                        "error": str(e),
                        "timestamp": str(datetime.now())
                    }

                    if isinstance(page_data, dict):
                        error_data["url"] = page_data.get("url", "unknown")

                    json.dump(error_data, f)
                return fallback_path
            except Exception as inner_e:
                logger.error(f"Error creating fallback file: {str(inner_e)}")
                return ""

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver closed")

    def _analyze_layout(self, page_data):
        """
        Analyze the page layout to identify key sections and their relationships.

        Args:
            page_data (dict): Page data dictionary to be updated with layout information
        """
        try:
            # This is a simple implementation - you might want to expand this
            layout_data = {
                "viewport_width": self.driver.execute_script("return window.innerWidth"),
                "viewport_height": self.driver.execute_script("return window.innerHeight"),
                "sections": []
            }

            # Try to identify main sections based on common layout elements
            for section_tag in ["header", "nav", "main", "footer", "section", "article", "aside"]:
                sections = self.driver.find_elements(By.TAG_NAME, section_tag)
                for i, section in enumerate(sections):
                    try:
                        section_id = section.get_attribute("id") or f"{section_tag}_{i}"
                        rect = section.rect

                        # Get the section elements
                        inner_elements = section.find_elements(By.XPATH, ".//*")
                        element_count = len(inner_elements)

                        # Add section data
                        layout_data["sections"].append({
                            "id": section_id,
                            "tag": section_tag,
                            "x": rect["x"],
                            "y": rect["y"],
                            "width": rect["width"],
                            "height": rect["height"],
                            "element_count": element_count
                        })
                    except Exception as e:
                        logger.debug(f"Error analyzing section {section_tag}_{i}: {str(e)}")
                        continue

            # Try to identify content structure using div elements with specific classes
            main_divs = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'main') or contains(@class, 'content') or contains(@class, 'container')]")
            for i, div in enumerate(main_divs):
                try:
                    div_id = div.get_attribute("id") or div.get_attribute("class") or f"main_div_{i}"
                    rect = div.rect

                    # Check if this seems like a main content area
                    if rect["width"] > layout_data["viewport_width"] * 0.5 and rect["height"] > 100:
                        layout_data["sections"].append({
                            "id": div_id,
                            "tag": "div",
                            "x": rect["x"],
                            "y": rect["y"],
                            "width": rect["width"],
                            "height": rect["height"],
                            "is_main_content": True
                        })
                except Exception as e:
                    logger.debug(f"Error analyzing main div {i}: {str(e)}")
                    continue

            # Add layout data to page data
            page_data["layout"] = layout_data

        except Exception as e:
            logger.error(f"Error analyzing layout: {str(e)}")
            # Don't fail the entire process if layout analysis fails
            page_data["layout"] = {"error": str(e)}
