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

    # Vision End-to-End command
    vision_e2e_parser = subparsers.add_parser('vision-e2e', help='End-to-end process using vision capabilities')
    vision_e2e_parser.add_argument('url', help='URL to crawl')
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

    # End-to-end command
    e2e_parser = subparsers.add_parser('e2e', help='End-to-end process: crawl, analyze, generate')
    e2e_parser.add_argument('url', help='URL to crawl')
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

        # Generate tests with the updated analysis - Fix the parameter name here
        generated_tests = test_gen.generate_tests(
            discovered_pages_data={url: analysis_data},
            output_dir=output_dir,
            framework=framework,
            language=language  # Changed from programming_language to language
        )

        logger.info(f"Generated {len(generated_tests)} test files")
        return True
    except Exception as e:
        logger.error(f"Error generating test scripts: {str(e)}", exc_info=True)
        return False

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

def analyze_page_with_vision(config: Config, url: str, output_filename: Optional[str] = None, flow_file: Optional[str] = None, force_screenshot: bool = False) -> str:
    """Analyze page with GPT-4o-mini vision capabilities.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        output_filename (Optional[str]): Output filename
        flow_file (Optional[str]): User flow description file
        force_screenshot (bool): Whether to force a new screenshot capture

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
            page_data = crawler.crawl_with_user_flow(url, flow_description)
            logger.info(f"User flow execution completed with {len(page_data.get('user_flow', []))} steps")
        else:
            # Regular crawl with screenshots enabled
            logger.info("Capturing page data with screenshots")
            page_data = crawler.extract_page_data(url, with_screenshots=True)

        # Check if page_data is valid
        if page_data is None:
            logger.error("Failed to extract page data")
            # Create minimal page data
            page_data = {
                "url": url,
                "title": "Failed to extract",
                "error": "Page data extraction failed"
            }

        # Save page data
        page_data_file = crawler.save_page_data(page_data)
        logger.info(f"Saved page data to {page_data_file}")

        # Ensure page_data has screenshot_path
        has_screenshot = isinstance(page_data, dict) and "screenshot_path" in page_data
        if not has_screenshot or not os.path.exists(page_data.get("screenshot_path", "")):
            logger.warning("No screenshot captured or invalid screenshot path. Taking screenshot now.")
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

        # Save analysis
        if output_filename:
            base_name = os.path.splitext(output_filename)[0]
            analysis_filename = f"{base_name}_vision_analysis.json"
        else:
            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            analysis_filename = f"{safe_filename}_vision_analysis.json"

        analysis_path = os.path.join(config.analysis_path, analysis_filename)
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
    """Process end-to-end with vision capabilities.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        framework (str): Test framework to use
        output_prefix (Optional[str]): Output file prefix
        flow_file (Optional[str]): User flow description file

    Returns:
        Dict[str, str]: Dictionary of output files
    """
    output_files = {}
    try:
        # Step 1: Analyze with vision capabilities
        logger.info(f"Starting vision-based end-to-end process for {url}")
        try:
            analysis_file = analyze_page_with_vision(config, url, output_prefix, flow_file)
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
            output_dir = os.path.join(config.test_scripts_path, "vision_tests")
            if output_prefix:
                output_dir = os.path.join(output_dir, output_prefix)

            os.makedirs(output_dir, exist_ok=True)

            logger.info(f"Generating test scripts with vision-enhanced analysis in {output_dir}")
            generated_tests = test_gen.generate_tests(
                discovered_pages_data={url: analysis_data},
                output_dir=output_dir,
                framework=framework
            )

            # Add test files to output
            for test_url, script in generated_tests.items():
                safe_url = test_gen._safe_filename(test_url)
                test_file = os.path.join(output_dir, f"{safe_url}_spec.feature")
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

    # Create a sitemap crawler
    sitemap_crawler = SitemapCrawler(config)

    # Crawl the site
    sitemap = sitemap_crawler.crawl_site(base_url, max_pages, output_dir)

    return sitemap

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
    # Don't pass llm_analyzer to TestGenerator - it will create its own instance
    test_generator = TestGenerator(config)

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

    logger.info(f"Starting site-wide E2E process for {base_url}")
    logger.info(f"Output will be saved to {output_dir}")

    # Step 1: Crawl the site
    sitemap = crawl_site(config, base_url, max_pages, output_dir)

    # Step 2: Generate tests for the entire site
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

def main():
    """Main entry point."""
    try:
        args = parse_arguments()
        config = Config()

        if args.command == 'crawl':
            logger.info(f"Crawl command with screenshots flag: {args.with_screenshots}")
            output_path = crawl_page(config, args.url, args.output, with_screenshots=args.with_screenshots)
            logger.info(f"Crawl completed: {output_path}")

        elif args.command == 'analyze':
            if args.use_vision:
                logger.info("Running analysis with vision capabilities")
                # For vision analysis with existing page data, we need to ensure the screenshot exists
                with open(args.input, 'r', encoding='utf-8') as f:
                    page_data = json.load(f)
                if "screenshot_path" not in page_data or not os.path.exists(page_data.get("screenshot_path", "")):
                    logger.warning("Page data doesn't contain a valid screenshot path. Vision analysis may be limited.")

                # Create an analyzer and use vision capabilities
                analyzer = LLMAnalyzer(config)
                analysis = analyzer.analyze_page_with_vision(page_data)

                # Save the analysis
                if args.output:
                    output_filename = args.output
                else:
                    base_name = os.path.splitext(os.path.basename(args.input))[0]
                    output_filename = f"{base_name}_vision_analysis.json"

                output_path = os.path.join(config.analysis_path, output_filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(analysis, indent=2, fp=f)

                logger.info(f"Vision analysis saved to {output_path}")
            else:
                analyze_page_data(config, args.input, args.output)

            if args.verbose and os.path.exists(os.path.join(config.analysis_path, args.output or "")):
                # Display a summary of the analysis
                analysis_path = os.path.join(config.analysis_path, args.output)
                with open(analysis_path, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)

                logger.info("=== Analysis Summary ===")
                logger.info(f"URL: {analysis.get('url')}")
                logger.info(f"Title: {analysis.get('title')}")
                logger.info(f"Key Elements: {len(analysis.get('key_elements', []))}")
                logger.info(f"Test Steps: {len(analysis.get('smoke_test_steps', []))}")
                if analysis.get('smoke_test_steps'):
                    for i, step in enumerate(analysis.get('smoke_test_steps', []), 1):
                        logger.info(f"  Step {i}: {step}")

        elif args.command == 'generate':
            language = getattr(args, 'language', 'java')
            success = generate_test_scripts(
                config,
                args.input,
                framework=args.framework,
                language=args.language,
                output_dir=args.output,
                use_vision=args.use_vision  # Pass the use_vision flag here
            )
            if not success:
                sys.exit(1)
            logger.info(f"Generated {args.framework} test scripts in {language}")

        elif args.command == 'e2e' and args.site:
            site_e2e_process(
                config,
                args.url,
                args.max_pages,
                args.framework,
                args.language,
                args.output,
                False
            )

        elif args.command == 'vision-e2e' and args.site:
            site_e2e_process(
                config,
                args.url,
                args.max_pages,
                args.framework,
                args.language,
                args.output,
                True
            )

        elif args.command == 'e2e':
            # Pass screenshots option from e2e to crawl
            output_files = process_end_to_end(
                config,
                args.url,
                args.framework,
                args.output
            )
            logger.info("End-to-end process completed successfully")
            logger.info("Output files:")
            for file_type, file_path in output_files.items():
                logger.info(f"  {file_type}: {file_path}")

        elif args.command == 'vision':
            # Pass force_screenshot option to allow forcing new screenshots
            output_file = analyze_page_with_vision(
                config,
                args.url,
                args.output,
                args.with_flow,
                force_screenshot=getattr(args, 'with_screenshots', False)
            )
            logger.info(f"Vision analysis completed: {output_file}")

        elif args.command == 'vision-e2e':
            language = getattr(args, 'language', 'java')
            output_files = vision_e2e_process(
                config,
                args.url,
                args.framework,
                args.output,
                args.with_flow
            )
            logger.info(f"Vision-based end-to-end process completed successfully using {language}")
            logger.info("Output files:")
            for file_type, file_path in output_files.items():
                logger.info(f"  {file_type}: {file_path}")

        else:
            logger.error("No command specified")
            return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())
