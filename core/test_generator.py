# core/test_generator.py - Add your implementation here

# core/test_generator.py
import os
import json
import logging
from config.config import Config
from core.llm_analyzer import LLMAnalyzer
from core.utils.path_utils import ensure_directory_exists, normalize_path

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

        # Ensure output directory exists (create parent directories if needed)
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
        successful_pages = 0
        failed_pages = 0
        for url, page_data in all_pages.items():
            try:
                # Skip if page data is incomplete (unless it's pre-analyzed data)
                if discovered_pages_data is None and not all(key in page_data for key in ["url", "title"]):
                    logger.warning(f"Skipping incomplete page data for {url}")
                    continue

                logger.info(f"Generating tests for {url}")

                # If this is pre-analyzed data, use it directly
                if discovered_pages_data:
                    # Check if we already have analysis data embedded in the page data
                    if "analysis" in page_data:
                        logger.info(f"Using pre-generated analysis for {url}")
                        page_analysis = page_data["analysis"]
                    else:
                        # Otherwise check for screenshot and do vision analysis if needed
                        has_screenshot = "screenshot_path" in page_data and os.path.exists(page_data["screenshot_path"])

                        if use_vision and has_screenshot:
                            logger.info(f"Using vision-enhanced analysis for {url} with screenshot: {page_data['screenshot_path']}")
                            try:
                                # Use vision-based analysis
                                page_analysis = self.llm_analyzer.analyze_page_with_vision(page_data)
                                logger.info(f"Vision analysis completed successfully for {url}")
                            except Exception as vision_err:
                                logger.error(f"Vision analysis failed for {url}: {str(vision_err)}")
                                logger.info(f"Falling back to standard analysis for {url}")
                                page_analysis = self.llm_analyzer.analyze_page(page_data)
                        else:
                            if use_vision:
                                logger.warning(f"Vision analysis requested but screenshot not available for {url}")
                            logger.info(f"Using standard analysis for {url}")
                            page_analysis = self.llm_analyzer.analyze_page(page_data)
                else:
                    # Otherwise analyze page with LLM
                    if use_vision and "screenshot_path" in page_data and os.path.exists(page_data["screenshot_path"]):
                        logger.info(f"Using vision-enhanced analysis for {url}")
                        page_analysis = self.llm_analyzer.analyze_page_with_vision(page_data)
                    else:
                        logger.info(f"Using standard analysis for {url}")
                        page_analysis = self.llm_analyzer.analyze_page(page_data)

                # Generate test script with raw page data included for user flow extraction
                if "user_flow" in page_data:
                    # Store the raw page data that contains user flow information
                    page_analysis["raw_page_data"] = page_data

                # Use the raw approach to test generation to avoid JSON parsing issues
                try:
                    # Add the url to the analysis if not present
                    if "url" not in page_analysis:
                        page_analysis["url"] = url

                    # Add the title to the analysis if not present
                    if "title" not in page_analysis and "title" in page_data:
                        page_analysis["title"] = page_data["title"]

                    logger.info(f"Generating raw test script for {url}")
                    test_script = self.llm_analyzer.generate_test_script_with_retry(
                        page_analysis,
                        framework,
                        max_retries=1
                    )

                    # Ensure test_script has the minimal required fields
                    if not all(key in test_script for key in ["feature_file", "step_definitions", "page_object"]):
                        logger.warning(f"Test script for {url} is missing required fields, creating basic fallback")

                        # Create a basic fallback
                        title = page_data.get('title', 'Unknown Page')
                        test_script = {
                            "url": url,
                            "title": title,
                            "feature_file": f"Feature: Basic test for {title}\n\nScenario: Verify page loads\n  Given I open the url \"{url}\"\n  Then I expect the page title contains \"{title}\"",
                            "step_definitions": f"// Basic step definitions for {url}",
                            "page_object": f"// Basic page object for {url}"
                        }
                except Exception as script_gen_error:
                    logger.error(f"Failed to generate test script for {url}: {str(script_gen_error)}")
                    # Create a basic fallback
                    title = page_data.get('title', 'Unknown Page')
                    test_script = {
                        "url": url,
                        "title": title,
                        "error": str(script_gen_error),
                        "feature_file": f"Feature: Error fallback for {title}\n\nScenario: Verify page loads\n  Given I open the url \"{url}\"\n  Then I expect the page title contains \"{title}\"",
                        "step_definitions": f"// Error in generation for {url}: {str(script_gen_error)}",
                        "page_object": f"// Error in generation for {url}: {str(script_gen_error)}"
                    }

                # Add to generated tests
                generated_tests[url] = test_script

                # Save test files with additional error handling
                try:
                    self._save_test_files(test_script, url, output_dir, framework, language)
                    successful_pages += 1
                except Exception as save_error:
                    logger.error(f"Failed to save test files for {url}: {str(save_error)}")
                    failed_pages += 1

            except Exception as e:
                logger.error(f"Unhandled error generating tests for {url}: {str(e)}")
                failed_pages += 1
                continue

        # Log summary of processing
        logger.info(f"Test generation complete: {successful_pages} successful, {failed_pages} failed out of {len(all_pages)} total pages")

        # Generate test suite file
        try:
            self._generate_test_suite(generated_tests, output_dir, framework, language)
        except Exception as suite_error:
            logger.error(f"Error generating test suite: {str(suite_error)}")

        # Return the generated tests dictionary
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
        Save generated test scripts to files directly without complex parsing.

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

            # Directly write the content without trying to parse JSON structure
            # This avoids issues with quotes and escaping

            # Write feature file - handle both dict format and raw string format
            feature_content = test_script.get("feature_file", "")
            if feature_content:
                feature_file = os.path.join(page_type_dir, f"{safe_url}_spec.feature")
                with open(feature_file, "w", encoding="utf-8") as f:
                    # Strip any markdown code block markers if present
                    if isinstance(feature_content, str):
                        feature_content = feature_content.replace("```feature", "").replace("```gherkin", "").replace("```", "").strip()
                    f.write(feature_content)
                logger.info(f"Feature file saved: {feature_file}")

            # Write step definitions
            steps_content = test_script.get("step_definitions", "")
            if steps_content:
                if language == "java":
                    # For Java, write to Java file based on page type
                    class_name = self._pascal_case(safe_url) + "Steps"
                    step_file = os.path.join(page_type_dir, f"{class_name}.java")
                else:
                    # For other languages, adjust as needed
                    step_file = os.path.join(page_type_dir, f"{safe_url}_steps.{language}")

                with open(step_file, "w", encoding="utf-8") as f:
                    # Strip any markdown code block markers if present
                    if isinstance(steps_content, str):
                        steps_content = steps_content.replace("```java", "").replace("```", "").strip()
                    f.write(steps_content)
                logger.info(f"Step definitions saved: {step_file}")

            # Write page object
            page_object_content = test_script.get("page_object", "")
            if page_object_content:
                if language == "java":
                    # For Java, create a proper class file
                    page_class_name = self._pascal_case(safe_url) + "Page"
                    page_file = os.path.join(page_type_dir, f"{page_class_name}.java")
                else:
                    # For other languages, adjust as needed
                    page_file = os.path.join(page_type_dir, f"{safe_url}_page.{language}")

                with open(page_file, "w", encoding="utf-8") as f:
                    # Strip any markdown code block markers if present
                    if isinstance(page_object_content, str):
                        page_object_content = page_object_content.replace("```java", "").replace("```", "").strip()
                    f.write(page_object_content)
                logger.info(f"Page object saved: {page_file}")

            # Add page type tag to feature files for better organization
            if framework == "cucumber" and feature_content:
                # Read the file back
                with open(feature_file, "r", encoding="utf-8") as f:
                    feature_text = f.read()

                # Add tag if not already present
                if not feature_text.strip().startswith("@"):
                    tag_line = f"@{page_type.lower().replace(' ', '-')}\n"
                    with open(feature_file, "w", encoding="utf-8") as f:
                        f.write(tag_line + feature_text)
                    logger.info(f"Added page type tag to feature file: {feature_file}")

            logger.info(f"Generated test files for {url} in {page_type_dir}")
            return True

        except Exception as e:
            logger.error(f"Error saving test files for {url}: {str(e)}")
            # Create emergency fallback files if we can
            try:
                emergency_dir = os.path.join(output_dir, "emergency_fallback")
                os.makedirs(emergency_dir, exist_ok=True)
                safe_url = self._safe_filename(url)

                # Create basic feature file as fallback
                feature_content = f"Feature: Emergency fallback for {url}\n\nScenario: Basic page verification\n  Given I open the url \"{url}\"\n  Then I verify the page loads"
                with open(os.path.join(emergency_dir, f"{safe_url}_emergency.feature"), "w", encoding="utf-8") as f:
                    f.write(feature_content)

                logger.info(f"Created emergency fallback test for {url}")
                return False
            except Exception as fallback_error:
                logger.error(f"Failed to create emergency fallback: {str(fallback_error)}")
                return False

    def _determine_page_type(self, test_script_or_title, url=None):
        """
        Determine the page type based on the test script content and analysis.
        Can be called with either a test_script object or with title and url.

        Args:
            test_script_or_title (dict or str): Either the test script object or page title
            url (str, optional): URL of the page, only used if first param is a string

        Returns:
            str: Page type (login, form, landing, content, etc.)
        """
        # Default page type
        page_type = "general"

        # Check if first argument is a test script object or a title string
        if isinstance(test_script_or_title, dict):
            # It's a test script object
            test_script = test_script_or_title

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
        else:
            # It's a title string with URL
            title = str(test_script_or_title).lower()
            url = str(url).lower() if url else ""

            # Determine type based on title and URL keywords
            if any(term in title or term in url for term in ["login", "sign in", "signin", "log in"]):
                return "login"
            elif any(term in title or term in url for term in ["register", "signup", "sign up", "create account"]):
                return "registration"
            elif any(term in title or term in url for term in ["contact", "feedback", "support"]):
                return "form"
            elif any(term in title or term in url for term in ["dashboard", "overview", "home"]):
                return "dashboard"
            elif any(term in title or term in url for term in ["profile", "account", "settings"]):
                return "profile"
            elif any(term in title or term in url for term in ["product", "item", "detail"]):
                return "detail"
            elif any(term in title or term in url for term in ["cart", "basket", "checkout", "payment"]):
                return "checkout"
            elif any(term in title or term in url for term in ["search", "find", "results"]):
                return "search"
            elif any(term in title or term in url for term in ["list", "catalog", "gallery"]):
                return "listing"
            elif "home" in title or url.endswith('/') or url.endswith('index'):
                return "landing"

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

    def generate_page_object_map(self, output_dir):
        """Generate a map of all page objects for easier navigation between tests."""
        all_page_objects = []

        # Find all Java files that look like page objects
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith("Page.java"):
                    # Extract page class name
                    page_class = os.path.splitext(file)[0]

                    # Get relative path
                    rel_path = os.path.relpath(os.path.join(root, file), output_dir)

                    all_page_objects.append({
                        "className": page_class,
                        "filePath": rel_path
                    })

        # Create a PageObjectFactory if we have page objects
        if all_page_objects:
            factory_path = os.path.join(output_dir, "PageObjectFactory.java")

            with open(factory_path, "w") as f:
                f.write("""import org.openqa.selenium.WebDriver;

/**
 * Factory for creating page objects to simplify test maintenance.
 */
public class PageObjectFactory {
    private WebDriver driver;

    public PageObjectFactory(WebDriver driver) {
        this.driver = driver;
    }

""")

                # Add methods for each page
                for page in all_page_objects:
                    class_name = page["className"]
                    method_name = class_name[0].lower() + class_name[1:]

                    f.write(f"""    /**
     * Get an instance of {class_name}
     */
    public {class_name} get{class_name}() {{
        return new {class_name}(driver);
    }}

""")

                f.write("}\n")

            logger.info(f"Generated PageObjectFactory: {factory_path}")

            # Create a BaseTest class for setup
            base_test_path = os.path.join(output_dir, "BaseTest.java")

            with open(base_test_path, "w") as f:
                f.write("""import io.cucumber.java.After;
import io.cucumber.java.Before;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Base test class for setting up and tearing down WebDriver.
 */
public class BaseTest {
    protected static WebDriver driver;
    protected static PageObjectFactory pages;

    @Before
    public void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");

        driver = new ChromeDriver(options);
        driver.manage().window().maximize();

        // Initialize the page factory
        pages = new PageObjectFactory(driver);
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}
""")

            logger.info(f"Generated BaseTest: {base_test_path}")

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

    def generate_tests_from_sitemap(
        self,
        sitemap,
        output_dir=None,
        framework="cucumber",
        language="java",
        use_vision=False,
        max_pages=None,
        web_crawler=None
    ):
        """
        Generate tests from a pre-generated sitemap.

        Args:
            sitemap: Dictionary mapping URLs to their metadata, or path to sitemap file
            output_dir: Directory to output generated tests
            framework: Test framework to generate for
            language: Programming language to use
            use_vision: Whether to use vision-enhanced analysis
            max_pages: Maximum number of pages to process
            web_crawler: Optional WebCrawler instance to use

        Returns:
            dict: Dictionary of generated test files
        """
        from core.sitemap_loader import SitemapLoader

        # Set default paths if not provided
        output_dir = output_dir or os.path.join(self.config.OUTPUT_DIR, "test_scripts")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Process sitemap input
        sitemap_data = {}
        if isinstance(sitemap, str):
            # It's a file path
            sitemap_loader = SitemapLoader(self.config)
            urls = sitemap_loader.load_sitemap_from_file(sitemap)
            sitemap_data = sitemap_loader.prepare_sitemap_for_testing(urls, os.path.dirname(output_dir))
        else:
            # It's already a dictionary
            sitemap_data = sitemap

        # Generate tests for each URL
        all_pages = {}
        from core.crawler import WebCrawler
        crawler = web_crawler or WebCrawler(self.config)

        try:
            # Limit the number of pages if specified
            urls = list(sitemap_data.keys())
            if max_pages and len(urls) > max_pages:
                logger.info(f"Limiting to {max_pages} pages from {len(urls)} total")
                urls = urls[:max_pages]

            # Process each URL
            for url in urls:
                logger.info(f"Extracting page data for {url}")
                try:
                    # Extract page data
                    page_data = crawler.extract_page_data(url, with_screenshots=use_vision)
                    all_pages[url] = page_data
                except Exception as e:
                    logger.error(f"Error extracting page data for {url}: {str(e)}")
                    continue

            # Generate tests for the extracted pages
            return self.generate_tests(
                discovered_pages_data=all_pages,
                output_dir=output_dir,
                framework=framework,
                language=language,
                use_vision=use_vision
            )

        finally:
            if crawler and crawler != web_crawler:
                crawler.close()

    def save_test_files(self, url, tests, output_dir):
        try:
            # Create a safe filename from the URL
            safe_filename = self._create_safe_filename(url)

            # Normalize and ensure the output path exists
            file_path = normalize_path(os.path.join(output_dir, f"{safe_filename}_spec.feature"))
            ensure_directory_exists(file_path)

            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(tests)

            self.logger.info(f"Test files saved for {url}")
            return file_path
        except Exception as e:
            self.logger.error(f"Error saving test files for {url}: {str(e)}")
            return None
