# utils/element_finder.py - Add your implementation here

"""5. Element Finder"""

import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

logger = logging.getLogger(__name__)


class ElementFinder:
    """
    Utility class to find and extract information about UI elements on a page.
    """

    def __init__(self, driver):
        """
        Initialize the element finder.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver

    def find_interactive_elements(self):
        """
        Find all interactive elements on the page.

        Returns:
            list: List of dictionaries with element information
        """
        elements = []

        try:
            # Find buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            buttons.extend(
                self.driver.find_elements(By.XPATH, '//input[@type="button"]')
            )
            buttons.extend(
                self.driver.find_elements(By.XPATH, '//input[@type="submit"]')
            )

            for button in buttons:
                try:
                    # Get element attributes
                    element_data = self._extract_element_data(button, "button")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find links (anchor tags)
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                try:
                    element_data = self._extract_element_data(link, "link")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find select dropdowns
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for select in selects:
                try:
                    element_data = self._extract_element_data(select, "select")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find checkboxes
            checkboxes = self.driver.find_elements(
                By.XPATH, '//input[@type="checkbox"]'
            )
            for checkbox in checkboxes:
                try:
                    element_data = self._extract_element_data(checkbox, "checkbox")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find radio buttons
            radios = self.driver.find_elements(By.XPATH, '//input[@type="radio"]')
            for radio in radios:
                try:
                    element_data = self._extract_element_data(radio, "radio")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find text inputs
            inputs = self.driver.find_elements(
                By.XPATH,
                '//input[@type="text"] | //input[@type="email"] | //input[@type="password"] | //input[@type="number"] | //textarea',
            )
            for input_elem in inputs:
                try:
                    element_data = self._extract_element_data(input_elem, "input")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

            # Find custom elements with click handlers
            clickable = self.driver.find_elements(
                By.XPATH,
                '//*[@onclick] | //*[@role="button"] | //*[contains(@class, "btn")]',
            )
            for elem in clickable:
                try:
                    # Skip if already found as a different type
                    if elem.tag_name in ["button", "a", "input", "select"]:
                        continue
                    element_data = self._extract_element_data(elem, "clickable")
                    elements.append(element_data)
                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.error(f"Error finding interactive elements: {str(e)}")

        return elements

    def find_frames(self):
        """
        Find all frames/iframes on the page.

        Returns:
            list: List of dictionaries with frame information
        """
        frames = []

        try:
            # Find iframes
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    frame_data = {
                        "type": "iframe",
                        "src": iframe.get_attribute("src") or "",
                        "id": iframe.get_attribute("id") or "",
                        "name": iframe.get_attribute("name") or "",
                        "class": iframe.get_attribute("class") or "",
                        "location": self._get_element_location(iframe),
                    }
                    frames.append(frame_data)
                except StaleElementReferenceException:
                    continue

            # Find frames
            frame_elements = self.driver.find_elements(By.TAG_NAME, "frame")
            for frame in frame_elements:
                try:
                    frame_data = {
                        "type": "frame",
                        "src": frame.get_attribute("src") or "",
                        "id": frame.get_attribute("id") or "",
                        "name": frame.get_attribute("name") or "",
                        "class": frame.get_attribute("class") or "",
                        "location": self._get_element_location(frame),
                    }
                    frames.append(frame_data)
                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.error(f"Error finding frames: {str(e)}")

        return frames

    def find_forms(self):
        """
        Find all forms on the page.

        Returns:
            list: List of dictionaries with form information
        """
        forms = []

        try:
            form_elements = self.driver.find_elements(By.TAG_NAME, "form")
            for form in form_elements:
                try:
                    # Get form attributes
                    form_data = {
                        "id": form.get_attribute("id") or "",
                        "name": form.get_attribute("name") or "",
                        "class": form.get_attribute("class") or "",
                        "action": form.get_attribute("action") or "",
                        "method": form.get_attribute("method") or "get",
                        "location": self._get_element_location(form),
                        "inputs": [],
                    }

                    # Get form inputs
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    inputs.extend(form.find_elements(By.TAG_NAME, "select"))
                    inputs.extend(form.find_elements(By.TAG_NAME, "textarea"))

                    for input_elem in inputs:
                        try:
                            input_type = (
                                input_elem.get_attribute("type") or input_elem.tag_name
                            )
                            input_data = {
                                "type": input_type,
                                "id": input_elem.get_attribute("id") or "",
                                "name": input_elem.get_attribute("name") or "",
                                "placeholder": input_elem.get_attribute("placeholder")
                                or "",
                                "required": input_elem.get_attribute("required")
                                == "true",
                            }
                            form_data["inputs"].append(input_data)
                        except StaleElementReferenceException:
                            continue

                    forms.append(form_data)
                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.error(f"Error finding forms: {str(e)}")

        return forms

    def find_headings(self):
        """
        Find heading elements to understand page structure.

        Returns:
            list: List of dictionaries with heading information
        """
        headings = []

        try:
            # Find all headings (h1 to h6)
            for level in range(1, 7):
                heading_elements = self.driver.find_elements(By.TAG_NAME, f"h{level}")
                for heading in heading_elements:
                    try:
                        heading_data = {
                            "level": level,
                            "text": heading.text,
                            "id": heading.get_attribute("id") or "",
                            "class": heading.get_attribute("class") or "",
                            "location": self._get_element_location(heading),
                        }
                        headings.append(heading_data)
                    except StaleElementReferenceException:
                        continue

        except Exception as e:
            logger.error(f"Error finding headings: {str(e)}")

        return headings

    def _extract_element_data(self, element, element_type):
        """
        Extract data from an element.

        Args:
            element: Selenium WebElement
            element_type: Type of element (e.g., button, link)

        Returns:
            dict: Element data
        """
        element_data = {
            "type": element_type,
            "tag": element.tag_name,
            "text": element.text.strip() if element.text else "",
            "id": element.get_attribute("id") or "",
            "name": element.get_attribute("name") or "",
            "class": element.get_attribute("class") or "",
            "location": self._get_element_location(element),
            "is_displayed": element.is_displayed(),
            "is_enabled": element.is_enabled(),
        }

        # Add type-specific attributes
        if element_type == "link":
            element_data["href"] = element.get_attribute("href") or ""
            element_data["target"] = element.get_attribute("target") or ""
        elif element_type in ["button", "clickable"]:
            element_data["onclick"] = element.get_attribute("onclick") or ""
        elif element_type == "input":
            element_data["input_type"] = element.get_attribute("type") or ""
            element_data["placeholder"] = element.get_attribute("placeholder") or ""
            element_data["value"] = element.get_attribute("value") or ""
        elif element_type == "select":
            # Get options
            options = []
            for option in element.find_elements(By.TAG_NAME, "option"):
                try:
                    option_data = {
                        "value": option.get_attribute("value") or "",
                        "text": option.text.strip() if option.text else "",
                        "selected": option.is_selected(),
                    }
                    options.append(option_data)
                except StaleElementReferenceException:
                    continue
            element_data["options"] = options
        elif element_type in ["checkbox", "radio"]:
            element_data["checked"] = element.is_selected()
            element_data["value"] = element.get_attribute("value") or ""

        return element_data

    def _get_element_location(self, element):
        """
        Get element location information.

        Args:
            element: Selenium WebElement

        Returns:
            dict: Location data
        """
        try:
            location = element.location
            size = element.size

            return {
                "x": location["x"],
                "y": location["y"],
                "width": size["width"],
                "height": size["height"],
            }
        except:
            # Return empty location if we can't get it
            return {"x": 0, "y": 0, "width": 0, "height": 0}
