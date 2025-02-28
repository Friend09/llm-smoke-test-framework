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
        output_dir=None,
        framework="cucumber",
        language="java",
    ):
        """
        Generate test scripts for discovered pages.

        Args:
            discovered_pages_file (str): Path to discovered pages JSON file
            output_dir (str): Directory to output generated tests
            framework (str): Test framework to generate for
            language (str): Programming language to use

        Returns:
            dict: Dictionary of generated test files
        """
        # Set default paths if not provided
        discovered_pages_file = discovered_pages_file or os.path.join(
            self.config.OUTPUT_DIR, "discovered_pages", "all_pages.json"
        )

        output_dir = output_dir or os.path.join(self.config.OUTPUT_DIR, "test_scripts")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Load discovered pages
        try:
            with open(discovered_pages_file, "r") as f:
                all_pages = json.load(f)
        except Exception as e:
            logger.error(f"Error loading discovered pages: {str(e)}")
            return {}

        # Dictionary to store generated test files
        generated_tests = {}

        # Generate tests for each page
        for url, page_data in all_pages.items():
            try:
                # Skip if page data is incomplete
                if not all(key in page_data for key in ["url", "title"]):
                    logger.warning(f"Skipping incomplete page data for {url}")
                    continue

                logger.info(f"Generating tests for {url}")

                # Analyze page with LLM
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

    def _save_test_files(self, test_script, url, output_dir, framework, language):
        """
        Save generated test files.

        Args:
            test_script (dict): Generated test script
            url (str): URL of the page
            output_dir (str): Output directory
            framework (str): Test framework
            language (str): Programming language
        """
        # Create safe filename from URL
        safe_filename = self._safe_filename(url)

        if framework.lower() == "cucumber":
            # Create feature directory
            feature_dir = os.path.join(output_dir, "features")
            os.makedirs(feature_dir, exist_ok=True)

            # Create step definitions directory
            steps_dir = os.path.join(output_dir, "step_definitions")
            os.makedirs(steps_dir, exist_ok=True)

            # Create page objects directory
            pages_dir = os.path.join(output_dir, "page_objects")
            os.makedirs(pages_dir, exist_ok=True)

            # Save feature file
            feature_file = os.path.join(feature_dir, f"{safe_filename}.feature")
            with open(feature_file, "w") as f:
                f.write(test_script.get("feature_file", "# Empty feature file"))

            # Save step definitions
            # For Java
            if language.lower() == "java":
                steps_file = os.path.join(
                    steps_dir, f"{self._pascal_case(safe_filename)}Steps.java"
                )
                with open(steps_file, "w") as f:
                    f.write(
                        test_script.get("step_definitions", "// Empty step definitions")
                    )

                # Save page object
                page_file = os.path.join(
                    pages_dir, f"{self._pascal_case(safe_filename)}Page.java"
                )
                with open(page_file, "w") as f:
                    f.write(test_script.get("page_object", "// Empty page object"))

            # For TypeScript
            elif language.lower() == "typescript":
                steps_file = os.path.join(steps_dir, f"{safe_filename}.steps.ts")
                with open(steps_file, "w") as f:
                    f.write(
                        test_script.get("step_definitions", "// Empty step definitions")
                    )

                # Save page object
                page_file = os.path.join(pages_dir, f"{safe_filename}.page.ts")
                with open(page_file, "w") as f:
                    f.write(test_script.get("page_object", "// Empty page object"))

    def _generate_test_suite(self, generated_tests, output_dir, framework, language):
        """
        Generate a test suite file that includes all tests.

        Args:
            generated_tests (dict): Dictionary of generated tests
            output_dir (str): Output directory
            framework (str): Test framework
            language (str): Programming language
        """
        if framework.lower() == "cucumber":
            # For Java
            if language.lower() == "java":
                # Create test runner directory
                runner_dir = os.path.join(output_dir, "runners")
                os.makedirs(runner_dir, exist_ok=True)

                # Generate test runner
                runner_file = os.path.join(runner_dir, "TestRunner.java")

                runner_content = """
package runners;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"step_definitions"},
    plugin = {"pretty", "html:target/cucumber-reports"},
    monochrome = true
)
public class TestRunner {
    // This class should be empty
}
"""

                with open(runner_file, "w") as f:
                    f.write(runner_content)

            # For TypeScript
            elif language.lower() == "typescript":
                # Create test runner directory
                runner_dir = os.path.join(output_dir, "runners")
                os.makedirs(runner_dir, exist_ok=True)

                # Generate test runner
                runner_file = os.path.join(runner_dir, "cucumber.conf.ts")

                runner_content = """
import { Options } from '@wdio/cli';

export const config: Options.Testrunner = {
    runner: 'local',
    specs: [
        './features/**/*.feature'
    ],
    exclude: [],
    maxInstances: 10,
    capabilities: [{
        maxInstances: 5,
        browserName: 'chrome',
        'goog:chromeOptions': {
            args: ['--headless', '--disable-gpu']
        }
    }],
    logLevel: 'info',
    bail: 0,
    baseUrl: 'http://localhost',
    waitforTimeout: 10000,
    connectionRetryTimeout: 120000,
    connectionRetryCount: 3,
    services: ['chromedriver'],
    framework: 'cucumber',
    reporters: ['spec', ['html', {
        outputDir: './reports'
    }]],
    cucumberOpts: {
        require: ['./step_definitions/**/*.ts'],
        backtrace: false,
        requireModule: ['ts-node/register'],
        dryRun: false,
        failFast: false,
        snippets: true,
        source: true,
        strict: false,
        tagExpression: '',
        timeout: 60000,
        ignoreUndefinedDefinitions: false
    }
};
"""

                with open(runner_file, "w") as f:
                    f.write(runner_content)

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
