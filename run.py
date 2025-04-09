# run.py
import argparse
import json
import logging
import os
import sys
import urllib
import time  # Add missing import
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.config import Config
from core.crawler import WebCrawler
from core.llm_analyzer import LLMAnalyzer
from core.test_generator import TestGenerator
from core.sitemap_crawler import SitemapCrawler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('llm_smoketest.log')
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='LLM Smoke Test Framework')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Vision Analysis command
    vision_parser = subparsers.add_parser('vision', help='Analyze page with vision capabilities')
    vision_parser.add_argument('url', help='URL to crawl')
    vision_parser.add_argument('-o', '--output', help='Output filename')
    vision_parser.add_argument('-f', '--with-flow', dest='with_flow', help='User flow description file')
    vision_parser.add_argument('-s', '--with-screenshots', action='store_true', help='Force new screenshot capture')

    # Vision End-to-End command - Make URL optional when sitemap file is provided
    vision_e2e_parser = subparsers.add_parser('vision-e2e', help='End-to-end process using vision capabilities')
    vision_e2e_parser_group = vision_e2e_parser.add_mutually_exclusive_group(required=True)
    vision_e2e_parser_group.add_argument('url', nargs='?', help='URL to crawl')
    vision_e2e_parser_group.add_argument('--sitemap-file', help='Path to a pre-generated sitemap file')
    vision_e2e_parser.add_argument('-f', '--framework', default='cucumber',
                                  help='Test framework (default: cucumber)')
    vision_e2e_parser.add_argument('-o', '--output', help='Output directory prefix')
    vision_e2e_parser.add_argument('-w', '--with-flow', dest='with_flow', help='User flow description file')
    vision_e2e_parser.add_argument('-l', '--language', default='java', help='Programming language (default: java)')
    # Add site-wide support to vision-e2e
    vision_e2e_parser.add_argument('--site', action='store_true', help="Process the entire site rather than just one page")
    vision_e2e_parser.add_argument('--max-pages', type=int, default=50, help="Maximum number of pages to crawl for site-wide processing")

    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl a webpage and extract data')
    crawl_parser.add_argument('url', help='URL to crawl')
    crawl_parser.add_argument('-o', '--output', help='Output filename')
    crawl_parser.add_argument('--with-screenshots', action='store_true', help='Capture screenshots')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze page data')
    analyze_parser.add_argument('input', help='Input page data JSON file')
    analyze_parser.add_argument('-o', '--output', help='Output filename')
    analyze_parser.add_argument('--use-vision', action='store_true', help='Use vision capabilities')
    analyze_parser.add_argument('--verbose', action='store_true', help='Show detailed analysis')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate test scripts')
    generate_parser.add_argument('input', help='Input analysis JSON file')
    generate_parser.add_argument('-f', '--framework', default='cucumber',
                                help='Test framework (default: cucumber)')
    generate_parser.add_argument('-l', '--language', default='java',
                                help='Programming language (default: java)')
    generate_parser.add_argument('-o', '--output', help='Output directory')
    generate_parser.add_argument('--use-vision', action='store_true', help='Use vision-based generation')

    # End-to-end command - Make URL optional when sitemap file is provided
    e2e_parser = subparsers.add_parser('e2e', help='End-to-end process: crawl, analyze, generate')
    e2e_parser_group = e2e_parser.add_mutually_exclusive_group(required=True)
    e2e_parser_group.add_argument('url', nargs='?', help='URL to crawl')
    e2e_parser_group.add_argument('--sitemap-file', help='Path to a pre-generated sitemap file')
    e2e_parser.add_argument('-f', '--framework', default='cucumber',
                           help='Test framework (default: cucumber)')
    e2e_parser.add_argument('-l', '--language', default='java',
                           help='Programming language (default: java)')
    e2e_parser.add_argument('-o', '--output', help='Output directory prefix')
    e2e_parser.add_argument('--use-vision', action='store_true', help='Use vision capabilities')
    e2e_parser.add_argument('--with-screenshots', action='store_true', help='Capture screenshots')
    # Add site-wide support to e2e
    e2e_parser.add_argument('--site', action='store_true', help="Process the entire site rather than just one page")
    e2e_parser.add_argument('--max-pages', type=int, default=50, help="Maximum number of pages to crawl for site-wide processing")

    # Add sitemap-specific commands
    sitemap_parser = subparsers.add_parser('sitemap', help='Work with pre-generated sitemaps')
    sitemap_parser.add_argument('--file', required=True, help='Path to the sitemap file')
    sitemap_parser.add_argument('--base-url', help='Base URL to filter sitemap entries')
    sitemap_parser.add_argument('--include', nargs='+', help='URL patterns to include')
    sitemap_parser.add_argument('--exclude', nargs='+', help='URL patterns to exclude')
    sitemap_parser.add_argument('-o', '--output', help='Output directory')

    return parser.parse_args()

def crawl_page(config: Config, url: str, output_filename: Optional[str] = None, with_screenshots: bool = False) -> str:
    """Crawl a webpage and extract data.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        output_filename (Optional[str]): Output filename
        with_screenshots (bool): Whether to capture screenshots

    Returns:
        str: Path to the saved page data file
    """
    crawler = WebCrawler(config)
    try:
        logger.info(f"Starting page crawl with screenshots={with_screenshots}")
        page_data = crawler.extract_page_data(url, with_screenshots=with_screenshots)

        # Log screenshot path if it exists
        if with_screenshots and "screenshot_path" in page_data:
            if os.path.exists(page_data["screenshot_path"]):
                logger.info(f"Screenshot captured: {page_data['screenshot_path']}")
            else:
                logger.warning(f"Screenshot path recorded but file doesn't exist: {page_data['screenshot_path']}")
        elif with_screenshots:
            logger.warning("Screenshots were requested but no screenshot_path found in page data")

        output_path = crawler.save_page_data(page_data, output_filename)
        return output_path
    finally:
        crawler.close()

def analyze_page_data(config: Config, input_file: str, output_filename: Optional[str] = None) -> str:
    """Analyze page data.

    Args:
        config (Config): Configuration object
        input_file (str): Input page data JSON file
        output_filename (Optional[str]): Output filename

    Returns:
        str: Path to the saved analysis file
    """
    # Load page data
    with open(input_file, 'r', encoding='utf-8') as f:
        page_data = json.load(f)

    # Analyze page
    analyzer = LLMAnalyzer(config)
    analysis = analyzer.analyze_page(page_data)

    # Save analysis
    if output_filename is None:
        # Create a filename based on the input filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{base_name}_analysis.json"

    output_path = os.path.join(config.analysis_path, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, indent=2, fp=f)

    logger.info(f"Saved analysis to {output_path}")
    return output_path

def generate_test_scripts(config: Config, analysis_file: str, framework: str = 'cucumber',
                         language: str = 'java', output_dir: Optional[str] = None,
                         use_vision: bool = False):
    """Generate test scripts from analysis results."""
    logger.info(f"Generating test scripts from {analysis_file}")
    try:
        # Load analysis data
        if not os.path.exists(analysis_file):
            raise ValueError(f"Analysis file not found: {analysis_file}")

        with open(analysis_file, 'r') as f:
            analysis_data = json.load(f)

        # Extract URL from analysis data
        url = analysis_data.get('url', '')
        if not url:
            logger.warning(f"URL not found in analysis data, using filename as fallback")
            url = os.path.basename(analysis_file).replace('_analysis.json', '')

        # Initialize test generator
        test_gen = TestGenerator(config)

        # Determine if this is a vision analysis (either by flag or filename)
        is_vision_analysis = use_vision or "_vision_analysis.json" in analysis_file

        # Use vision capabilities if requested
        if is_vision_analysis:
            logger.info("Using vision-enhanced test generation")
            # Inject vision-specific properties if needed
            if "vision_analysis" not in analysis_data:
                logger.info("Converting standard analysis to vision-enhanced format")
                # This adapts a standard analysis for vision processing
                analysis_data["vision_analysis"] = True

        # Generate tests with the updated analysis
        generated_tests = test_gen.generate_tests(
            discovered_pages_data={url: analysis_data},
            output_dir=output_dir,
            framework=framework,
            language=language
        )

        logger.info(f"Generated {len(generated_tests)} test files")

        # Return a dictionary with the test files
        output_files = {}
        for test_url, test_script in generated_tests.items():
            safe_url = test_gen._safe_filename(test_url)
            test_file = os.path.join(output_dir or config.test_scripts_path, f"{safe_url}_spec.feature")
            output_files[f"test_{safe_url}"] = test_file

        return output_files
    except Exception as e:
        logger.error(f"Error generating test scripts: {str(e)}", exc_info=True)
        return {"error": str(e)}

def process_end_to_end(
    config: Config,
    url: str,
    framework: str = 'cucumber',
    output_prefix: Optional[str] = None
) -> Dict[str, str]:
    """Process a URL end-to-end: crawl, analyze, generate.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        framework (str): Test framework
        output_prefix (Optional[str]): Output directory prefix

    Returns:
        Dict[str, str]: Mapping of file types to their paths
    """
    if output_prefix is None:
        # Create prefix based on URL
        from urllib.parse import urlparse
        import re

        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace(".", "_")
        path = re.sub(r'[^\w]', '_', parsed_url.path)
        if not path:
            path = "home"
        output_prefix = f"{domain}_{path}"

    # Step 1: Crawl
    page_data_file = crawl_page(config, url, f"{output_prefix}.json")

    # Step 2: Analyze
    analysis_file = analyze_page_data(config, page_data_file, f"{output_prefix}_analysis.json")

    # Step 3: Generate
    output_files = generate_test_scripts(config, analysis_file, framework, output_prefix)

    # Add the page data and analysis files to the output mapping
    output_files["page_data"] = page_data_file
    output_files["analysis"] = analysis_file

    return output_files

def analyze_page_with_vision(config: Config, url: str, output_filename: Optional[str] = None, flow_file: Optional[str] = None, force_screenshot: bool = False, output_dir: Optional[str] = None) -> str:
    """Analyze page with GPT-4o-mini vision capabilities.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        output_filename (Optional[str]): Output filename
        flow_file (Optional[str]): User flow description file
        force_screenshot (bool): Whether to force a new screenshot capture
        output_dir (Optional[str]): Output directory

    Returns:
        str: Path to the saved analysis file
    """
    logger.info(f"Starting vision analysis for {url}")
    crawler = WebCrawler(config)
    try:
        # If flow file is provided, use crawl with user flow
        if (flow_file):
            if not os.path.exists(flow_file):
                logger.error(f"User flow file not found: {flow_file}")
                raise FileNotFoundError(f"User flow file not found: {flow_file}")

            with open(flow_file, 'r') as f:
                flow_description = f.read()

            if not flow_description.strip():
                logger.warning(f"User flow file is empty: {flow_file}")

            logger.info(f"Using user flow from {flow_file}")
            # Pass the output_dir parameter to ensure step screenshots are saved in the site-specific directory
            page_data = crawler.crawl_with_user_flow(url, flow_description, output_dir=output_dir)
            logger.info(f"User flow execution completed with {len(page_data.get('user_flow', []))} steps")
        else:
            # Regular crawl with screenshots enabled - pass output_dir if provided
            logger.info("Capturing page data with screenshots")
            page_data = crawler.extract_page_data(url, with_screenshots=True, output_dir=output_dir)

        # Check if page_data is valid
        if page_data is None:
            logger.error("Failed to extract page data")
            # Create minimal page data
            page_data = {
                "url": url,
                "title": "Failed to extract",
                "error": "Page data extraction failed"
            }

        # Save page data to the site-specific directory if provided
        if output_dir:
            page_data_dir = os.path.join(output_dir, "page_data")
            os.makedirs(page_data_dir, exist_ok=True)

            # Generate a safe filename
            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            page_data_file = os.path.join(page_data_dir, f"{safe_filename}.json")

            with open(page_data_file, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, indent=2)

            logger.info(f"Saved page data to {page_data_file}")
        else:
            # Use the default method if no specific output directory
            page_data_file = crawler.save_page_data(page_data)
            logger.info(f"Saved page data to {page_data_file}")

        # Ensure page_data has screenshot_path
        has_screenshot = isinstance(page_data, dict) and "screenshot_path" in page_data
        if not has_screenshot or not os.path.exists(page_data.get("screenshot_path", "")):
            logger.warning("No screenshot captured or invalid screenshot path. Taking screenshot now.")

            # Use site-specific screenshot directory if provided
            if output_dir:
                screenshot_dir = os.path.join(output_dir, "screenshots")
            else:
                screenshot_dir = os.path.join(config.OUTPUT_DIR, "screenshots")

            os.makedirs(screenshot_dir, exist_ok=True)

            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            screenshot_path = os.path.join(screenshot_dir, f"{safe_filename}.png")

            try:
                if crawler.driver:
                    crawler.driver.save_screenshot(screenshot_path)
                    if isinstance(page_data, dict):
                        page_data["screenshot_path"] = screenshot_path
                    logger.info(f"Saved screenshot to {screenshot_path}")
                else:
                    logger.error("WebDriver is not available for screenshot capture")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")

        # Analyze with vision capabilities
        logger.info("Starting LLM vision analysis")
        analyzer = LLMAnalyzer(config)

        # Check if page_data has a valid screenshot_path before vision analysis
        if isinstance(page_data, dict) and "screenshot_path" in page_data and os.path.exists(page_data["screenshot_path"]):
            analysis = analyzer.analyze_page_with_vision(page_data)
        else:
            logger.warning("No valid screenshot available. Falling back to standard analysis.")
            analysis = analyzer.analyze_page(page_data)

        # Ensure we have an analysis result
        if analysis is None:
            logger.error("Analysis returned None, creating minimal analysis")
            analysis = {
                "url": url,
                "title": page_data.get("title", "Unknown") if isinstance(page_data, dict) else "Unknown",
                "error": "Analysis failed",
                "smoke_test_steps": ["Visit the page and verify it loads"]
            }

        # Preserve user flow data in the analysis if it exists
        if isinstance(page_data, dict) and "user_flow" in page_data:
            analysis["user_flow"] = page_data["user_flow"]

        # Save analysis to the appropriate directory
        if output_dir:
            # If output_dir is provided, save analysis there
            analysis_dir = os.path.join(output_dir, "analysis")
            os.makedirs(analysis_dir, exist_ok=True)
        else:
            # Otherwise use default
            analysis_dir = config.analysis_path

        # Save analysis
        if output_filename:
            base_name = os.path.splitext(output_filename)[0]
            analysis_filename = f"{base_name}_vision_analysis.json"
        else:
            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            analysis_filename = f"{safe_filename}_vision_analysis.json"

        analysis_path = os.path.join(analysis_dir, analysis_filename)
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2)

        logger.info(f"Vision analysis completed and saved to {analysis_path}")
        return analysis_path

    except Exception as e:
        logger.error(f"Error in vision analysis: {str(e)}", exc_info=True)

        # Create fallback analysis file
        safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
        error_filename = f"{safe_filename}_error_analysis.json"
        error_path = os.path.join(config.analysis_path, error_filename)

        try:
            os.makedirs(config.analysis_path, exist_ok=True)
            with open(error_path, 'w') as f:
                error_analysis = {
                    "url": url,
                    "error": str(e),
                    "timestamp": str(datetime.now()),
                    "smoke_test_steps": ["Visit the page and verify it loads"]
                }
                json.dump(error_analysis, f, indent=2)
            logger.info(f"Created error analysis file: {error_path}")
            return error_path
        except Exception as write_error:
            logger.error(f"Failed to write error analysis: {str(write_error)}")
            raise e
    finally:
        if crawler:
            crawler.close()

def vision_e2e_process(
    config: Config,
    url: str,
    framework: str = 'cucumber',
    output_prefix: Optional[str] = None,
    flow_file: Optional[str] = None
) -> Dict[str, str]:
    """Process end-to-end with vision capabilities."""
    output_files = {}
    try:
        # Create site-specific output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        url_domain = urllib.parse.urlparse(url).netloc
        vision_output_dir = os.path.join(config.OUTPUT_DIR, output_prefix or f"vision_e2e_{url_domain}_{timestamp}")
        os.makedirs(vision_output_dir, exist_ok=True)

        # Create subdirectories within the site-specific folder
        screenshots_dir = os.path.join(vision_output_dir, "screenshots")
        analysis_dir = os.path.join(vision_output_dir, "analysis")
        page_data_dir = os.path.join(vision_output_dir, "page_data")
        test_scripts_dir = os.path.join(vision_output_dir, "test_scripts")

        # Create all needed subdirectories
        for directory in [screenshots_dir, analysis_dir, page_data_dir, test_scripts_dir]:
            os.makedirs(directory, exist_ok=True)

        # Step 1: Analyze with vision capabilities
        logger.info(f"Starting vision-based end-to-end process for {url}")
        try:
            # Use the vision-specific output directory for analysis
            analysis_file = analyze_page_with_vision(
                config,
                url,
                output_prefix,
                flow_file,
                output_dir=vision_output_dir
            )
            output_files["analysis"] = analysis_file

            # Load the analysis to use directly in test generation
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)

            has_analysis = True
        except Exception as analyze_error:
            logger.error(f"Vision analysis failed: {str(analyze_error)}")
            # Create minimal analysis for test generation
            analysis_data = {
                "url": url,
                "title": "Unknown Page",
                "error": str(analyze_error),
                "page_title_validation": "Page loads correctly",
                "unique_identifiers": [],
                "key_elements": [],
                "smoke_test_steps": ["Visit the page and verify it loads correctly"],
                "locator_strategies": {}
            }
            has_analysis = False

        # Step 2: Generate test scripts from the analysis
        try:
            test_gen = TestGenerator(config)

            # Use the site-specific test scripts directory
            logger.info(f"Generating test scripts with vision-enhanced analysis in {test_scripts_dir}")
            generated_tests = test_gen.generate_tests(
                discovered_pages_data={url: analysis_data},
                output_dir=test_scripts_dir,  # Use the site-specific directory
                framework=framework,
                language="java"  # Make sure we explicitly pass language
            )

            # Add test files to output
            for test_url, script in generated_tests.items():
                safe_url = test_gen._safe_filename(test_url)
                test_file = os.path.join(test_scripts_dir, f"{safe_url}_spec.feature")
                output_files[f"test_{safe_url}"] = test_file

            logger.info(f"Vision-based end-to-end process completed with {len(generated_tests)} test files")

        except Exception as gen_error:
            logger.error(f"Test generation failed: {str(gen_error)}")
            # Add error information to output
            output_files["test_generation_error"] = str(gen_error)

        return output_files

    except Exception as e:
        logger.error(f"Error in vision-based end-to-end process: {str(e)}", exc_info=True)
        return {"error": str(e)}

def crawl_site(config: Config, base_url: str, max_pages: int = 50, output_dir: Optional[str] = None) -> Dict[str, Dict]:
    """Crawl an entire website and generate a sitemap."""
    output_dir = output_dir or config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Starting site crawl from {base_url} with max_pages={max_pages}")

    # Create a sitemap crawler
    sitemap_crawler = SitemapCrawler(config)

    # Crawl the site
    try:
        logger.info("Initializing site crawler")
        sitemap = sitemap_crawler.crawl_site(base_url, max_pages, output_dir)
        logger.info(f"Site crawl completed with {len(sitemap)} pages discovered")
        return sitemap
    except Exception as e:
        logger.error(f"Error during site crawl: {str(e)}", exc_info=True)
        # Return empty sitemap in case of error
        return {}

def generate_site_tests(
    config: Config,
    sitemap: Dict[str, Dict],
    framework: str = 'cucumber',
    language: str = 'java',
    output_dir: Optional[str] = None,
    use_vision: bool = False,
    batch_size: int = 5  # Process pages in batches to avoid overwhelming resources
) -> Dict[str, Dict]:
    """Generate tests for an entire website based on a sitemap."""
    output_dir = output_dir or os.path.join(config.OUTPUT_DIR, "site_tests")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the LLM analyzer and test generator
    test_generator = TestGenerator(config)
    llm_analyzer = LLMAnalyzer(config)

    generated_tests = {}
    page_data_map = {}

    # Process pages in batches
    urls = list(sitemap.keys())
    for i in range(0, len(urls), batch_size):
        batch_urls = urls[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(urls)+batch_size-1)//batch_size}, pages {i+1}-{min(i+batch_size, len(urls))}")

        # Load page data for batch
        for url in batch_urls:
            try:
                file_path = sitemap[url]["file_path"]
                with open(file_path, 'r') as f:
                    page_data = json.load(f)

                # If we have pre-generated analysis, use it
                if "analysis_path" in sitemap[url] and os.path.exists(sitemap[url]["analysis_path"]):
                    try:
                        with open(sitemap[url]["analysis_path"], 'r') as f:
                            analysis_data = json.load(f)

                        # Merge analysis data with page data
                        page_data["analysis"] = analysis_data
                        logger.info(f"Using pre-generated analysis for {url}")
                    except Exception as e:
                        logger.warning(f"Could not load analysis for {url}: {str(e)}")

                page_data_map[url] = page_data
            except Exception as e:
                logger.error(f"Error loading page data for {url}: {str(e)}")

        # Generate tests for batch
        batch_test_dir = os.path.join(output_dir, f"batch_{i//batch_size + 1}")
        batch_tests = test_generator.generate_tests(
            discovered_pages_data=page_data_map,
            output_dir=batch_test_dir,
            framework=framework,
            language=language,
            use_vision=use_vision
        )

        generated_tests.update(batch_tests)

        # Clear batch data to free memory
        page_data_map.clear()

    # Generate a main test suite that includes all batches
    main_suite_path = os.path.join(output_dir, "MainTestSuite.java")
    with open(main_suite_path, 'w') as f:
        f.write(f"""import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({{
    {", ".join([f"Batch{i+1}TestSuite.class" for i in range((len(urls)+batch_size-1)//batch_size)])}
}})
public class MainTestSuite {{
    // This class will run all batch test suites
}}
""")

    # Create a summary report
    summary_path = os.path.join(output_dir, "test_summary.md")
    with open(summary_path, 'w') as f:
        f.write(f"# Site-Wide Test Summary\n\n")
        f.write(f"Base URL: {list(sitemap.keys())[0]}\n\n")
        f.write(f"Total Pages Tested: {len(sitemap)}\n\n")
        f.write(f"## Pages and Tests\n\n")

        for url, data in sitemap.items():
            f.write(f"### {data.get('title', url)}\n")
            f.write(f"- URL: {url}\n")
            if url in generated_tests:
                test_count = len(generated_tests[url].get("scenarios", []))
                f.write(f"- Tests: {test_count}\n")
            f.write("\n")

    return generated_tests

def site_e2e_process(
    config: Config,
    base_url: str,
    max_pages: int = 50,
    framework: str = 'cucumber',
    language: str = 'java',
    output_prefix: Optional[str] = None,
    use_vision: bool = False
) -> Dict[str, Dict]:
    """Run the end-to-end process for an entire site."""
    # Set up the output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    site_domain = urllib.parse.urlparse(base_url).netloc
    output_dir_name = output_prefix or f"site_e2e_{site_domain}_{timestamp}"
    output_dir = os.path.join(config.OUTPUT_DIR, output_dir_name)

    # Create screenshots directory within site folder
    screenshots_dir = os.path.join(output_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    logger.info(f"Starting site-wide E2E process for {base_url}")
    logger.info(f"Output will be saved to {output_dir}")

    # Step 1: Crawl the site
    logger.info("Step 1: Crawling site to discover pages...")
    sitemap = crawl_site(config, base_url, max_pages, output_dir)

    if not sitemap:
        logger.error("Site crawl failed or returned empty sitemap. Exiting process.")
        return {}

    logger.info(f"Site crawl completed. Found {len(sitemap)} pages.")

    # Create analysis directory
    analysis_dir = os.path.join(output_dir, "analysis")
    os.makedirs(analysis_dir, exist_ok=True)

    # Step 2: If use_vision is enabled, capture screenshots for all pages
    if use_vision:
        logger.info("Step 2: Vision mode enabled - capturing screenshots for all pages")

        # Create WebDriver once and reuse
        crawler = WebCrawler(config)
        analyzer = LLMAnalyzer(config)
        try:
            # Process pages in batches to avoid memory issues
            urls = list(sitemap.keys())
            batch_size = 3  # Process pages in small batches

            for i in range(0, len(urls), batch_size):
                batch_urls = urls[i:i+batch_size]
                logger.info(f"Processing batch {i//batch_size + 1}/{(len(urls)+batch_size-1)//batch_size}, pages {i+1}-{min(i+batch_size, len(urls))}")

                for url in batch_urls:
                    try:
                        logger.info(f"Processing {url} with vision analysis")

                        # Check if we already have page data
                        page_data = None
                        if "file_path" in sitemap[url] and os.path.exists(sitemap[url]["file_path"]):
                            with open(sitemap[url]["file_path"], 'r') as f:
                                page_data = json.load(f)
                            logger.info(f"Loaded existing page data from {sitemap[url]['file_path']}")

                        # If we don't have page data or it needs screenshots, extract it
                        if not page_data or "screenshot_path" not in page_data or not os.path.exists(page_data.get("screenshot_path", "")):
                            logger.info(f"Capturing screenshot for {url}")
                            # Pass the site-specific output_dir to ensure screenshots are saved in the site folder
                            page_data = crawler.extract_page_data(url, with_screenshots=True, output_dir=output_dir)

                            if not page_data:
                                logger.error(f"Failed to extract page data for {url}")
                                continue

                            # Save page data to file if it doesn't exist
                            if "file_path" not in sitemap[url] or not os.path.exists(sitemap[url]["file_path"]):
                                safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                                page_data_file = os.path.join(output_dir, "page_data", f"{safe_filename}.json")
                                os.makedirs(os.path.dirname(page_data_file), exist_ok=True)

                                with open(page_data_file, 'w') as f:
                                    json.dump(page_data, f, indent=2)

                                sitemap[url]["file_path"] = page_data_file
                                logger.info(f"Saved page data to {page_data_file}")

                            # Update existing page data file with screenshot information
                            elif "file_path" in sitemap[url] and os.path.exists(sitemap[url]["file_path"]):
                                with open(sitemap[url]["file_path"], 'r') as f:
                                    existing_data = json.load(f)

                                # Add screenshot path to existing data
                                if "screenshot_path" in page_data:
                                    existing_data["screenshot_path"] = page_data["screenshot_path"]

                                    # Save updated page data
                                    with open(sitemap[url]["file_path"], 'w') as f:
                                        json.dump(existing_data, f, indent=2)

                                    # Use the updated data
                                    page_data = existing_data
                                    logger.info(f"Screenshot path added to page data: {page_data['screenshot_path']}")

                        # Generate and save analysis with vision
                        if page_data and "screenshot_path" in page_data and os.path.exists(page_data["screenshot_path"]):
                            logger.info(f"Generating vision analysis for {url} with screenshot: {page_data['screenshot_path']}")

                            try:
                                # Generate analysis with timeout protection
                                import threading
                                analysis_result = [None]
                                analysis_error = [None]

                                def analyze_with_timeout():
                                    try:
                                        analysis_result[0] = analyzer.analyze_page_with_vision(page_data)
                                    except Exception as e:
                                        analysis_error[0] = str(e)

                                analysis_thread = threading.Thread(target=analyze_with_timeout)
                                analysis_thread.daemon = True
                                analysis_thread.start()
                                analysis_thread.join(timeout=300)  # 5-minute timeout

                                if analysis_thread.is_alive():
                                    logger.error(f"Vision analysis timed out for {url}")
                                    analysis = None
                                elif analysis_error[0]:
                                    logger.error(f"Vision analysis failed: {analysis_error[0]}")
                                    analysis = None
                                else:
                                    analysis = analysis_result[0]

                                if not analysis:
                                    logger.warning(f"Vision analysis failed, falling back to standard analysis for {url}")
                                    analysis = analyzer.analyze_page(page_data)

                                # Save analysis to file
                                safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                                analysis_filename = f"{safe_filename}_vision_analysis.json"
                                analysis_path = os.path.join(analysis_dir, analysis_filename)

                                with open(analysis_path, 'w') as f:
                                    json.dump(analysis, f, indent=2)

                                logger.info(f"Saved vision analysis to {analysis_path}")

                                # Add analysis path to sitemap
                                sitemap[url]["analysis_path"] = analysis_path
                            except Exception as e:
                                logger.error(f"Error generating vision analysis for {url}: {str(e)}", exc_info=True)

                                # Fallback to standard analysis
                                analysis = analyzer.analyze_page(page_data)

                                # Save standard analysis
                                safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                                analysis_filename = f"{safe_filename}_analysis.json"
                                analysis_path = os.path.join(analysis_dir, analysis_filename)

                                with open(analysis_path, 'w') as f:
                                    json.dump(analysis, f, indent=2)

                                logger.info(f"Saved standard analysis to {analysis_path}")

                                # Add analysis path to sitemap
                                sitemap[url]["analysis_path"] = analysis_path
                        else:
                            logger.warning(f"No screenshot available for vision analysis of {url}")

                            # Fallback to standard analysis
                            analysis = analyzer.analyze_page(page_data)

                            # Save standard analysis
                            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                            analysis_filename = f"{safe_filename}_analysis.json"
                            analysis_path = os.path.join(analysis_dir, analysis_filename)

                            with open(analysis_path, 'w') as f:
                                json.dump(analysis, f, indent=2)

                            logger.info(f"Saved standard analysis to {analysis_path}")

                            # Add analysis path to sitemap
                            sitemap[url]["analysis_path"] = analysis_path
                    except Exception as e:
                        logger.error(f"Error processing {url} with vision: {str(e)}", exc_info=True)

                # Save current state of sitemap after each batch for recovery
                sitemap_path = os.path.join(output_dir, "sitemap.json")
                with open(sitemap_path, 'w') as f:
                    json.dump(sitemap, f, indent=2)
        finally:
            # Ensure we close the crawler
            logger.info("Closing WebDriver")
            try:
                crawler.close()
            except Exception as e:
                logger.error(f"Error closing WebDriver: {str(e)}")

    # Step 3: Generate tests for the entire site
    logger.info("Step 3: Generating tests based on site analysis")
    tests = generate_site_tests(
        config,
        sitemap,
        framework,
        language,
        os.path.join(output_dir, "test_scripts"),
        use_vision
    )

    logger.info(f"Site-wide E2E process complete. Generated tests for {len(tests)} pages.")
    logger.info(f"Results saved to {output_dir}")

    return tests

def process_sitemap_file(config, sitemap_file, base_url=None, include_patterns=None, exclude_patterns=None, output_dir=None):
    """Process a pre-generated sitemap file and prepare it for testing."""
    from core.sitemap_loader import SitemapLoader

    loader = SitemapLoader(config)

    # Load URLs from sitemap file
    urls = loader.load_sitemap_from_file(sitemap_file)

    # Filter URLs if needed
    if base_url or include_patterns or exclude_patterns:
        urls = loader.filter_urls(urls, base_url, include_patterns, exclude_patterns)

    # Prepare sitemap for testing
    prepared_sitemap = loader.prepare_sitemap_for_testing(urls, output_dir)

    return prepared_sitemap

def site_e2e_process_with_sitemap(config, sitemap_file, framework='cucumber', language='java',
                                output_prefix=None, use_vision=False):
    """Run the end-to-end process using a pre-generated sitemap."""
    # Set up the output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir_name = output_prefix or f"sitemap_e2e_{timestamp}"
    output_dir = os.path.join(config.OUTPUT_DIR, output_dir_name)
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Starting sitemap-based E2E process with {sitemap_file}")
    logger.info(f"Output will be saved to {output_dir}")

    # Process the sitemap file
    from core.sitemap_loader import SitemapLoader
    loader = SitemapLoader(config)
    urls = loader.load_sitemap_from_file(sitemap_file)

    # Create the sitemap structure
    sitemap = {}

def main():
    """Main entry point."""
    try:
        args = parse_arguments()
        config = Config()

        # Show initial command being processed
        logger.info(f"Executing command: {args.command} with arguments: {vars(args)}")

        if args.command == 'crawl':
            output_file = crawl_page(config, args.url, args.output, args.with_screenshots)
            logger.info(f"Crawl completed. Output saved to {output_file}")

        elif args.command == 'analyze':
            output_file = analyze_page_data(config, args.input, args.output)
            logger.info(f"Analysis completed. Output saved to {output_file}")

        elif args.command == 'generate':
            output_files = generate_test_scripts(config, args.input, args.framework, args.language, args.output, args.use_vision)
            if output_files.get("error"):
                logger.error("Test script generation failed.")
            else:
                logger.info("Test script generation completed successfully.")

        elif args.command == 'e2e':
            if args.sitemap_file:
                output_files = site_e2e_process_with_sitemap(
                    config,
                    args.sitemap_file,
                    args.framework,
                    args.language,
                    args.output,
                    args.use_vision
                )
            elif args.site and args.url:
                output_files = site_e2e_process(
                    config,
                    args.url,
                    args.max_pages,
                    args.framework,
                    args.language,
                    args.output,
                    args.use_vision
                )
            elif args.url:
                output_files = process_end_to_end(
                    config,
                    args.url,
                    args.framework,
                    args.output
                )
            else:
                logger.error("URL or sitemap file must be provided for end-to-end process.")
                return 1

            logger.info(f"End-to-end process completed. Output files: {output_files}")

        elif args.command == 'vision':
            output_file = analyze_page_with_vision(config, args.url, args.output, args.with_flow, args.with_screenshots)
            logger.info(f"Vision analysis completed. Output saved to {output_file}")

        elif args.command == 'vision-e2e':
            logger.info(f"Starting vision-e2e with URL: {args.url}, site mode: {args.site}, max pages: {args.max_pages}")
            # Create output directory prefix if specified
            output_prefix = args.output

            if args.sitemap_file:
                # Run vision-enhanced E2E process using a pre-generated sitemap
                site_e2e_process_with_sitemap(
                    config,
                    args.sitemap_file,
                    args.framework,
                    args.language,
                    args.output,
                    True
                )
            elif args.site and args.url:
                logger.info("Processing entire site with vision analysis")
                # Add timeout protection to prevent hanging
                import signal

                def timeout_handler(signum, frame):
                    logger.error("Timeout occurred - process took too long")
                    raise TimeoutError("Process took too long to complete")

                # Set timeout to 20 minutes (adjust as needed)
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(1200)  # 20 minutes in seconds

                try:
                    site_e2e_process(
                        config,
                        args.url,
                        args.max_pages,
                        args.framework,
                        args.language,
                        args.output,
                        True
                    )
                    # Cancel alarm if successful
                    signal.alarm(0)
                except TimeoutError:
                    logger.error("Site processing timed out - consider increasing the timeout or reducing max pages")
                    return 1
                except Exception as e:
                    logger.error(f"Error in site_e2e_process: {str(e)}", exc_info=True)
                    return 1
            elif args.url:
                output_files = vision_e2e_process(
                    config,
                    args.url,
                    args.framework,
                    output_prefix,
                    args.with_flow
                )
                logger.info(f"Vision end-to-end process completed. Output files: {output_files}")

                # Print summary of results
                print("\nVision E2E Test Generation Complete")
                print("====================================")
                print(f"URL: {args.url}")

                # Get the output directory path
                if output_prefix:
                    output_dir = os.path.join(config.OUTPUT_DIR, output_prefix)
                else:
                    url_domain = urllib.parse.urlparse(args.url).netloc
                    # Find the most recent directory
                    vision_dirs = [d for d in os.listdir(config.OUTPUT_DIR)
                                  if d.startswith(f"vision_e2e_{url_domain}") and
                                  os.path.isdir(os.path.join(config.OUTPUT_DIR, d))]
                    if vision_dirs:
                        vision_dirs.sort(reverse=True)
                        output_dir = os.path.join(config.OUTPUT_DIR, vision_dirs[0])
                    else:
                        output_dir = None

                if output_dir:
                    print(f"Output directory: {output_dir}")
                    print("\nGenerated files:")
                    print(f"  - Analysis: {len(os.listdir(os.path.join(output_dir, 'analysis')))} files")
                    print(f"  - Screenshots: {len(os.listdir(os.path.join(output_dir, 'screenshots')))} files")
                    print(f"  - Test Scripts: {os.path.join(output_dir, 'test_scripts')}")
            else:
                logger.error("URL or sitemap file must be provided for vision end-to-end process.")
                return 1

        elif args.command == 'sitemap':
            prepared_sitemap = process_sitemap_file(
                config,
                args.file,
                args.base_url,
                args.include,
                args.exclude,
                args.output
            )
            logger.info(f"Sitemap processing completed. Prepared sitemap: {prepared_sitemap}")

        else:
            logger.error(f"Unknown command: {args.command}")
            return 1

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
