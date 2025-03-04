# run.py
import argparse
import json
import logging
import os
import sys
from typing import List, Dict, Any, Optional

from config.config import Config
from core.crawler import WebCrawler
from core.llm_analyzer import LLMAnalyzer

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

    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl a webpage and extract data')
    crawl_parser.add_argument('url', help='URL to crawl')
    crawl_parser.add_argument('-o', '--output', help='Output filename')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze page data')
    analyze_parser.add_argument('input', help='Input page data JSON file')
    analyze_parser.add_argument('-o', '--output', help='Output filename')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate test scripts')
    generate_parser.add_argument('input', help='Input analysis JSON file')
    generate_parser.add_argument('-f', '--framework', default='cucumber',
                                help='Test framework (default: cucumber)')
    generate_parser.add_argument('-o', '--output', help='Output directory')

    # End-to-end command
    e2e_parser = subparsers.add_parser('e2e', help='End-to-end process: crawl, analyze, generate')
    e2e_parser.add_argument('url', help='URL to crawl')
    e2e_parser.add_argument('-f', '--framework', default='cucumber',
                           help='Test framework (default: cucumber)')
    e2e_parser.add_argument('-o', '--output', help='Output directory prefix')

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

        else:
            logger.error("No command specified")
            return 1

        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
