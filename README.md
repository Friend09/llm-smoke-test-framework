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
    - [Command Reference](#command-reference)
    - [Basic Commands](#basic-commands)
      - [Crawling a Webpage](#crawling-a-webpage)
    - [Analyzing Page Data](#analyzing-page-data)
    - [Generating Test Scripts](#generating-test-scripts)
    - [Advanced Features](#advanced-features)
      - [End-to-End Process](#end-to-end-process)
      - [Vision-Enhanced Analysis](#vision-enhanced-analysis)
      - [Vision-Based End-to-End Testing](#vision-based-end-to-end-testing)
      - [User Flow Testing](#user-flow-testing)
    - [Working with Test Generator](#working-with-test-generator)
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

Vision-enhanced testing provides several benefits:

- Better understanding of page layout and visual elements
- Improved element locator strategies based on visual context
- More comprehensive test scenarios that consider visual relationships
- Enhanced ability to test complex UI components

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
