# LLM Smoke Test Framework

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

An automated framework that uses LLMs to generate smoke tests for web applications. The framework crawls webpages, extracts essential elements, analyzes them using an LLM, and generates comprehensive test scripts.

## Table of Contents

- [LLM Smoke Test Framework](#llm-smoke-test-framework)
  - [Table of Contents](#table-of-contents)
  - [✨ Features](#-features)
  - [🚀 Quick Setup](#-quick-setup)
  - [🗂️ Project Structure](#️-project-structure)
  - [🔧 Implementation Details](#-implementation-details)
    - [Core - LLM Analyzer](#core---llm-analyzer)
    - [Core - Web Crawler](#core---web-crawler)
    - [Core - Test Generator](#core---test-generator)
  - [⚙️ Usage](#️-usage)
    - [End-to-End Process](#end-to-end-process)
    - [Vision-Enhanced Testing](#vision-enhanced-testing)
    - [Individual Steps](#individual-steps)
  - [📤 Output](#-output)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## ✨ Features

- **Automated Test Generation:** Leverages LLMs to create robust smoke tests
- **Web Crawling:** Discovers and extracts key elements from web pages
- **Vision Capabilities:** Uses GPT-4o-mini's vision capabilities for enhanced UI analysis
- **Error Handling and Robustness:** Improved error handling and fallback mechanisms for increased reliability
- **Configurable:** Easily adaptable to different testing frameworks and environments
- **Modular Design:** Supports individual step execution for customized workflows

## 🚀 Quick Setup

1. **Clone the repository:**

```bash
git clone https://github.com/Friend09/llm-smoke-test-framework
cd llm-smoke-test-framework
```

2. **Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

```bash
touch .env
```

Example `.env` configuration:

```ini
# Crawler settings
HEADLESS=True
PAGE_LOAD_TIMEOUT=30

# Output settings
OUTPUT_DIR=output

# LLM settings
OPENAI_API_KEY=<YOUR API KEY>
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=2000
```

## 🗂️ Project Structure

```
llm-smoke-test-framework/
├── config/             # Configuration management
├── core/              # Core functionality
├── output/            # Generated outputs
├── tests/             # Tests
├── requirements.txt   # Project dependencies
└── run.py            # Main entry point
```

## 🔧 Implementation Details

### Core - LLM Analyzer

- `analyze_page`: Processes crawler data through LLM
- `analyze_page_with_vision`: Uses GPT-4o-mini's vision capabilities for enhanced analysis
- `generate_test_script`: Creates test scripts from analysis
- `_generate_combined_test_steps`: Combines test steps from visual and DOM analysis

### Core - Web Crawler

- `extract_page_data`: Extracts page elements and structure
- `save_page_data`: Stores extracted data in JSON format

### Core - Test Generator

- `generate_tests`: Generate test scripts for discovered pages
- `generate_login_tests`: Generate login-specific test cases
- `_generate_test_suite`: Generate a test suite file that includes all tests.

## ⚙️ Usage

### End-to-End Process

```bash
python run.py e2e https://example.com
```

### Vision-Enhanced Testing

The framework now supports vision-enhanced testing using GPT-4o-mini's vision capabilities:

```bash
# Run end-to-end process with vision capabilities
python run.py vision-e2e https://example.com

# Analyze a specific page with vision capabilities
python run.py vision https://example.com
```

Vision-enhanced testing provides several benefits:
- Better understanding of page layout and visual elements
- Improved element locator strategies based on visual context
- More comprehensive test scenarios that consider visual relationships
- Enhanced ability to test complex UI components

### Individual Steps

```bash
python run.py crawl https://example.com
python run.py analyze output/page_data/example_com_home.json
python run.py generate output/analysis/example_com_home_analysis.json
```

## 📤 Output

1. **Page Data (JSON)**

   - Interactive elements
   - Forms
   - Frames
   - Headings

2. **Page Analysis**

   - Element identifiers
   - Test priorities
   - Locator strategies
   - Test steps

3. **Test Scripts**
   - Cucumber features
   - Step definitions
   - Page objects

4. **Error Handling**
   - Detailed logs and fallback mechanisms for robust testing

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

## 📜 License

[MIT License](LICENSE)
