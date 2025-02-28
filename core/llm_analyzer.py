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

    def __init__(self, config=None):
        """
        Initialize the LLM analyzer.

        Args:
            config (Config): Configuration object
        """
        self.config = config or Config()

        # Initialize OpenAI client
        self.llm = ChatOpenAI(
            openai_api_key=self.config.OPENAI_API_KEY,
            model=self.config.LLM_MODEL,
            temperature=0.1,
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

        # Prepare the prompt
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

            # Parse the structured output
            parsed_output = output_parser.parse(response.content)

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
