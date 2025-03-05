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

logger = logging.getLogger(__name__)


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

    def analyze_page(self, page_data):
        """
        Analyze page data to identify key elements for testing.

        Args:
            page_data (dict): Page data extracted by the crawler

        Returns:
            dict: Analysis results with test recommendations
        """
        # Set up the response schema for structured output
        response_schemas = [
            ResponseSchema(
                name="page_title_validation",
                description="Text that should be present in the page title to validate correct page loading",
            ),
            ResponseSchema(
                name="unique_identifiers",
                description="List of unique elements that can be used to verify the page loaded correctly",
            ),
            ResponseSchema(
                name="key_elements",
                description="List of key interactive elements that should be verified",
            ),
            ResponseSchema(
                name="smoke_test_steps",
                description="Step-by-step smoke test procedure for this page",
            ),
            ResponseSchema(
                name="locator_strategies",
                description="Recommended locator strategies for important elements",
            ),
        ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # Prepare the prompt
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert in automated testing for web applications.

            Analyze the following page data and provide recommendations for smoke testing.

            PAGE URL: {url}
            PAGE TITLE: {title}

            INTERACTIVE ELEMENTS:
            {interactive_elements}

            FRAMES DETECTED:
            {frames}

            FORMS DETECTED:
            {forms}

            HEADINGS STRUCTURE:
            {headings}

            Based on this information, provide:
            1. What text should be present in the page title to validate correct page loading
            2. Unique identifiers or elements that can be used to verify the page loaded correctly
            3. Key interactive elements that should be verified for a smoke test
            4. Step-by-step smoke test procedure for this page
            5. Recommended locator strategies for the important elements

            {format_instructions}
            """
        )

        # Format the input data
        interactive_elements_str = json.dumps(page_data.get("elements", []), indent=2)
        frames_str = json.dumps(page_data.get("frames", []), indent=2)
        forms_str = json.dumps(page_data.get("forms", []), indent=2)
        headings_str = json.dumps(page_data.get("headings", []), indent=2)

        # Create the formatted prompt
        formatted_prompt = prompt.format_messages(
            url=page_data["url"],
            title=page_data["title"],
            interactive_elements=interactive_elements_str,
            frames=frames_str,
            forms=forms_str,
            headings=headings_str,
            format_instructions=format_instructions,
        )

        try:
            # Get response from LLM
            response = self.llm.invoke(formatted_prompt)

            # Parse the structured output
            parsed_output = output_parser.parse(response.content)

            # Add additional metadata
            parsed_output["url"] = page_data["url"]
            parsed_output["title"] = page_data["title"]

            return parsed_output

        except Exception as e:
            logger.error(f"Error analyzing page with LLM: {str(e)}")
            return {
                "url": page_data["url"],
                "title": page_data["title"],
                "error": str(e),
                "page_title_validation": page_data["title"],
                "unique_identifiers": [],
                "key_elements": [],
                "smoke_test_steps": ["Error generating smoke test steps"],
                "locator_strategies": {},
            }

    def generate_test_script(self, page_analysis, framework="cucumber"):
        """
        Generate test script based on page analysis.

        Args:
            page_analysis (dict): Analysis results from analyze_page
            framework (str): Test framework to generate script for

        Returns:
            dict: Generated test script information
        """
        if framework.lower() == "cucumber":
            return self._generate_cucumber_script(page_analysis)
        else:
            logger.warning(f"Unsupported framework: {framework}")
            return {"error": f"Unsupported framework: {framework}"}


    def _generate_cucumber_script(self, page_analysis):
        """
        Generate Cucumber/Gherkin test script.

        Args:
            page_analysis (dict): Analysis results from analyze_page

        Returns:
            dict: Generated Cucumber script files
        """
        # Set up the response schema for structured output
        response_schemas = [
            ResponseSchema(
                name="feature_file",
                description="Gherkin feature file content for testing this page",
            ),
            ResponseSchema(
                name="step_definitions",
                description="Step definitions implementation (for your existing framework)",
            ),
            ResponseSchema(
                name="page_object",
                description="Page object model implementation for this page",
            ),
        ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # Prepare the prompt with extra emphasis on proper JSON formatting
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert in automated testing using Cucumber with {language}.

            Generate Cucumber test scripts for the following page based on the analysis:

            PAGE URL: {url}
            PAGE TITLE: {title}

            PAGE TITLE VALIDATION: {page_title_validation}

            UNIQUE IDENTIFIERS:
            {unique_identifiers}

            KEY ELEMENTS:
            {key_elements}

            SMOKE TEST STEPS:
            {smoke_test_steps}

            LOCATOR STRATEGIES:
            {locator_strategies}

            Generate the following files:
            1. A Cucumber feature file (.feature) for smoke testing this page
            2. Step definitions that implement the feature file steps
            3. A page object model for this page

            The code should follow best practices for the {language} framework and include appropriate comments.
            Handle potential errors and edge cases.

            CRITICAL: Your response MUST be valid JSON that follows this structure exactly:
            {{
            "feature_file": "Feature: ... (full feature file content)",
            "step_definitions": "package ... (full step definitions code)",
            "page_object": "package ... (full page object code)"
            }}

            Make sure to properly escape all quotes and special characters in the code.
            Do not add any explanation text outside of this JSON structure.

            {format_instructions}
            """
        )

        # Determine the language based on framework preference
        language = "Java"  # Default

        # Format the input data
        unique_identifiers_str = json.dumps(
            page_analysis.get("unique_identifiers", []), indent=2
        )
        key_elements_str = json.dumps(page_analysis.get("key_elements", []), indent=2)
        smoke_test_steps_str = json.dumps(
            page_analysis.get("smoke_test_steps", []), indent=2
        )
        locator_strategies_str = json.dumps(
            page_analysis.get("locator_strategies", {}), indent=2
        )

        # Create the formatted prompt
        formatted_prompt = prompt.format_messages(
            url=page_analysis["url"],
            title=page_analysis["title"],
            page_title_validation=page_analysis.get("page_title_validation", ""),
            unique_identifiers=unique_identifiers_str,
            key_elements=key_elements_str,
            smoke_test_steps=smoke_test_steps_str,
            locator_strategies=locator_strategies_str,
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
                logger.debug(f"Response content: {response.content}")

                # Fall back to simple extraction of code blocks
                content = response.content
                feature_file = ""
                step_definitions = ""
                page_object = ""

                # Try to extract code blocks with regex
                import re

                # Look for feature file (Gherkin syntax)
                feature_match = re.search(r"```gherkin\n(.*?)```", content, re.DOTALL)
                if feature_match:
                    feature_file = feature_match.group(1)
                else:
                    feature_match = re.search(r"```feature\n(.*?)```", content, re.DOTALL)
                    if feature_match:
                        feature_file = feature_match.group(1)
                    else:
                        # Look for content that looks like a feature file
                        for line in content.split("\n"):
                            if line.startswith("Feature:") or line.startswith("Scenario:"):
                                # Extract the whole block
                                start_idx = content.find(line)
                                feature_block = content[start_idx:]
                                end_idx = feature_block.find("```")
                                if end_idx > 0:
                                    feature_file = feature_block[:end_idx].strip()
                                else:
                                    feature_file = line
                                break

                # Look for Java code blocks
                java_blocks = re.findall(r"```java\n(.*?)```", content, re.DOTALL)

                # If we found Java blocks, try to determine which is which
                if len(java_blocks) >= 2:
                    for block in java_blocks:
                        if "class" in block and ("Page" in block or "PO" in block):
                            page_object = block
                        elif "Given" in block or "When" in block or "Then" in block:
                            step_definitions = block

                    # If we couldn't distinguish, just assign them in order
                    if not page_object and len(java_blocks) > 0:
                        page_object = java_blocks[0]
                    if not step_definitions and len(java_blocks) > 1:
                        step_definitions = java_blocks[1]

                # Create a fallback parsed output
                parsed_output = {
                    "feature_file": feature_file or "# Error extracting feature file",
                    "step_definitions": step_definitions
                    or "// Error extracting step definitions",
                    "page_object": page_object or "// Error extracting page object",
                }

            # Add metadata
            parsed_output["url"] = page_analysis["url"]
            parsed_output["title"] = page_analysis["title"]
            parsed_output["language"] = language

            return parsed_output

        except Exception as e:
            logger.error(f"Error generating Cucumber script: {str(e)}")
            return {
                "url": page_analysis["url"],
                "title": page_analysis["title"],
                "error": str(e),
                "feature_file": f"# Error generating feature file: {str(e)}",
                "step_definitions": f"// Error generating step definitions: {str(e)}",
                "page_object": f"// Error generating page object: {str(e)}",
            }
