import os
import json
from core.llm_analyzer import LLMAnalyzer
from core.test_generator import TestGenerator
from config.config import Config

# generate doc string for this file



def main():
    # Load configuration
    config = Config()

    # Initialize LLMAnalyzer and TestGenerator
    llm_analyzer = LLMAnalyzer(config)
    test_generator = TestGenerator(config)

    # Directory containing the discovered pages
    discovered_pages_dir = os.path.join(config.OUTPUT_DIR, "discovered_pages")

    # Load page data
    page_data = {}
    for filename in os.listdir(discovered_pages_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(discovered_pages_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                html_content = f.read()
                # Simulate page data structure
                page_data[filename] = {
                    "url": f"https://example.com/{filename}",
                    "title": "Sample Page",
                    "html_content": html_content,
                }

    # Analyze each page and generate tests
    for url, data in page_data.items():
        analysis_results = llm_analyzer.analyze_page(data)
        test_generator.generate_tests(analysis_results)

if __name__ == "__main__":
    main()
