# run.py
import argparse
import json
import logging
import os
import sys
import time  # Add missing import
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.config import Config
from core.crawler import WebCrawler
from core.llm_analyzer import LLMAnalyzer
from core.test_generator import TestGenerator

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
    vision_parser.add_argument('-o', '--output', help='Output directory')
    vision_parser.add_argument('--with-flow', help='User flow description file')

    # Vision End-to-End command
    vision_e2e_parser = subparsers.add_parser('vision-e2e', help='End-to-end process using vision capabilities')
    vision_e2e_parser.add_argument('url', help='URL to crawl')
    vision_e2e_parser.add_argument('-f', '--framework', default='cucumber',
                                  help='Test framework (default: cucumber)')
    vision_e2e_parser.add_argument('-o', '--output', help='Output directory prefix')
    vision_e2e_parser.add_argument('--with-flow', help='User flow description file')

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

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate test scripts')
    generate_parser.add_argument('input', help='Input analysis JSON file')
    generate_parser.add_argument('-f', '--framework', default='cucumber',
                                help='Test framework (default: cucumber)')
    generate_parser.add_argument('-o', '--output', help='Output directory')
    generate_parser.add_argument('--use-vision', action='store_true', help='Use vision-based generation')

    # End-to-end command
    e2e_parser = subparsers.add_parser('e2e', help='End-to-end process: crawl, analyze, generate')
    e2e_parser.add_argument('url', help='URL to crawl')
    e2e_parser.add_argument('-f', '--framework', default='cucumber',
                           help='Test framework (default: cucumber)')
    e2e_parser.add_argument('-o', '--output', help='Output directory prefix')
    e2e_parser.add_argument('--use-vision', action='store_true', help='Use vision capabilities')

    return parser.parse_args()

def crawl_page(config: Config, url: str, output_filename: Optional[str] = None) -> str:
    """Crawl a webpage and extract data.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        output_filename (Optional[str]): Output filename

    Returns:
        str: Path to the saved page data file
    """
    crawler = WebCrawler(config)
    try:
        page_data = crawler.extract_page_data(url)
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

def generate_test_scripts(
    config: Config,
    input_file: str,
    framework: str = 'cucumber',
    output_dir: Optional[str] = None
) -> Dict[str, str]:
    """Generate test scripts.

    Args:
        config (Config): Configuration object
        input_file (str): Input analysis JSON file
        framework (str): Test framework
        output_dir (Optional[str]): Output directory

    Returns:
        Dict[str, str]: Mapping of file types to their paths
    """
    # Load analysis
    with open(input_file, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    # Generate test scripts
    analyzer = LLMAnalyzer(config)
    test_scripts = analyzer.generate_test_script(analysis, framework)

    # Determine output directory
    if output_dir is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = os.path.join(config.test_scripts_path, base_name)
    else:
        output_dir = os.path.join(config.test_scripts_path, output_dir)

    os.makedirs(output_dir, exist_ok=True)

    # Save test scripts
    output_files = {}

    # Save summary JSON
    summary_path = os.path.join(output_dir, "test_scripts.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(test_scripts, indent=2, fp=f)

    output_files["summary"] = summary_path

    # Save individual files
    if "feature_file" in test_scripts:
        feature_path = os.path.join(output_dir, "test.feature")
        with open(feature_path, 'w', encoding='utf-8') as f:
            f.write(test_scripts["feature_file"])
        output_files["feature"] = feature_path

    if "step_definitions" in test_scripts:
        steps_path = os.path.join(output_dir, "StepDefinitions.java")
        with open(steps_path, 'w', encoding='utf-8') as f:
            f.write(test_scripts["step_definitions"])
        output_files["steps"] = steps_path

    if "page_object" in test_scripts:
        page_path = os.path.join(output_dir, "PageObject.java")
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(test_scripts["page_object"])
        output_files["page_object"] = page_path

    logger.info(f"Generated test scripts in {output_dir}")
    return output_files

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

def analyze_page_with_vision(config: Config, url: str, output_filename: Optional[str] = None, flow_file: Optional[str] = None) -> str:
    """Analyze page with GPT-4o-mini vision capabilities.

    Args:
        config (Config): Configuration object
        url (str): URL to crawl
        output_filename (Optional[str]): Output filename
        flow_file (Optional[str]): User flow description file

    Returns:
        str: Path to the saved analysis file
    """
    logger.info(f"Starting vision analysis for {url}")
    crawler = WebCrawler(config)
    try:
        # If flow file is provided, use crawl with user flow
        if flow_file:
            with open(flow_file, 'r') as f:
                flow_description = f.read()
            logger.info(f"Using user flow from {flow_file}")
            page_data = crawler.crawl_with_user_flow(url, flow_description)
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

def main():
    """Main entry point."""
    try:
        args = parse_arguments()
        config = Config()

        if args.command == 'crawl':
            crawl_page(config, args.url, args.output)

        elif args.command == 'analyze':
            analyze_page_data(config, args.input, args.output)

        elif args.command == 'generate':
            generate_test_scripts(config, args.input, args.framework, args.output)

        elif args.command == 'e2e':
            output_files = process_end_to_end(config, args.url, args.framework, args.output)
            logger.info("End-to-end process completed successfully")
            logger.info("Output files:")
            for file_type, file_path in output_files.items():
                logger.info(f"  {file_type}: {file_path}")

        elif args.command == 'vision':
            output_file = analyze_page_with_vision(
                config,
                args.url,
                args.output,
                args.with_flow
            )
            logger.info(f"Vision analysis completed: {output_file}")

        elif args.command == 'vision-e2e':
            output_files = vision_e2e_process(
                config,
                args.url,
                args.framework,
                args.output,
                args.with_flow
            )
            logger.info("Vision-based end-to-end process completed successfully")
            logger.info("Output files:")
            for file_type, file_path in output_files.items():
                logger.info(f"  {file_type}: {file_path}")

        else:
            logger.error("No command specified")
            return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
