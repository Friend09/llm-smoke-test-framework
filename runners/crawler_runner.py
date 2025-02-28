#!/usr/bin/env python
# runners/crawler_runner.py

"""Main runner for the test generator"""

import os
import sys
import logging
import argparse
from datetime import datetime
from utils.session_manager import SessionManager
from utils.exceptions import TestGeneratorError
from utils.performance import measure_performance

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import Config
from core.crawler import WebCrawler
from core.test_generator import TestGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("smoke_test_generator.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="LLM-Enhanced Smoke Test Generator")

    parser.add_argument("--url", type=str, help="Starting URL to crawl")
    parser.add_argument("--depth", type=int, default=3, help="Maximum depth to crawl")
    parser.add_argument("--auth", type=str, choices=["basic", "ntlm", "okta"], help="Authentication type")
    parser.add_argument("--output", type=str, help="Output directory")
    parser.add_argument("--framework", type=str, default="cucumber", choices=["cucumber"], help="Test framework")
    parser.add_argument("--language", type=str, default="java", choices=["java", "typescript"], help="Programming language")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--skip-crawl", action="store_true", help="Skip crawling and use existing page data")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--visible", action="store_true", help="Run browser in visible mode for debugging")
    parser.add_argument("--username", type=str, help="Override username for authentication")
    parser.add_argument("--password", type=str, help="Override password for authentication")

    return parser.parse_args()


@measure_performance
def main():
    """Main function to run the crawler and test generator."""
    start_time = datetime.now()

    # Parse command line arguments
    args = parse_args()

    try:
        # Load configuration
        config = Config()
        session_manager = SessionManager(config)

        # Override config with command line arguments
        if args.url:
            config.BASE_URL = args.url
        if args.depth:
            config.MAX_DEPTH = args.depth
        if args.auth:
            config.AUTH_TYPE = args.auth
        if args.output:
            config.OUTPUT_DIR = args.output
        if args.headless:
            config.HEADLESS = True
        if args.debug:
            config.DEBUG_MODE = True
        if args.visible:
            config.HEADLESS = False
        if args.username:
            config.USERNAME = args.username
            config.AUTH_CONFIG["username"] = args.username
        if args.password:
            config.PASSWORD = args.password
            config.AUTH_CONFIG["password"] = args.password

        # Create output directory
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)

        try:
            driver = session_manager.create_session()

            # Step 1: Crawl the application (if not skipped)
            if not args.skip_crawl:
                logger.info(f"Starting web crawler at {config.BASE_URL}")

                # Add debug information about the configuration
                logger.info(f"Configuration - AUTH_TYPE: {config.AUTH_TYPE}, USERNAME: {config.USERNAME}")
                logger.info(f"Configuration - HEADLESS: {config.HEADLESS}, MAX_DEPTH: {config.MAX_DEPTH}")

                if config.AUTH_TYPE != "none":
                    logger.info(f"Using authentication type: {config.AUTH_TYPE}")
                    # Don't log sensitive information in production
                    if config.DEBUG_MODE:
                        logger.debug(f"Auth config: {config.AUTH_CONFIG}")

                crawler = WebCrawler(config.BASE_URL, config)

                try:
                    # Take a screenshot before authentication (if not headless)
                    if not config.HEADLESS:
                        os.makedirs(os.path.join(config.OUTPUT_DIR, "screenshots"), exist_ok=True)
                        crawler.driver.save_screenshot(os.path.join(config.OUTPUT_DIR, "screenshots", "before_auth.png"))
                        logger.info("Saved screenshot before authentication")

                    page_data = crawler.start_crawling(config.MAX_DEPTH, config.AUTH_TYPE)

                    if not page_data:
                        logger.error("Crawler did not find any pages. Check the URL and authentication settings.")
                        # Take a screenshot after failed crawl (if not headless)
                        if not config.HEADLESS and crawler.driver:
                            crawler.driver.save_screenshot(os.path.join(config.OUTPUT_DIR, "screenshots", "failed_crawl.png"))
                            logger.info("Saved screenshot after failed crawl")
                        return 1

                    logger.info(f"Crawler discovered {len(page_data)} pages")
                except Exception as e:
                    logger.error(f"Crawler failed with error: {str(e)}", exc_info=True)
                    # Take a screenshot on exception (if not headless)
                    if not config.HEADLESS and crawler.driver:
                        os.makedirs(os.path.join(config.OUTPUT_DIR, "screenshots"), exist_ok=True)
                        crawler.driver.save_screenshot(os.path.join(config.OUTPUT_DIR, "screenshots", "crawler_exception.png"))
                        logger.info("Saved screenshot after exception")
                    return 1
            else:
                logger.info("Skipping crawl phase, using existing page data")

            # Step 2: Generate tests
            logger.info("Starting test generation")
            test_generator = TestGenerator(config)
            generated_tests = test_generator.generate_tests(
                output_dir=os.path.join(config.OUTPUT_DIR, "test_scripts"),
                framework=args.framework,
                language=args.language,
            )

            logger.info(f"Generated tests for {len(generated_tests)} pages")

            # Calculate execution time
            end_time = datetime.now()
            duration = end_time - start_time

            logger.info(f"Complete! Total execution time: {duration}")
            logger.info(f"Output directory: {os.path.abspath(config.OUTPUT_DIR)}")

            return 0

        finally:
            session_manager.close_session()

    except TestGeneratorError as e:
        logger.error(f"Test generator error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
