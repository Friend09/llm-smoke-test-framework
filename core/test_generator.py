# core/test_generator.py - Add your implementation here

# core/test_generator.py
import os
import json
import logging
from config.config import Config
from core.llm_analyzer import LLMAnalyzer

logger = logging.getLogger(__name__)


class TestGenerator:
    """
    Generates test scripts from discovered pages.
    """

    def __init__(self, config=None):
        """
        Initialize the test generator.

        Args:
            config (Config): Configuration object
        """
        self.config = config or Config()
        self.llm_analyzer = LLMAnalyzer(self.config)

    def generate_tests(
        self,
        discovered_pages_file=None,
        discovered_pages_data=None,
        output_dir=None,
        framework="cucumber",
        language="java",
        use_vision=False,
    ):
        """
        Generate test scripts for discovered pages.

        Args:
            discovered_pages_file (str): Path to discovered pages JSON file
            discovered_pages_data (dict): Pre-analyzed page data (optional)
            output_dir (str): Directory to output generated tests
            framework (str): Test framework to generate for
            language (str): Programming language to use
            use_vision (bool): Whether to use vision-enhanced analysis

        Returns:
            dict: Dictionary of generated test files
        """
        # Set default paths if not provided
        output_dir = output_dir or os.path.join(self.config.OUTPUT_DIR, "test_scripts")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Dictionary to store generated test files
        generated_tests = {}

        # Use pre-analyzed data if provided, otherwise load from file
        all_pages = {}
        if discovered_pages_data:
            logger.info("Using pre-analyzed page data")
            all_pages = discovered_pages_data
        elif discovered_pages_file:
            try:
                discovered_pages_file = discovered_pages_file or os.path.join(
                    self.config.OUTPUT_DIR, "discovered_pages", "all_pages.json"
                )
                with open(discovered_pages_file, "r") as f:
                    all_pages = json.load(f)
                logger.info(f"Loaded {len(all_pages)} pages from {discovered_pages_file}")
            except Exception as e:
                logger.error(f"Error loading discovered pages: {str(e)}")
                return {}
        else:
            logger.error("No page data provided")
            return {}

        # Generate tests for each page
        for url, page_data in all_pages.items():
            try:
                # Skip if page data is incomplete (unless it's pre-analyzed data)
                if discovered_pages_data is None and not all(key in page_data for key in ["url", "title"]):
                    logger.warning(f"Skipping incomplete page data for {url}")
                    continue

                logger.info(f"Generating tests for {url}")

                # If this is pre-analyzed data, use it directly
                if discovered_pages_data:
                    page_analysis = page_data
                else:
                    # Otherwise analyze page with LLM
                    if use_vision and "screenshot_path" in page_data and os.path.exists(page_data["screenshot_path"]):
                        logger.info(f"Using vision-enhanced analysis for {url}")
                        page_analysis = self.llm_analyzer.analyze_page_with_vision(page_data)
                    else:
                        logger.info(f"Using standard analysis for {url}")
                        page_analysis = self.llm_analyzer.analyze_page(page_data)

                # Generate test script
                test_script = self.llm_analyzer.generate_test_script(
                    page_analysis, framework
                )

                # Add to generated tests
                generated_tests[url] = test_script

                # Save test files
                self._save_test_files(test_script, url, output_dir, framework, language)

            except Exception as e:
                logger.error(f"Error generating tests for {url}: {str(e)}")
                continue

        # Generate test suite file
        self._generate_test_suite(generated_tests, output_dir, framework, language)

        return generated_tests

    def generate_login_tests(self):
        """Generate login-specific test cases"""
        test_cases = [
            {
                "name": "test_successful_login",
                "description": "Verify successful login with valid credentials",
                "steps": [
                    f"Navigate to {self.config.LOGIN_URL}",
                    f"Enter username: {self.config.TEST_USERNAME}",
                    f"Enter password: {self.config.TEST_PASSWORD}",
                    "Click login button",
                    f"Verify success message: {self.config.SUCCESS_MESSAGE}",
                ],
            }
        ]

        if self.config.GENERATE_NEGATIVE_TESTS:
            test_cases.extend(
                [
                    {
                        "name": "test_invalid_username",
                        "description": "Verify error message with invalid username",
                        "steps": [
                            f"Navigate to {self.config.LOGIN_URL}",
                            "Enter invalid username",
                            f"Enter password: {self.config.TEST_PASSWORD}",
                            "Click login button",
                            "Verify error message",
                        ],
                    },
                    {
                        "name": "test_invalid_password",
                        "description": "Verify error message with invalid password",
                        "steps": [
                            f"Navigate to {self.config.LOGIN_URL}",
                            f"Enter username: {self.config.TEST_USERNAME}",
                            "Enter invalid password",
                            "Click login button",
                            "Verify error message",
                        ],
                    },
                ]
            )

        return test_cases

    def _save_test_files(self, test_script, url, output_dir, framework, language):
        """
        Save generated test scripts to files.

        Args:
            test_script (dict): Generated test script
            url (str): URL of the page
            output_dir (str): Output directory
            framework (str): Test framework to generate for
            language (str): Programming language to use
        """
        try:
            # Create safe filename from URL
            safe_url = self._safe_filename(url)
            page_title = test_script.get("title", "Unknown Page")

            # Determine page type from analysis
            page_type = self._determine_page_type(test_script)

            # Create subdirectory for page type
            page_type_dir = os.path.join(output_dir, page_type)
            os.makedirs(page_type_dir, exist_ok=True)

            # Write feature file
            feature_file = os.path.join(page_type_dir, f"{safe_url}_spec.feature")
            with open(feature_file, "w", encoding="utf-8") as f:
                f.write(test_script["feature_file"])

            # Write step definitions
            if language == "java":
                # For Java, write to Java file based on page type
                class_name = self._pascal_case(safe_url) + "Steps"
                step_file = os.path.join(page_type_dir, f"{class_name}.java")
                with open(step_file, "w", encoding="utf-8") as f:
                    f.write(test_script["step_definitions"])

                # Write page object
                page_class_name = self._pascal_case(safe_url) + "Page"
                page_file = os.path.join(page_type_dir, f"{page_class_name}.java")
                with open(page_file, "w", encoding="utf-8") as f:
                    f.write(test_script["page_object"])
            else:
                # For other languages, adjust as needed
                step_file = os.path.join(page_type_dir, f"{safe_url}_steps.{language}")
                with open(step_file, "w", encoding="utf-8") as f:
                    f.write(test_script["step_definitions"])

                # Write page object
                page_file = os.path.join(page_type_dir, f"{safe_url}_page.{language}")
                with open(page_file, "w", encoding="utf-8") as f:
                    f.write(test_script["page_object"])

            logger.info(f"Generated test files for {url} in {page_type_dir}")

        except Exception as e:
            logger.error(f"Error saving test files for {url}: {str(e)}")

    def _determine_page_type(self, test_script):
        """
        Determine the page type based on the test script content and analysis.

        Args:
            test_script (dict): Generated test script

        Returns:
            str: Page type (login, form, landing, content, etc.)
        """
        # Default page type
        page_type = "general"

        # Extract feature file content
        feature_content = test_script.get("feature_file", "").lower()
        steps_content = test_script.get("step_definitions", "").lower()

        # Check for common page types
        if "login" in feature_content and ("username" in feature_content or "password" in feature_content):
            page_type = "login"
        elif "register" in feature_content or "sign up" in feature_content or "registration" in feature_content:
            page_type = "registration"
        elif "checkout" in feature_content or "payment" in feature_content or "purchase" in feature_content:
            page_type = "checkout"
        elif "search" in feature_content and "results" in feature_content:
            page_type = "search"
        elif "form" in feature_content and "submit" in feature_content:
            page_type = "form"
        elif "cart" in feature_content or "shopping cart" in feature_content:
            page_type = "cart"
        elif "dashboard" in feature_content or "overview" in feature_content:
            page_type = "dashboard"
        elif "profile" in feature_content or "account" in feature_content:
            page_type = "profile"
        elif "listing" in feature_content or "list" in feature_content:
            page_type = "listing"
        elif "detail" in feature_content or "product" in feature_content:
            page_type = "detail"
        elif "landing" in feature_content or "home" in feature_content:
            page_type = "landing"

        return page_type

    def _generate_test_suite(self, generated_tests, output_dir, framework, language):
        """
        Generate a test suite file that includes all tests.

        Args:
            generated_tests (dict): Dictionary of generated tests
            output_dir (str): Output directory
            framework (str): Test framework to generate for
            language (str): Programming language to use
        """
        try:
            # Create output directories
            os.makedirs(output_dir, exist_ok=True)

            if framework == "cucumber":
                # Structure by page types
                page_types = {}

                # Group tests by page type
                for url, test_script in generated_tests.items():
                    page_type = self._determine_page_type(test_script)
                    safe_url = self._safe_filename(url)

                    if page_type not in page_types:
                        page_types[page_type] = []

                    page_types[page_type].append({
                        "url": url,
                        "safe_url": safe_url,
                        "title": test_script.get("title", "Unknown Page")
                    })

                # Generate test runner for Java
                if language == "java":
                    # Write test suite runner
                    suite_file = os.path.join(output_dir, "TestSuite.java")
                    with open(suite_file, "w", encoding="utf-8") as f:
                        f.write("""
import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"stepdefinitions"},
    plugin = {"pretty", "html:target/cucumber-reports"}
)
public class TestSuite {
    // This class will run all Cucumber tests
}
                        """)

                    # Write README
                    readme_file = os.path.join(output_dir, "README.md")
                    with open(readme_file, "w", encoding="utf-8") as f:
                        f.write("# Generated Test Suite\n\n")
                        f.write("This test suite contains smoke tests for the following pages:\n\n")

                        # List all page types and tests
                        for page_type, pages in page_types.items():
                            f.write(f"## {page_type.title()} Pages\n\n")
                            for page in pages:
                                f.write(f"- [{page['title']}]({page['url']})\n")
                            f.write("\n")

                        f.write("## Running the Tests\n\n")
                        f.write("To run the tests, use the following command:\n\n")
                        f.write("```bash\n")
                        f.write("mvn test\n")
                        f.write("```\n")

                logger.info(f"Generated test suite in {output_dir}")

        except Exception as e:
            logger.error(f"Error generating test suite: {str(e)}")

    def generate_tests_by_page_type(self, page_type, output_dir=None, framework="cucumber", language="java"):
        """
        Specialized test generation for specific page types.

        Args:
            page_type (str): Type of page to generate tests for (login, form, etc.)
            output_dir (str): Directory to output generated tests
            framework (str): Test framework to generate for
            language (str): Programming language to use

        Returns:
            dict: Dictionary of generated test files
        """
        generated_tests = {}

        # Create page-type specific output directory
        output_dir = output_dir or os.path.join(self.config.OUTPUT_DIR, "test_scripts")
        page_type_dir = os.path.join(output_dir, page_type)
        os.makedirs(page_type_dir, exist_ok=True)

        if page_type == "login":
            login_tests = self.generate_login_tests()
            if login_tests:
                generated_tests.update(login_tests)
        # Add other specialized page type handlers here if needed

        return generated_tests

    def _safe_filename(self, url):
        """
        Convert URL to safe filename.

        Args:
            url (str): URL

        Returns:
            str: Safe filename
        """
        # Remove protocol
        filename = url.split("://")[-1]

        # Remove domain if in the base URL
        base_domain = self.config.BASE_URL.split("://")[-1].split("/")[0]
        if filename.startswith(base_domain):
            filename = filename[len(base_domain) :]

        # Remove leading/trailing slashes
        filename = filename.strip("/")

        # Replace special characters
        filename = (
            filename.replace("/", "_")
            .replace("?", "_")
            .replace("&", "_")
            .replace("=", "_")
        )
        filename = (
            filename.replace(".", "_")
            .replace(":", "_")
            .replace(";", "_")
            .replace(",", "_")
        )

        # If empty, use index
        if not filename:
            filename = "index"

        return filename

    def _pascal_case(self, snake_case):
        """
        Convert snake_case to PascalCase.

        Args:
            snake_case (str): Snake case string

        Returns:
            str: Pascal case string
        """
        # Split by underscores
        parts = snake_case.split("_")

        # Capitalize each part and join
        return "".join(part.capitalize() for part in parts)
