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
    - [Core - Sitemap Loader](#core---sitemap-loader)
  - [⚙️ Usage](#️-usage)
    - [Command Reference](#command-reference)
    - [Basic Commands](#basic-commands)
      - [Crawling a Webpage](#crawling-a-webpage)
    - [Analyzing Page Data](#analyzing-page-data)
    - [Generating Test Scripts](#generating-test-scripts)
    - [Advanced Features](#advanced-features)
      - [End-to-End Process](#end-to-end-process)
      - [Vision-Enhanced Analysis](#vision-enhanced-analysis)
      - [Vision-Based End-to-End Testing](#vision-based-end-to-end-testing)
      - [Generating Tests from Vision Analysis](#generating-tests-from-vision-analysis)
      - [User Flow Testing](#user-flow-testing)
      - [Site-Wide Testing](#site-wide-testing)
      - [Using External Sitemaps](#using-external-sitemaps)
    - [Working with Test Generator](#working-with-test-generator)
  - [📤 Output](#-output)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## ✨ Features

- **Automated Test Generation:** Leverages LLMs to create robust smoke tests
- **Web Crawling:** Discovers and extracts key elements from web pages
- **Vision Capabilities:** Uses GPT-4o-mini's vision capabilities for enhanced UI analysis
- **Screenshot Optimization:** Automatically resizes and compresses screenshots for efficient API usage
- **Error Handling and Robustness:** Improved error handling and fallback mechanisms for increased reliability
- **Configurable:** Easily adaptable to different testing frameworks and environments
- **Modular Design:** Supports individual step execution for customized workflows
- **External Sitemap Support:** Integrates with separately generated sitemaps for efficient testing

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

# Screenshot settings
SCREENSHOT_MAX_DIMENSION=1280
SCREENSHOT_QUALITY=75
```

## 🗂️ Project Structure

```
llm-smoke-test-framework/
├── config/             # Configuration management
├── core/              # Core functionality
├── flows/             # Directory for user flow definitions
│   ├── login_flow.txt # Example user flow file
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
- `crawl_with_user_flow`: Simulates user interactions based on predefined flows

### Core - Test Generator

- `generate_tests`: Generate test scripts for discovered pages
- `generate_login_tests`: Generate login-specific test cases
- `_generate_test_suite`: Generate a test suite file that includes all tests.

### Core - Sitemap Loader

- `load_sitemap`: Loads pre-generated sitemaps from an external repository
- `parse_sitemap`: Parses sitemap data to extract URLs for testing

## ⚙️ Usage

### Command Reference

| Command                  | Description                                                                   |
| ------------------------ | ----------------------------------------------------------------------------- |
| `crawl`                  | Extracts elements, forms, and other data from a webpage.                      |
| `analyze`                | Processes the extracted page data using the LLM to generate analysis results. |
| `generate`               | Creates test scripts based on the analysis results.                           |
| `e2e`                    | Runs the end-to-end process for a given URL.                                  |
| `vision`                 | Analyzes a specific page with vision capabilities.                            |
| `vision-e2e`             | Runs the end-to-end process with vision capabilities.                         |
| `vision --with-flow`     | Runs with a predefined user flow.                                             |
| `vision-e2e --with-flow` | Runs end-to-end process with user flow.                                       |
| `e2e --site`             | Runs end-to-end process for an entire website.                                |
| `vision-e2e --site`      | Runs vision-enhanced end-to-end process for an entire website.                |
| `sitemap`                | Loads and processes a pre-generated sitemap for testing.                      |

### Basic Commands

The framework provides several individual commands that can be run separately or combined as needed.

#### Crawling a Webpage

The `crawl` command extracts elements, forms, and other data from a webpage.

```bash
# Basic usage
python run.py crawl https://example.com

# Save to specific filename
python run.py crawl https://example.com -o custom_filename.json

# Capture screenshots during crawl
python run.py crawl https://example.com --with-screenshots
```

**Example output:**

### Analyzing Page Data

The `analyze` command processes the extracted page data using the LLM to generate analysis results.

```bash
# Basic usage
python run.py analyze output/page_data/example_com_home.json

# Save to specific filename
python run.py analyze output/page_data/example_com_home.json -o custom_analysis.json
```

**Example output:**

### Generating Test Scripts

The `generate` command creates comprehensive test scripts based on the analysis results. These scripts can be directly used in your testing framework with minimal adjustments.

```bash
# Basic usage
python run.py generate output/analysis/example_com_home_analysis.json

# Generate for a specific test framework and programming language
python run.py generate output/analysis/example_com_home_analysis.json -f cucumber -l java

# Save to specific directory
python run.py generate output/analysis/example_com_home_analysis.json -o custom_tests
```

**Available options:**

- `-f, --framework`: Test framework to generate (default: cucumber)
- `-l, --language`: Programming language for test implementation (default: java, others: python3)
- `-o, --output`: Custom output directory name
- `--use-vision`: Use vision-enhanced analysis for test generation

**Example output:**

### Advanced Features

#### End-to-End Process

```bash
python run.py e2e https://example.com
```

#### Vision-Enhanced Analysis

The framework now supports vision-enhanced testing using GPT-4o-mini's vision capabilities:

```bash
# Analyze a specific page with vision capabilities
python run.py vision https://example.com
```

#### Vision-Based End-to-End Testing

```bash
# Run end-to-end process with vision capabilities
python run.py vision-e2e https://example.com
```

#### Generating Tests from Vision Analysis

You can generate test scripts based on vision analysis results in the following ways:

1. **Directly from vision analysis files**:

```bash
# Generate tests from a vision analysis file
python run.py generate output/analysis/example_com_vision_analysis.json
```

2. **Using the `--use-vision` flag with standard analysis**:

```bash
# Generate tests with vision enhancement from page data
python run.py generate output/analysis/example_com_analysis.json --use-vision
```

3. **After running vision-e2e process**:
   Tests are automatically generated as part of the vision-e2e process and saved in:
   ```
   output/test_scripts/[domain]_vision_analysis/
   ```

Vision-enhanced test generation provides several benefits:

- Test scenarios based on visual relationships and UI layouts
- Element locators derived from visual analysis
- Test cases for content visibility and visual state validation
- Improved detection of interactive elements that might be missed in DOM-only analysis

**Example output structure**:

```
output/test_scripts/example_com_vision_analysis/
├── test.feature         # Cucumber feature file with scenarios
├── PageObject.java      # Page object with visually identified elements
├── StepDefinitions.java # Step definitions for visual interactions
└── test_scripts.json    # Complete test script data
```

Vision-enhanced testing provides several benefits:

#### User Flow Testing

The framework supports simulating and analyzing user flows through web applications using predefined action sequences.

**User Flow File Format:**

- Create a text file containing one action per line. Ensure this text file is saved inside `flows` folder
  - eg: `flows/login_flow.txt`
- Each line added inside this file describes a specific browser interaction
- Empty lines and lines starting with `#` are treated as comments

**Example User Flow File:**

```text
# Example: login_flow.txt
# Path: flows/login_flow.txt
# Target site: https://practicetestautomation.com/practice-test-login/

# Click the login button to begin
click login button

# Enter credentials
type student into username
type Password123 into password

# Submit the form
click submit
```

**Supported Commands:**

- `click [element description]` - Clicks on an element
- `type [text] into [element description]` - Enters text into a form field
- `select [option] from [element description]` - Selects an option from a dropdown

**Running with User Flows:**

Make sure your user flow file is created and properly formatted before running these commands:

```bash
# Analyze with a predefined user flow
python run.py vision https://example.com --with-flow flows/login_flow.txt

# Run end-to-end process with user flow
python run.py vision-e2e https://example.com --with-flow flows/login_flow.txt
```

**Note:** The user flow file must exist at the specified path when running the command.

#### Site-Wide Testing

The framework now supports generating test scripts for an entire website, not just individual pages:

```bash
# Run end-to-end process for a whole site (up to 50 pages by default)
python run.py e2e https://example.com --site

# Run with vision capabilities for an entire site
python run.py vision-e2e https://example.com --site

# Limit the number of pages to crawl
python run.py e2e https://example.com --site --max-pages 20

# Set custom output directory
python run.py e2e https://example.com --site --output my_site_tests
```

When using site-wide testing, the framework:

1. **Discovers pages**: Uses a sitemap crawler to find all accessible pages within the domain
2. **Optimizes crawling**: Attempts to use sitemap.xml if available, then falls back to discovery crawling
3. **Groups pages by type**: Categorizes pages (login, registration, product, etc.)
4. **Processes in batches**: Handles groups of pages to manage resource usage
5. **Creates comprehensive tests**: Generates tests for each page
6. **Builds a test suite**: Creates a suite structure that organizes tests by page type
7. **Produces a summary report**: Creates documentation with pages tested and test coverage stats

The output structure for site-wide tests:

#### Using External Sitemaps

The framework supports using pre-generated sitemaps from an external repository for efficient testing.

```bash
# Load and process a pre-generated sitemap
python run.py sitemap https://example.com/sitemap.xml
```

When using external sitemaps, the framework:

1. **Loads the sitemap**: Fetches the sitemap from the provided URL
2. **Parses the sitemap**: Extracts URLs for testing
3. **Generates tests**: Creates tests for each URL in the sitemap
4. **Produces a summary report**: Documents the pages tested and test coverage stats

For additional details on working with external sitemaps, including supported formats, filtering options, and integration workflows, see the [external sitemaps documentation](docs/using_external_sitemaps.md).

### Working with Test Generator

The `generate_tests` method in the Test Generator module can be used to create test scripts for discovered pages.

```py
from core.test_generator import TestGenerator
from config.config import Config

# Initialize configuration and test generator
config = Config()
test_generator = TestGenerator(config)

# Generate tests for a specific page
test_generator.generate_tests("output/analysis/example_com_home_analysis.json")

# Generate login-specific test cases
test_generator.generate_login_tests("output/analysis/example_com_login_analysis.json")

# Generate a test suite file that includes all tests
test_generator._generate_test_suite("output/tests/")
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
