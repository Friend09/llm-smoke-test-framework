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
import asyncio

from config.config import Config
from core.crawler import PlaywrightCrawler
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

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
TESTS_DIR = os.path.join(OUTPUT_DIR, "tests")
os.makedirs(TESTS_DIR, exist_ok=True)

async def main():
    parser = argparse.ArgumentParser(description="LLM Smoke Test Framework (Playwright Edition)")
    parser.add_argument("vision-e2e", help="Run end-to-end vision-based smoke test generation", nargs=1)
    parser.add_argument("website_url", help="Website URL to crawl and test")
    parser.add_argument("--page-only", action="store_true", help="Only generate a test for the initial page (no crawling)")
    parser.add_argument("--site", action="store_true", help="Crawl and generate tests for the entire site (default)")
    parser.add_argument("--max-pages", type=int, default=None, help="Maximum number of pages to crawl and generate tests for")
    args = parser.parse_args()

    website_url = args.website_url
    logger.info(f"Starting crawl for: {website_url}")

    llm_analyzer = LLMAnalyzer(Config())

    if args.page_only:
        # Only process the initial page
        logger.info("Generating test for the initial page only (--page-only mode)...")
        # Simulate a single-page crawl result
        crawler = PlaywrightCrawler(website_url, max_pages=1)
        page_data_dict = await crawler.crawl(single_page_only=True)
    else:
        # Site-wide crawl (default)
        max_pages = args.max_pages if args.max_pages else 100
        crawler = PlaywrightCrawler(website_url, max_pages=max_pages)
        page_data_dict = await crawler.crawl()

    for url, page_data in page_data_dict.items():
        screenshot_path = page_data.get("screenshot_path")
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")

        # 1. Perform analysis (vision-based if screenshot is available)
        if screenshot_path and os.path.exists(screenshot_path):
            logger.info(f"Performing vision-based analysis for {url} using screenshot: {screenshot_path}")
            page_analysis = llm_analyzer.analyze_page_with_vision(page_data)
        else:
            logger.info(f"Performing standard analysis for {url} (no screenshot available)")
            page_analysis = llm_analyzer.analyze_page(page_data)

        # 2. Generate test script from analysis (force Selenium/Java)
        logger.info(f"Generating test script for {url}...")
        test_script_info = llm_analyzer.generate_test_script(page_analysis, framework="selenium", language="java")
        logger.info(f"LLM test_script_info: {test_script_info}")
        logger.info(f"Raw LLM output:\n{test_script_info.get('feature_file', '')}")

        # 3. Save feature file
        test_file = os.path.join(TESTS_DIR, f"{safe_name}_smoketest.feature")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_script_info.get("feature_file", ""))
        logger.info(f"Saved smoke test for {url} to {test_file}")

        # 4. Save step definitions (Java example)
        if "step_definitions" in test_script_info:
            steps_file = os.path.join(TESTS_DIR, f"{safe_name}_steps.java")
            with open(steps_file, "w", encoding="utf-8") as f:
                f.write(test_script_info["step_definitions"])
            logger.info(f"Saved step definitions for {url} to {steps_file}")

        # 5. Save page object (Java example)
        if "page_object" in test_script_info:
            page_file = os.path.join(TESTS_DIR, f"{safe_name}_page.java")
            with open(page_file, "w", encoding="utf-8") as f:
                f.write(test_script_info["page_object"])
            logger.info(f"Saved page object for {url} to {page_file}")
    logger.info("All done!")

if __name__ == "__main__":
    asyncio.run(main())
