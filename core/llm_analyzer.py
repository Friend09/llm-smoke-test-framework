# core/llm_analyzer.py - Add your implementation here

"""6. LLM Analyzer"""
# core/llm_analyzer.py
import os
import json
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from config.config import Config
import openai
import re
from .screenshot_utils import optimize_screenshot
from dotenv import load_dotenv
import base64

logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMAnalyzer:
    """
    LLM-based analyzer that processes page data and generates test information.
    """

    def __init__(self, config: Config):
        """
        Initialize the LLM analyzer.

        Args:
            config (Config): Configuration object
        """
        self.config = config
        self.config.validate()  # Ensure required settings are present

        # Initialize OpenAI client
        self.llm = ChatOpenAI(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.LLM_MODEL,
            temperature=self.config.LLM_TEMPERATURE,
            max_tokens=self.config.LLM_MAX_TOKENS,
        )

        # Direct OpenAI client for vision capabilities
        self.openai_client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)

    def analyze_page(self, page_data):
        """Analyze page data to identify key elements for testing."""
        try:
            # More aggressive data simplification
            def truncate_text(text, max_length=500):
                return text[:max_length] if isinstance(text, str) and len(text) > max_length else text

            # Create a simplified version of the page data to stay within token limits
            simplified_data = {
                "url": page_data.get("url", ""),
                "title": page_data.get("title", ""),
            }

            # Process elements - only keep key interactive elements
            if "elements" in page_data:
                # Sort elements by importance (prefer elements with IDs, then with text content)
                def element_importance(elem):
                    has_id = elem.get('id', '') != ''
                    has_text = elem.get('text', '') != ''
                    has_name = elem.get('name', '') != ''
                    interactive = elem.get('tag', '') in ['button', 'a', 'input', 'select']
                    return (interactive, has_id, has_text, has_name)

                elements = page_data.get("elements", [])
                sorted_elements = sorted(elements, key=element_importance, reverse=True)

                # Take the top N elements and simplify them
                simplified_elements = []
                for elem in sorted_elements[:20]:  # Increased from 10 to 20 elements
                    simple_elem = {}
                    # Only keep the most important attributes
                    for key in ['id', 'tag', 'type', 'name', 'text', 'class']:
                        if key in elem and elem[key]:
                            # Truncate text values to reduce token count
                            if isinstance(elem[key], str) and len(elem[key]) > 100:
                                simple_elem[key] = elem[key][:100] + "..."
                            else:
                                simple_elem[key] = elem[key]
                    simplified_elements.append(simple_elem)

                simplified_data["elements"] = simplified_elements

            # Process forms - very important for testing
            if "forms" in page_data:
                forms = page_data.get("forms", [])
                simplified_forms = []
                for form in forms[:3]:  # Limit to top 3 forms
                    simple_form = {
                        "id": form.get("id", ""),
                        "action": form.get("action", ""),
                        "method": form.get("method", ""),
                        "inputs": []
                    }
                    # Process form inputs
                    for input_field in form.get("inputs", [])[:5]:  # Limit to top 5 inputs per form
                        simple_input = {}
                        for key in ['id', 'name', 'type', 'required']:
                            if key in input_field and input_field[key]:
                                simple_input[key] = input_field[key]
                        simple_form["inputs"].append(simple_input)
                    simplified_forms.append(simple_form)

                simplified_data["forms"] = simplified_forms

            # Process headings - helpful for understanding page structure
            if "headings" in page_data:
                headings = page_data.get("headings", [])
                simplified_headings = []
                for heading in headings[:5]:  # Limit to top 5 headings
                    simplified_headings.append({
                        "level": heading.get("level", ""),
                        "text": truncate_text(heading.get("text", ""), 100)
                    })
                simplified_data["headings"] = simplified_headings

            # Make the prompt clearer and more structured
            prompt_template = """
            I'm an expert web tester analyzing a webpage to generate smoke test information.

            PAGE URL: {url}
            PAGE TITLE: {title}

            ELEMENTS:
            {elements_info}

            FORMS:
            {forms_info}

            HEADINGS:
            {headings_info}

            Based on this data, I need to provide:

            1. KEY ELEMENTS:
            List the most important elements that should be tested.

            2. UNIQUE IDENTIFIERS:
            List unique ways to identify this page in tests (title, URL patterns, unique elements).

            3. RECOMMENDED SMOKE TEST STEPS:
            List 5-10 concise steps for smoke testing this page.

            4. SUGGESTED LOCATOR STRATEGIES:
            List element: locator pairs for important elements (use best practice selectors).
            """

            # Format element info
            elements_info = "ELEMENTS:\n"
            for elem in simplified_data.get("elements", []):
                elements_info += f"- {elem.get('tag', '')}"
                if elem.get('id'):
                    elements_info += f" id='{elem.get('id')}'"
                if elem.get('type'):
                    elements_info += f" type='{elem.get('type')}'"
                if elem.get('text'):
                    elements_info += f" text='{elem.get('text')}'"
                elements_info += "\n"

            # Format form info
            forms_info = "FORMS:\n"
            for form in simplified_data.get("forms", []):
                forms_info += f"- Form"
                if form.get('id'):
                    forms_info += f" id='{form.get('id')}'"
                forms_info += f" method='{form.get('method', '')}'\n"
                for input_field in form.get("inputs", []):
                    forms_info += f"  - Input"
                    if input_field.get('id'):
                        forms_info += f" id='{input_field.get('id')}'"
                    if input_field.get('type'):
                        forms_info += f" type='{input_field.get('type')}'"
                    if input_field.get('name'):
                        forms_info += f" name='{input_field.get('name')}'"
                    forms_info += "\n"

            # Format headings info
            headings_info = "HEADINGS:\n"
            for heading in simplified_data.get("headings", []):
                headings_info += f"- H{heading.get('level', '')}: {heading.get('text', '')}\n"

            # Format the prompt
            formatted_prompt = prompt_template.format(
                url=simplified_data.get("url", ""),
                title=simplified_data.get("title", ""),
                elements_info=elements_info,
                forms_info=forms_info,
                headings_info=headings_info
            )

            # Get LLM response
            logger.info(f"Sending analysis request to LLM for {simplified_data.get('url', '')}")
            response = self.llm.invoke(formatted_prompt)

            # Log response for debugging
            logger.info(f"Raw LLM output:\n{response.content}")

            # Process the response
            return self._process_analysis_response(response.content, simplified_data)

        except Exception as e:
            logger.error(f"Error analyzing page with LLM: {str(e)}")
            return {
                "url": page_data.get("url", ""),
                "title": page_data.get("title", ""),
                "error": str(e),
                "page_title_validation": page_data.get("title", ""),
                "unique_identifiers": ["URL: " + page_data.get("url", "")],
                "key_elements": [],
                "smoke_test_steps": ["Visit the page and verify it loads",
                                   f"Check page title is '{page_data.get('title', '')}'"],
                "locator_strategies": {},
            }

    def _process_analysis_response(self, response_content, page_data):
        """Process the LLM response to extract structured information."""
        logger.info(f"Processing LLM response for {page_data.get('url', '')}")

        # Log the raw response for debugging
        logger.info(f"Raw LLM response: {response_content[:1000]}...")

        analysis_result = {
            "url": page_data.get("url", ""),
            "title": page_data.get("title", ""),
            "page_title_validation": page_data.get("title", ""),
            "unique_identifiers": [],
            "key_elements": [],
            "smoke_test_steps": [],
            "locator_strategies": {},
        }

        # Extract key elements - more robust pattern matching
        key_elements = []

        # Try with labeled sections first
        if "Key elements" in response_content:
            elements_section = self._extract_section(response_content, "Key elements", ["Unique identifiers", "Recommended smoke", "Suggested locator"])
            for line in elements_section.split("\n"):
                if line.strip().startswith("-") or line.strip().startswith("*"):
                    key_elements.append(line.strip()[2:].strip())

        # Fallback to heuristic extraction based on content if section headers aren't found
        if not key_elements:
            # Look for numbered or bullet lists of elements
            pattern_element = re.compile(r'(?:^|\n)(?:\d+[\.\)]|\*|\-)\s+(.*?)(?=$|\n)', re.MULTILINE)
            element_matches = pattern_element.findall(response_content)

            # Filter to likely elements (more specific patterns)
            for match in element_matches:
                text = match.strip()
                if any(keyword in text.lower() for keyword in ['button', 'input', 'field', 'form', 'link', 'element']):
                    key_elements.append(text)

        analysis_result["key_elements"] = key_elements[:10]  # Limit to top 10

        # Extract unique identifiers with enhanced pattern matching
        identifiers = []
        if "Unique identifiers" in response_content:
            identifiers_section = self._extract_section(response_content, "Unique identifiers", ["Key elements", "Recommended smoke", "Suggested locator"])
            for line in identifiers_section.split("\n"):
                if line.strip().startswith("-") or line.strip().startswith("*"):
                    identifiers.append(line.strip()[2:].strip())

        # Fallback extraction for identifiers
        if not identifiers:
            # Look for ID patterns in the response
            id_patterns = re.compile(r'(?:id|ID|Id)[\s\:]+[\"\'](#?[\w\-]+)[\"\']\s', re.MULTILINE)
            id_matches = id_patterns.findall(response_content)
            identifiers.extend(id_matches)

            # Look for title or URL as identifiers
            if page_data.get("title"):
                identifiers.append(f"Page title: {page_data.get('title')}")
            if page_data.get("url"):
                identifiers.append(f"URL: {page_data.get('url')}")

        analysis_result["unique_identifiers"] = identifiers[:5]  # Limit to top 5

        # Extract smoke test steps - more robust pattern matching
        steps = []
        if "Recommended smoke test steps" in response_content:
            steps_section = self._extract_section(response_content, "Recommended smoke test steps", ["Key elements", "Unique identifiers", "Suggested locator"])
            for line in steps_section.split("\n"):
                if line.strip().startswith("-") or line.strip().startswith("*") or bool(re.match(r'^\d+[\.\)]', line.strip())):
                    # Remove list markers (-, *, 1., etc.)
                    cleaned_step = re.sub(r'^[\-\*\d\.)+\s*]+', '', line.strip())
                    if cleaned_step:
                        steps.append(cleaned_step)

        # Fallback extraction for steps
        if not steps:
            test_keywords = ["verify", "check", "validate", "click", "enter", "navigate", "test", "assert"]
            for line in response_content.split('\n'):
                line = line.strip()
                if any(keyword in line.lower() for keyword in test_keywords) and len(line) > 10:
                    # Clean up the line to look like a step
                    if line.startswith("-") or line.startswith("*"):
                        line = line[1:].strip()
                    if bool(re.match(r'^\d+[\.\)]', line)):
                        line = re.sub(r'^\d+[\.\)]', '', line).strip()

                    steps.append(line)

        # If still no steps, generate some basic ones based on the page data
        if not steps:
            steps = [
                f"Navigate to {page_data.get('url', 'the page')}",
                f"Verify page title is '{page_data.get('title', 'correct')}'",
                "Check that the page loads without errors"
            ]

            # Add steps for forms if present
            if page_data.get("forms"):
                steps.append("Verify form is displayed")
                steps.append("Submit the form with valid data")

            # Add steps for buttons if found in elements
            buttons = [e for e in page_data.get("elements", []) if e.get("tag") == "button" or e.get("type") == "button"]
            if buttons:
                steps.append(f"Click the {buttons[0].get('text', 'submit')} button")

        analysis_result["smoke_test_steps"] = steps[:10]  # Limit to top 10

        # Extract locator strategies
        locators = {}
        if "Suggested locator strategies" in response_content:
            locators_section = self._extract_section(response_content, "Suggested locator strategies", ["Key elements", "Unique identifiers", "Recommended smoke"])
            for line in locators_section.split("\n"):
                if ":" in line and (line.strip().startswith("-") or line.strip().startswith("*")):
                    parts = line.strip()[2:].split(":", 1)
                    if len(parts) == 2:
                        element_name = parts[0].strip()
                        locator = parts[1].strip()
                        locators[element_name] = locator

        # Fallback locator strategy extraction
        if not locators:
            # Generate locators from page elements if available
            for elem in page_data.get("elements", [])[:5]:  # Just use the top 5 elements
                elem_name = elem.get("text") or elem.get("name") or elem.get("id") or f"{elem.get('tag', 'element')}_element"
                if elem.get("id"):
                    locators[elem_name] = f"By ID: #{elem.get('id')}"
                elif elem.get("name"):
                    locators[elem_name] = f"By name: {elem.get('name')}"
                elif elem.get("class"):
                    locators[elem_name] = f"By class: .{elem.get('class').split()[0]}"
                elif elem.get("xpath"):
                    locators[elem_name] = f"XPath: {elem.get('xpath')}"

        analysis_result["locator_strategies"] = locators

        logger.info(f"Analysis extracted: {len(key_elements)} key elements, {len(steps)} test steps")
        return analysis_result

    def _extract_section(self, text, section_name, other_sections):
        """Extract a section from the text based on section name and other section markers."""
        # Find the start of the section
        start_idx = text.find(section_name)
        if (start_idx == -1):
            return ""

        # Skip to the content after the section name
        start_idx = text.find("\n", start_idx)
        if (start_idx == -1):
            return ""

        # Find the end of the section (next section or end of text)
        end_idx = len(text)
        for other_section in other_sections:
            section_idx = text.find(other_section, start_idx)
            if (section_idx != -1 and section_idx < end_idx):
                end_idx = section_idx

        # Extract the section content
        section_content = text[start_idx:end_idx].strip()
        return section_content

    def analyze_page_with_vision(self, page_data):
        """
        Analyze page with enhanced vision-based analysis in steps:
        1. Capture screenshot if not already present
        2. Visual analysis of screenshot using vision capabilities
        3. DOM structure analysis
        4. Combine visual and DOM insights
        """
        try:
            # Step 1: Ensure we have a screenshot
            if "screenshot_path" not in page_data or not os.path.exists(page_data["screenshot_path"]):
                logger.info("Screenshot not found in page data. Capturing screenshot.")
                screenshot_path = self._capture_screenshot(page_data)
                if screenshot_path:
                    page_data["screenshot_path"] = screenshot_path
                else:
                    logger.warning("Failed to capture screenshot. Proceeding with DOM-only analysis.")
                    return self.analyze_page(page_data)

            # Step 2: Analyze screenshot with vision capabilities
            logger.info(f"Starting vision analysis of screenshot: {page_data['screenshot_path']}")
            visual_analysis = self._analyze_screenshot(page_data["screenshot_path"])

            if not visual_analysis:
                logger.warning("Vision analysis failed or returned empty results. Proceeding with DOM-only analysis.")
                return self.analyze_page(page_data)

            # Step 3: Get DOM structure analysis with reduced data
            logger.info("Starting DOM structure analysis")
            dom_analysis = self._analyze_dom_structure(page_data)

            # Step 4: Combine analyses for comprehensive insights
            logger.info("Combining vision and DOM analyses")
            combined_analysis = self._combine_analyses(visual_analysis, dom_analysis)

            return combined_analysis

        except Exception as e:
            logger.error(f"Error in vision-enhanced analysis: {str(e)}", exc_info=True)
            logger.info("Falling back to standard DOM analysis")
            return self.analyze_page(page_data)

    def _capture_screenshot(self, page_data):
        """
        Capture a screenshot if driver is available, otherwise return None.
        """
        try:
            # Check if we have access to a WebDriver instance
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service

            # Create output directory for screenshots if it doesn't exist
            screenshot_dir = os.path.join(self.config.OUTPUT_DIR, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Generate a safe filename from the URL
            from urllib.parse import urlparse
            url = page_data.get("url", "unknown_page")
            parsed_url = urlparse(url)
            filename = parsed_url.netloc.replace(".", "_") + parsed_url.path.replace("/", "_")
            if not filename:
                filename = "unknown_page"

            screenshot_path = os.path.join(screenshot_dir, f"{filename}.png")

            # Initialize Chrome in headless mode
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")

            service = None
            if self.config.CHROME_DRIVER_PATH:
                service = Service(executable_path=self.config.CHROME_DRIVER_PATH)

            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Navigate to the URL and capture screenshot
            driver.get(url)
            driver.save_screenshot(screenshot_path)
            driver.quit()

            logger.info(f"Captured screenshot: {screenshot_path}")
            return screenshot_path

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}", exc_info=True)
            return None

    def _analyze_screenshot(self, screenshot_path: str) -> dict:
        """
        Analyze screenshot using GPT-4o-mini's vision capabilities to identify visual elements and layout.
        """
        try:
            if not os.path.exists(screenshot_path):
                logger.error(f"Screenshot file not found: {screenshot_path}")
                return {}

            # Optimize the screenshot before sending to API
            from .screenshot_utils import optimize_screenshot  # Use the new utility function
            screenshot_base64, image_format = optimize_screenshot(
                screenshot_path,
                max_dimension=self.config.SCREENSHOT_MAX_DIMENSION,  # Cap max dimension at 1280px
                quality=self.config.SCREENSHOT_QUALITY  # Use 75% JPEG quality
            )

            if not screenshot_base64:
                logger.warning("Failed to optimize screenshot. Vision analysis may be limited.")
                # Fallback to reading the original file
                with open(screenshot_path, "rb") as image_file:
                    screenshot_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                    image_format = "png"

            logger.info(f"Analyzing optimized screenshot from: {screenshot_path}")

            # Create the prompt for visual analysis
            prompt = """
            Analyze this webpage screenshot for smoke testing purposes. Identify:

            1. Main UI sections and their layout
            2. Interactive elements (buttons, forms, links, inputs)
            3. Navigation elements and their positions
            4. Potential test scenarios based on visual elements
            5. Suggested element locators (IDs, classes, or XPaths)

            Format your response with these sections:
            - VISUAL_SECTIONS: List the main visual sections
            - INTERACTIVE_ELEMENTS: List interactive elements with descriptions
            - TEST_SCENARIOS: Suggest 3-5 smoke test scenarios
            - ELEMENT_LOCATORS: Suggest locator strategies for key elements
            """

            # Use the OpenAI client directly with vision capabilities
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # Using vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{image_format};base64,{screenshot_base64}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=self.config.VISUAL_ANALYSIS_TOKENS,
            )

            # Extract the content from the response
            analysis_text = response.choices[0].message.content
            logger.info("Screenshot analysis completed successfully")

            # Parse the structured sections from the response
            return {
                "visual_sections": self._extract_sections_from_response(analysis_text),
                "visual_elements": self._extract_elements_from_response(analysis_text),
                "test_scenarios": self._extract_test_scenarios_from_response(analysis_text),
                "element_locators": self._extract_locators_from_response(analysis_text),
                "raw_analysis": analysis_text  # Store the full analysis for reference
            }

        except Exception as e:
            logger.error(f"Error analyzing screenshot with vision: {str(e)}", exc_info=True)
            return {}

    def _extract_test_scenarios_from_response(self, response: str) -> list:
        """Extract test scenarios from the formatted response."""
        try:
            if "TEST_SCENARIOS" in response:
                scenarios_section = response.split("TEST_SCENARIOS:")[1].split("ELEMENT_LOCATORS:")[0]
                scenarios = [s.strip() for s in scenarios_section.strip().split("\n") if s.strip()]
                return [s[2:] if s.startswith("- ") else s for s in scenarios]
            return []
        except Exception:
            return []

    def _extract_locators_from_response(self, response: str) -> dict:
        """Extract element locators from the formatted response."""
        try:
            locators = {}
            if "ELEMENT_LOCATORS" in response:
                locators_section = response.split("ELEMENT_LOCATORS:")[1].strip()
                lines = [l.strip() for l in locators_section.split("\n") if l.strip()]

                for line in lines:
                    if ":" in line and line.startswith("- "):
                        line = line[2:]  # Remove the list marker
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            element_name = parts[0].strip()
                            locator = parts[1].strip()
                            locators[element_name] = locator

            return locators
        except Exception:
            return {}

    def _analyze_dom_structure(self, page_data: dict) -> dict:
        """Analyze DOM structure with minimal data."""
        try:
            # Use existing analyze_page but with reduced scope
            simplified_data = {
                "url": page_data["url"],
                "title": page_data["title"],
                "elements": self._simplify_elements_for_analysis(page_data.get("elements", []), max_elements=3),
                "forms": self._simplify_elements_for_analysis(page_data.get("forms", []), max_elements=2)
            }

            # Analyze with reduced prompt
            dom_prompt = ChatPromptTemplate.from_template(
                """
                Analyze these DOM elements and identify key testing points.
                Focus only on the most critical elements.
                {format_instructions}
                """
            )

            return self.analyze_page(simplified_data)
        except Exception as e:
            logger.error(f"Error in DOM structure analysis: {str(e)}", exc_info=True)
            return {}

    def _simplify_elements_for_analysis(self, elements, max_elements=3):
        """Helper method to simplify elements for DOM analysis."""
        if not isinstance(elements, list):
            return []

        # Sort elements by importance (prefer elements with IDs, then with text content)
        def element_importance(elem):
            has_id = elem.get('id', '') != ''
            has_text = elem.get('text', '') != ''
            has_name = elem.get('name', '') != ''
            return (has_id, has_text, has_name)

        sorted_elements = sorted(elements, key=element_importance, reverse=True)

        # Take the top N elements
        simplified = []
        for elem in sorted_elements[:max_elements]:
            simple_elem = {}
            # Only keep the most important attributes
            for key in ['id', 'tag', 'type', 'name', 'text', 'class']:
                if key in elem and elem[key]:
                    # Truncate text values to reduce token count
                    if isinstance(elem[key], str) and len(elem[key]) > 100:
                        simple_elem[key] = elem[key][:100] + "..."
                    else:
                        simple_elem[key] = elem[key]
            simplified.append(simple_elem)

        return simplified

    def _combine_analyses(self, visual_analysis: dict, dom_analysis: dict) -> dict:
        """
        Combine visual and DOM analyses for comprehensive insights.

        Args:
            visual_analysis: Results from screenshot vision analysis
            dom_analysis: Results from DOM structure analysis

        Returns:
            dict: Combined analysis with enhanced test recommendations
        """
        # Start with the DOM analysis as base
        combined = dom_analysis.copy() if dom_analysis else {}

        # Add or enhance with visual insights
        if (visual_analysis):
            # Add visual sections if not in DOM analysis
            if "visual_sections" in visual_analysis and visual_analysis["visual_sections"]:
                combined["page_sections"] = visual_analysis["visual_sections"]

            # Enhance element identification with visual elements
            if "visual_elements" in visual_analysis and visual_analysis["visual_elements"]:
                if "key_elements" not in combined:
                    combined["key_elements"] = []
                combined["key_elements"].extend(visual_analysis["visual_elements"])
                # Remove duplicates
                combined["key_elements"] = list(set(combined["key_elements"]))

            # Add test scenarios from visual analysis
            if "test_scenarios" in visual_analysis and visual_analysis["test_scenarios"]:
                combined["test_scenarios"] = visual_analysis["test_scenarios"]

            # Add element locators from visual analysis
            if "element_locators" in visual_analysis and visual_analysis["element_locators"]:
                if "locator_strategies" not in combined:
                    combined["locator_strategies"] = {}
                combined["locator_strategies"].update(visual_analysis["element_locators"])

            # Generate enhanced test steps
            if "test_scenarios" in visual_analysis and visual_analysis["test_scenarios"]:
                combined["smoke_test_steps"] = self._generate_combined_test_steps(
                    visual_analysis,
                    combined.get("smoke_test_steps", [])
                )

            # Add the raw analysis for reference
            if "raw_analysis" in visual_analysis:
                combined["vision_analysis"] = visual_analysis["raw_analysis"]

        return combined

    def _extract_sections_from_response(self, response: str) -> list:
        """Extract section information from visual analysis response."""
        sections = []
        # Simple extraction logic - can be enhanced
        for line in response.split('\n'):
            if any(keyword in line.lower() for keyword in ['section', 'layout', 'area', 'region']):
                sections.append(line.strip())
        return sections

    def _extract_elements_from_response(self, response: str) -> list:
        """Extract element information from visual analysis response."""
        elements = []
        # Simple extraction logic - can be enhanced
        for line in response.split('\n'):
            if any(keyword in line.lower() for keyword in ['button', 'input', 'link', 'form', 'menu']):
                elements.append(line.strip())
        return elements

    def _generate_combined_test_steps(self, visual_analysis, dom_steps):
        """
        Generate combined test steps from visual analysis and DOM steps.

        Args:
            visual_analysis (dict): Visual analysis results
            dom_steps (list): DOM-based test steps

        Returns:
            list: Combined test steps
        """
        combined_steps = []

        # Add test scenarios from visual analysis
        if "test_scenarios" in visual_analysis and visual_analysis["test_scenarios"]:
            # Convert scenarios to steps
            for scenario in visual_analysis["test_scenarios"]:
                # Split multi-step scenarios
                if " and " in scenario:
                    parts = scenario.split(" and ")
                    for part in parts:
                        combined_steps.append(part.strip())
                else:
                    combined_steps.append(scenario)

        # Add steps from DOM analysis if not duplicative
        for step in dom_steps:
            # Check if step is substantively similar to any existing step
            is_duplicate = False
            for existing_step in combined_steps:
                if self._are_steps_similar(step, existing_step):
                    is_duplicate = True
                    break

            if not is_duplicate:
                combined_steps.append(step)

        # If no steps, add a basic fallback step
        if not combined_steps:
            combined_steps = ["Verify page loads correctly", "Check page title is as expected"]

        return combined_steps

    def _are_steps_similar(self, step1, step2):
        """
        Determine if two test steps are substantively similar.

        Args:
            step1 (str): First test step
            step2 (str): Second test step

        Returns:
            bool: True if steps are similar, False otherwise
        """
        # Convert to lowercase for comparison
        s1 = step1.lower()
        s2 = step2.lower()

        # Check for high similarity
        if s1 == s2:
            return True

        # Check if one is a substring of the other
        if s1 in s2 or s2 in s1:
            return True

        # Check if they have similar keywords
        important_keywords = ["verify", "check", "validate", "enter", "click", "submit", "login", "select"]
        for keyword in important_keywords:
            if keyword in s1 and keyword in s2:
                # Check for additional context similarity
                s1_words = set(s1.split())
                s2_words = set(s2.split())
                common_words = s1_words.intersection(s2_words)

                # If they share a significant number of words, consider them similar
                if len(common_words) >= 3 or len(common_words) / len(s1_words.union(s2_words)) > 0.5:
                    return True

        return False

    def _analyze_layout(self, page_data):
        """Analyze layout based on DOM structure and positioning."""
        layout_analysis = {
            "sections": page_data.get("logical_sections", []),
            "hierarchy": self._extract_hierarchy_info(page_data.get("dom_structure", {})),
            "recommendations": []
        }

        # Add recommendations based on layout
        if page_data.get("forms"):
            layout_analysis["recommendations"].append("Verify form layout and field alignment")

        if page_data.get("headings"):
            layout_analysis["recommendations"].append("Validate heading hierarchy and visibility")

        return layout_analysis

    def _extract_hierarchy_info(self, dom_structure):
        """Extract useful hierarchy information from DOM structure."""
        if not dom_structure:
            return {}

        return {
            "main_elements": self._get_main_elements(dom_structure),
            "interactive_elements": self._get_interactive_elements(dom_structure)
        }

    def _get_main_elements(self, structure):
        """Get main structural elements."""
        main_elements = []
        if isinstance(structure, dict):
            tag = structure.get("tag", "")
            if tag in ["main", "header", "footer", "nav", "section", "article"]:
                main_elements.append({
                    "tag": tag,
                    "id": structure.get("id"),
                    "class": structure.get("class")
                })

            # Recursively check children
            for child in structure.get("children", []):
                main_elements.extend(self._get_main_elements(child))

        return main_elements

    def _get_interactive_elements(self, structure):
        """Get interactive elements with their context."""
        interactive = []
        if isinstance(structure, dict):
            tag = structure.get("tag", "")
            if tag in ["button", "a", "input", "select", "textarea"]:
                interactive.append({
                    "tag": tag,
                    "type": structure.get("type"),
                    "id": structure.get("id"),
                    "text": structure.get("text")
                })

            # Recursively check children
            for child in structure.get("children", []):
                interactive.extend(self._get_interactive_elements(child))

        return interactive

    def _update_test_strategies(self, analysis):
        """
        Update test strategies based on visual analysis.

        Args:
            analysis (dict): Combined analysis data
        """
        if "visual_analysis" not in analysis:
            return

        try:
            # Extract visual insights
            visual_insights = analysis["visual_analysis"]

            # Update smoke test steps with visual validations
            updated_steps = []
            for step in analysis.get("smoke_test_steps", []):
                updated_steps.append(step)

                # Add visual validation steps
                if "click" in step.lower() or "submit" in step.lower():
                    updated_steps.append("Verify visual state after interaction")

            analysis["smoke_test_steps"] = updated_steps

            # Add visual locator strategies
            if "locator_strategies" not in analysis:
                analysis["locator_strategies"] = {}

            analysis["locator_strategies"]["visual"] = {
                "layout_based": "Use relative positioning for dynamic elements",
                "visual_anchors": "Use stable visual elements as anchors"
            }

        except Exception as e:
            logger.error(f"Error updating test strategies: {str(e)}")

    def generate_test_script(self, page_analysis, framework="selenium", language="java"):
        """
        Generate both Gherkin feature file, step definitions, and page object for the given framework (default: selenium in Java).
        """
        feature_result = self._generate_cucumber_script(page_analysis, language=language)
        return {
            "feature_file": feature_result.get("feature_file", ""),
            "step_definitions": feature_result.get("step_definitions", ""),
            "page_object": feature_result.get("page_object", ""),
            "framework": framework,
            "language": language,
            "url": page_analysis.get("url", ""),
            "title": page_analysis.get("title", "")
        }

    def _generate_automation_script(self, page_analysis, framework="selenium", language="java"):
        """
        Use the LLM to generate an automation script for the specified framework and language.
        """
        prompt = f"""
You are an expert test automation engineer. Given the following web page analysis, generate a complete {framework} automation script in {language} that implements a smoke test for this page. The script should cover login if required, navigation, and basic assertions. Use best practices for the chosen framework and language.

PAGE ANALYSIS:
{json.dumps(page_analysis, indent=2)}

Return only the code, no explanation.
"""
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def _generate_cucumber_script(self, page_analysis, language="java"):
        """
        Generate Cucumber script (feature file, step definitions, page object).

        Args:
            page_analysis (dict): Page analysis
            language (str): Programming language

        Returns:
            dict: Generated scripts
        """
        try:
            # Setup response schemas
            response_schemas = [
                ResponseSchema(
                    name="feature_file",
                    description="Cucumber feature file with scenarios based on page analysis",
                    type="string",
                ),
                ResponseSchema(
                    name="step_definitions",
                    description=f"Step definitions in {language} to implement the scenarios",
                    type="string",
                ),
                ResponseSchema(
                    name="page_object",
                    description=f"Page object in {language} for interacting with UI elements",
                    type="string",
                ),
            ]

            # Setup output parser
            output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
            format_instructions = output_parser.get_format_instructions()

            # Format the prompt with the page analysis
            formatted_prompt = self._format_test_generation_prompt(
                page_analysis,
                language=language,
                format_instructions=format_instructions,
            )

            try:
                # Get response from LLM
                response = self.llm.invoke(formatted_prompt)

                try:
                    # Try to parse the structured output
                    parsed_output = output_parser.parse(response.content)
                except Exception as parse_error:
                    logger.error(f"JSON parsing error: {str(parse_error)}")

                    # Log the actual response content for debugging
                    logger.info(f"Response content: {response.content}")

                    # Fall back to simple extraction of code blocks
                    parsed_output = self._extract_code_blocks_with_enhanced_regex(response.content)

                # Add metadata
                parsed_output["url"] = page_analysis.get("url", "")
                parsed_output["title"] = page_analysis.get("title", "")
                parsed_output["language"] = language

                return parsed_output

            except Exception as e:
                logger.error(f"Error generating Cucumber script: {str(e)}")
                return {
                    "url": page_analysis.get("url", ""),
                    "title": page_analysis.get("title", ""),
                    "error": str(e),
                    "feature_file": f"# Error generating feature file: {str(e)}",
                    "step_definitions": f"// Error generating step definitions: {str(e)}",
                    "page_object": f"// Error generating page object: {str(e)}",
                }

        except Exception as outer_e:
            logger.error(f"Outer error in Cucumber script generation: {str(outer_e)}")
            return {
                "url": page_analysis.get("url", ""),
                "title": page_analysis.get("title", ""),
                "error": str(outer_e),
                "feature_file": "# Error in test generation",
                "step_definitions": "// Error in test generation",
                "page_object": "// Error in test generation",
            }

    def _extract_interactions_from_user_flow(self, page_data):
        """
        Extract all successful interactions from user flow data.

        Args:
            page_data (dict): Page data that might contain user_flow

        Returns:
            dict: Extracted interactions, credentials, and sequence information
        """
        result = {
            "username": None,
            "password": None,
            "interactions": [],
            "successful_actions": [],
            "verified_flow": False,
            "sequence": []
        }

        if not page_data or "user_flow" not in page_data:
            return result

        user_flow = page_data.get("user_flow", [])

        # Extract all successful interactions
        for step in user_flow:
            if not step.get("success", False):
                continue

            description = step.get("description", "").lower()
            result["successful_actions"].append(description)

            # Track the sequence of actions
            action = {
                "description": description,
                "url": step.get("url"),
                "type": None,
                "element": None,
                "value": None
            }

            # Extract action type and details
            if description.startswith("click "):
                action["type"] = "click"
                action["element"] = description[6:].strip()

            elif description.startswith("type "):
                action["type"] = "type"
                parts = description[5:].strip().split(" into ")
                if len(parts) == 2:
                    action["value"] = parts[0].strip()
                    action["element"] = parts[1].strip()

                    # Store common credentials if found
                    if "username" in parts[1] or "email" in parts[1] or "user" in parts[1]:
                        result["username"] = parts[0].strip()
                    elif "password" in parts[1] or "pwd" in parts[1]:
                        result["password"] = parts[0].strip()

            elif description.startswith("select "):
                action["type"] = "select"
                parts = description[7:].strip().split(" from ")
                if len(parts) == 2:
                    action["value"] = parts[0].strip()
                    action["element"] = parts[1].strip()

            # Add any other interaction types here
            # e.g., checkboxes, radio buttons, drag-and-drop, etc.

            # Add to interactions list and sequence
            if action["type"]:
                result["interactions"].append(action)
                result["sequence"].append(action)

        # Determine if we have a verified flow
        result["verified_flow"] = len(result["successful_actions"]) > 0 and (
            # Did we complete a submission?
            any("submit" in action for action in result["successful_actions"]) or
            any("login" in action for action in result["successful_actions"]) or
            # Did we do a click after entering data?
            (result["username"] or result["password"]) and any("click" in action for action in result["successful_actions"])
        )

        return result

    # Replace the old _extract_credentials_from_user_flow function usage in _format_test_generation_prompt
    def _format_test_generation_prompt(self, page_analysis, language="java", format_instructions=""):
        """
        Format the test generation prompt with page analysis data.

        Args:
            page_analysis (dict): Page analysis data
            language (str): Programming language for implementation
            format_instructions (str): Format instructions for the output parser

        Returns:
            list: Formatted messages for the LLM
        """
        # Add examples of well-formed feature files and step definitions
        example_features = """
        Feature: Smoke-QA

            Scenario: verify home page
                Given user launches browser in "Edge"
                And user opens URL "QA_URL"
                And user verifies "My Tasks" is "present" on screen
                And user verifies "My Products" is "present" on screen

            Scenario: verify new product page
                Given user launches browser in "Edge"
                And user opens URL "QA_URL"
                When user mouse hover the link "Products"
                And user click on the link "New Product"
                And user verifies "New Product Steps" is "present" on screen

            Background: User Logged in
                Given I open the url "SOMEURL"
                When I add "UserName" to the inputfield "UserName"
                When I add "pwd" to the inputfield "word"
                And I click on the Login element "Login"
                And I pause for 2000 ms
                Then I expect that the url is "SOMEURL"
        """

        example_steps = """
            @Given("I am on the login page")
            public void iAmOnTheLoginPage() {
                loginPage.navigateTo();
                Assert.assertTrue(loginPage.isPageLoaded());
            }

            @When("I enter {string} into the username field")
            public void iEnterIntoTheUsernameField(String username) {
                loginPage.enterUsername(username);
            }
        """

        # Extract user flow data if available
        interactions = self._extract_interactions_from_user_flow(page_analysis.get("raw_page_data", {}))

        # Create user flow section for the prompt
        user_flow_str = ""
        if interactions["verified_flow"]:
            user_flow_str = "VERIFIED USER INTERACTIONS:\n"

            if interactions["username"] or interactions["password"]:
                user_flow_str += "USER CREDENTIALS:\n"
                if interactions["username"]:
                    user_flow_str += f"- Verified Username: {interactions['username']}\n"
                if interactions["password"]:
                    user_flow_str += f"- Verified Password: {interactions['password']}\n"

            user_flow_str += "\nACTION SEQUENCE:\n"
            for i, action in enumerate(interactions["sequence"]):
                user_flow_str += f"{i+1}. {action['description']}\n"

            user_flow_str += "\nIMPORTANT: Use these verified interactions in your test cases as they are known to work.\n"

        # Extract page information
        url = page_analysis.get("url", "")
        title = page_analysis.get("title", "")

        # Create a summary from vision analysis if available
        vision_analysis = page_analysis.get("vision_analysis", "")
        page_analysis_summary = vision_analysis[:500] if vision_analysis else "No vision analysis available"

        # Prepare test scenarios from either source
        test_scenarios = page_analysis.get("test_scenarios", [])
        if not test_scenarios and "smoke_test_steps" in page_analysis:
            # Create scenarios from steps if dedicated scenarios not available
            test_scenarios = ["Verify " + step for step in page_analysis.get("smoke_test_steps", [])[:3]]

        # Format data for the prompt
        unique_identifiers_str = json.dumps(page_analysis.get("unique_identifiers", []), indent=2)
        key_elements_str = json.dumps(page_analysis.get("key_elements", []), indent=2)
        test_scenarios_str = json.dumps(test_scenarios, indent=2)
        smoke_test_steps_str = json.dumps(page_analysis.get("smoke_test_steps", []), indent=2)
        locator_strategies_str = json.dumps(page_analysis.get("locator_strategies", {}), indent=2)

        # Prepare the prompt with extra emphasis on proper JSON formatting
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert in automated testing using Cucumber with {language}.

            EXAMPLE FEATURE FILE:
            {example_features}

            EXAMPLE STEP DEFINITIONS:
            {example_steps}

            Generate Cucumber test scripts for the following page based on the analysis:

            PAGE URL: {url}
            PAGE TITLE: {title}

            PAGE ANALYSIS:
            {page_analysis_summary}

            {user_flow}

            UNIQUE IDENTIFIERS:
            {unique_identifiers}

            KEY ELEMENTS:
            {key_elements}

            TEST SCENARIOS:
            {test_scenarios}

            SMOKE TEST STEPS:
            {smoke_test_steps}

            LOCATOR STRATEGIES:
            {locator_strategies}

            Generate the following files:
            1. A Cucumber feature file (.feature) for smoke testing this page
            2. Step definitions that implement the feature file steps
            3. A page object model for this page

            IMPORTANT GUIDELINES:
            - If verified credentials are provided, use them in your test scenarios
            - Create tests based on the successful user flow actions if available
            - Do NOT assume this is a login page unless explicitly mentioned in the analysis
            - Create tests based on the actual page purpose and elements discovered
            - The code should follow best practices for the {language} framework and include appropriate comments
            - Handle potential errors and edge cases
            - Keep scenarios focused on main user flows for the specific page type

            {format_instructions}
            """
        )

        # Create the formatted prompt and return it
        return prompt.format_messages(
            url=url,
            title=title,
            example_features=example_features,
            example_steps=example_steps,
            page_analysis_summary=page_analysis_summary,
            unique_identifiers=unique_identifiers_str,
            key_elements=key_elements_str,
            test_scenarios=test_scenarios_str,
            smoke_test_steps=smoke_test_steps_str,
            locator_strategies=locator_strategies_str,
            language=language,
            format_instructions=format_instructions,
            user_flow=user_flow_str,
        )

    def parse_json_safely(self, json_str):
        """
        Parse JSON with error handling and more robust recovery attempts.
        """
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing error: {str(e)}. Attempting recovery...")

            # Try fixing common JSON issues
            try:
                # Replace single quotes with double quotes for keys and string values
                fixed_json = re.sub(r"(\w+)\':", r'"\1":', json_str)
                fixed_json = re.sub(r"\'(\w+)\'", r'"\1"', fixed_json)
                return json.loads(fixed_json)
            except json.JSONDecodeError:
                # Try more aggressive fixing - extract braced content
                match = re.search(r"\{.*\}", json_str, re.DOTALL)
                if match:
                    try:
                        return json.loads(match.group(0))
                    except json.JSONDecodeError:
                        pass

                logger.error(f"Failed to parse JSON even after recovery attempts: {json_str[:100]}...")
                return None

    def parse_llm_json_response(response_content):
        """
        More robust parser for LLM-generated JSON responses that might have formatting issues.
        """
        try:
            # First try standard parsing
            return json.loads(response_content)
        except json.JSONDecodeError:
            # Try to extract JSON block if it's embedded in markdown or text
            json_pattern = r'```json\s*([\s\S]*?)\s*```'
            json_matches = re.findall(json_pattern, response_content)

            if json_matches:
                for json_content in json_matches:
                    try:
                        return json.loads(json_content)
                    except json.JSONDecodeError:
                        continue

            # If that fails, try common fixes for JSON formatting issues
            try:
                # Fix missing quotes around keys
                fixed_content = re.sub(r'(\s*?)(\w+)(\s*?):', r'\1"\2"\3:', response_content)
                return json.loads(fixed_content)
            except json.JSONDecodeError:
                # Other common fixes can be added here
                pass

            # Fall back to regex-based extraction as a last resort
            logger.warning("JSON parsing recovery attempts failed, falling back to regex extraction")
            return _extract_code_blocks_with_enhanced_regex(response_content)

    @staticmethod
    def _extract_code_blocks_with_enhanced_regex(content):
        """
        Enhanced version of code block extraction with better edge case handling.
        """
        logger.info("Falling back to regex-based code block extraction")
        feature_file = ""
        step_definitions = ""
        page_object = ""

        # Extract feature file (multiple approaches)
        feature_patterns = [
            r"```(?:gherkin|feature|cucumber)\n(.*?)```",
            r"```feature\n(.*?)```",
            r"Feature:(.*?)(?=```|Scenario:|Background:|@|\n\n\n)",
            r"# Language: gherkin\n(.*?)(?=```)"
        ]

        for pattern in feature_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                feature_file = match.group(1).strip()
                if feature_file and not feature_file.startswith("Feature:"):
                    feature_file = "Feature: " + feature_file
                break

        # Scan for content that looks like a feature file if no explicit feature block
        if not feature_file:
            for line in content.split("\n"):
                if line.strip().startswith("Feature:") or line.strip().startswith("Scenario:"):
                    feature_start_idx = content.find(line)
                    feature_content = content[feature_start_idx:]

                    # Find a reasonable end for the feature content
                    end_markers = ["```", "public class", "import", "@Given"]
                    end_idx = len(feature_content)

                    for marker in end_markers:
                        marker_idx = feature_content.find(marker)
                        if marker_idx > 0 and marker_idx < end_idx:
                            end_idx = marker_idx

                    feature_file = feature_content[:end_idx].strip()
                    break

        # Extract step definitions
        step_patterns = [
            r"```(?:java|step(?:s)?|stepdef(?:s)?)\n(.*?public class.*?(?:Steps|StepDefinitions).*?)```",
            r"```java\n(.*?)```",
            r"(?:public class|import).*?(?:Steps|StepDefinitions)(.*?)(?=```|\n\n\n|public class)",
        ]

        for pattern in step_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                step_content = match.group(1).strip()
                # Check if this is actually step definitions and not page object
                if "@Given" in step_content or "@When" in step_content or "@Then" in step_content:
                    step_definitions = step_content
                    break

        # Extract page object
        page_patterns = [
            r"```(?:java|pageobject|page)\n(.*?public class.*?(?:Page|PageObject).*?)```",
            r"public class\s+\w+(?:Page|PageObject)(.*?)(?=```|\n\n\n|public class|@Given)",
        ]

        for pattern in page_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                page_content = match.group(1).strip()
                # Check if this is actually a page object
                if "WebElement" in page_content or "findElement" in page_content or "driver" in page_content:
                    page_object = page_content
                    break

        # If no explicit step definitions or page object found, try to infer from the content
        if not step_definitions:
            # Look for @Given, @When, @Then annotations
            for block in re.findall(r"```java\n(.*?)```", content, re.DOTALL):
                if "@Given" in block or "@When" in block or "@Then" in block:
                    step_definitions = block
                    break

        if not page_object:
            # Look for a class with "Page" in the name or WebElement members
            for block in re.findall(r"```java\n(.*?)```", content, re.DOTALL):
                if "class" in block and ("Page" in block or "WebElement" in block):
                    if not ("@Given" in block or "@When" in block or "@Then" in block):  # Not step definitions
                        page_object = block
                        break

        logger.info(f"Extraction results - Feature file: {bool(feature_file)}, Step definitions: {bool(step_definitions)}, Page object: {bool(page_object)}")

        return {
            "feature_file": feature_file or "# Error extracting feature file",
            "step_definitions": step_definitions or "// Error extracting step definitions",
            "page_object": page_object or "// Error extracting page object"
        }

    def generate_test_script_with_retry(self, page_analysis, framework="cucumber", language="java", max_retries=2):
        """
        Generate test script with retry mechanism, using the direct text approach.

        Args:
            page_analysis (dict): Analysis results from analyze_page
            framework (str): Test framework to generate script for
            language (str): Programming language for implementation
            max_retries (int): Maximum number of retries

        Returns:
            dict: Generated test script information
        """
        # Use the direct raw approach which is more reliable
        try:
            raw_response = self.generate_test_script_raw(page_analysis, framework, language)
            # Parse the raw response into sections
            return self._parse_raw_test_script(raw_response, page_analysis)
        except Exception as e:
            logger.error(f"Error with raw test script generation: {str(e)}")
            # Create a fallback response
            url = page_analysis.get("url", "")
            title = page_analysis.get("title", "Unknown Page")
            return {
                "url": url,
                "title": title,
                "feature_file": f"Feature: Error fallback for {title}\n\nScenario: Verify page loads\n  Given I open the url \"{url}\"\n  Then I expect the page title contains \"{title}\"",
                "step_definitions": f"// Error in generation: {str(e)}",
                "page_object": f"// Error in generation: {str(e)}"
            }

    def generate_test_script_raw(self, page_analysis, framework="selenium", language="java"):
        """
        Generate test script based on page analysis and return the raw unprocessed response.
        This avoids JSON parsing issues by returning the direct LLM output.
        """
        try:
            prompt = f"""
You are an expert test automation engineer. Given the following web page analysis, generate:

1. A Gherkin feature file for a smoke test of the page.
2. Java step definitions for Selenium using Cucumber annotations, implementing the steps in the feature file.
3. A Java Page Object class for the page.

Return your response in the following format, with each section clearly marked:

FEATURE FILE:
[Place the Gherkin feature file here]

STEP DEFINITIONS:
[Place the Java step definitions here]

PAGE OBJECT:
[Place the Java Page Object class here]

Do not include any explanation or extra text. Only output the code in the specified sections.

WEB PAGE ANALYSIS:
{json.dumps(page_analysis, indent=2)}
"""
            logger.info(f"Generating test script for {page_analysis.get('url', '')} with framework {framework}")
            response = self.llm.invoke(prompt)
            logger.info(f"Raw LLM output:\n{response.content}")
            return response.content
        except Exception as e:
            logger.error(f"Error generating raw test script: {str(e)}")
            # Return a basic fallback script
            return f"""
            FEATURE FILE:
            Feature: Basic test for {page_analysis.get('title', 'Unknown Page')}

            Scenario: Verify page loads
              Given I open the url "{page_analysis.get('url', '')}"
              Then I verify the page loads

            STEP DEFINITIONS:
            // Error occurred: {str(e)}
            // Basic step definitions

            PAGE OBJECT:
            // Error occurred: {str(e)}
            // Basic page object
            """

    def _parse_raw_test_script(self, raw_script, page_analysis):
        """
        Parse a raw test script response into its component parts.
        """
        result = {
            "url": page_analysis.get("url", ""),
            "title": page_analysis.get("title", "Unknown Page"),
            "feature_file": "",
            "step_definitions": "",
            "page_object": ""
        }
        patterns = {
            "feature_file": r"FEATURE FILE:\s*(.*?)(?=\n[A-Z ]+?:|\Z)",
            "step_definitions": r"STEP DEFINITIONS:\s*(.*?)(?=\n[A-Z ]+?:|\Z)",
            "page_object": r"PAGE OBJECT:\s*(.*?)(?=\n[A-Z ]+?:|\Z)"
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, raw_script, re.DOTALL | re.IGNORECASE)
            if match:
                result[key] = match.group(1).strip()
            else:
                if key == "feature_file":
                    result[key] = f"Feature: {result['title']}\n\nScenario: Verify page loads\n  Given I open the url \"{result['url']}\"\n  Then I verify the page loads"
                else:
                    result[key] = f"// No content generated for {key}"
        return result

    def is_login_page(self, page_data, screenshot_path):
        """
        Use the LLM to determine if the given page is a login page.
        Args:
            page_data (dict): The extracted page data
            screenshot_path (str): Path to the screenshot file
        Returns:
            bool: True if the page is a login page, False otherwise
        """
        # Read screenshot as bytes
        with open(screenshot_path, "rb") as f:
            screenshot_bytes = f.read()
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

        # Prepare prompt
        prompt = (
            "You are an expert web QA assistant. Given the following page data and screenshot, "
            "determine if this is a login page. "
            "A login page typically has username/email and password fields, and a login/submit button. "
            "Reply with only 'yes' or 'no'.\n"
            f"Page data: {json.dumps(page_data)[:2000]}\n"  # Truncate for safety
        )

        # Use OpenAI vision model if available, else fallback to text only
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"}}
                    ]}
                ],
                max_tokens=10,
            )
            answer = response.choices[0].message.content.strip().lower()
        except Exception as e:
            logger.warning(f"Vision model failed, falling back to text only: {e}")
            # Fallback: text only
            response = self.llm.invoke(prompt)
            answer = response.content.strip().lower()

        return answer.startswith("yes")
