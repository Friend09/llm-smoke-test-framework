# test_llm_analyzer_real.py
import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import your modules
from core.llm_analyzer import LLMAnalyzer
from config.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebCrawler:
    """Simple web crawler to extract page data for testing"""

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def extract_page_data(self, url):
        """Extract relevant data from a webpage"""
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

            # Extract frames
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

            # Extract forms
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

            # Extract headings
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

            return page_data

        except Exception as e:
            logger.error(f"Error extracting page data: {str(e)}")
            return {
                "url": url,
                "title": "Error",
                "error": str(e),
                "elements": [],
                "frames": [],
                "forms": [],
                "headings": []
            }

    def close(self):
        """Close the browser"""
        self.driver.quit()


class RealConfigLoader:
    """Load real configuration from environment variables"""

    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-40-mini")
        self.LLM_TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.0"))
        self.LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "2000"))

    def validate(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True


def save_json(data, filename):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, indent=2, fp=f)
    logger.info(f"Saved data to {filename}")


def test_with_real_page():
    """Test LLMAnalyzer with real page data"""
    # URL to test
    url = "https://practicetestautomation.com/practice-test-login/"  # Replace with your target URL

    # Extract page data
    crawler = WebCrawler()
    try:
        page_data = crawler.extract_page_data(url)
        save_json(page_data, "./output/page_data/test_page_data.json")

        # Check if valid data was extracted
        if "error" in page_data:
            logger.error(f"Failed to extract page data: {page_data['error']}")
            return

        # Now use LLMAnalyzer to analyze the page
        try:
            config = RealConfigLoader()
            analyzer = LLMAnalyzer(config)

            # Analyze page
            logger.info("Analyzing page with LLM...")
            analysis = analyzer.analyze_page(page_data)
            save_json(analysis, "./output/analysis/test_analysis_result.json")

            # Generate test script
            logger.info("Generating test scripts...")
            test_script = analyzer.generate_test_script(analysis, "cucumber")
            save_json(test_script, "./output/test_scripts/test_script.json")

            # Also save the actual script files
            if "feature_file" in test_script:
                with open("./output/test_scripts/test_generated_test.feature", "w") as f:
                    f.write(test_script["feature_file"])

            if "step_definitions" in test_script:
                with open("./output/test_scripts/test_generated_steps.java", "w") as f:
                    f.write(test_script["step_definitions"])

            if "page_object" in test_script:
                with open("./output/test_scripts/test_generated_page.java", "w") as f:
                    f.write(test_script["page_object"])

            logger.info("Testing completed successfully!")

        except Exception as e:
            logger.error(f"Error in LLM analysis: {str(e)}")

    finally:
        crawler.close()


if __name__ == "__main__":
    test_with_real_page()
