# LLM-Enhanced Smoke Test Generator

An intelligent framework for automated smoke test generation using web crawling and large language models.

## Overview

This framework automatically discovers and tests web applications by:

1. Crawling the application to discover all pages and interactive elements
2. Using LLMs (like OpenAI's GPT models) to analyze page structure
3. Generating comprehensive smoke tests with Cucumber features, step definitions, and page objects
4. Integrating with existing Selenium and WebDriverIO test infrastructure

The framework solves common challenges in test automation, including:

- Discovering hidden pages and dynamic content
- Correctly extracting all URLs and interactive elements
- Handling different authentication methods (Basic, NTLM, Okta)
- Creating maintainable and reliable test scripts

## Features

### Enhanced Web Crawler

- Handles various authentication types
- Advanced URL extraction for all page elements
- Support for iframes, popups, and dynamic content
- Systematic discovery of all application pages

### LLM-Powered Test Generation

- Analyzes page structure to identify key elements
- Generates comprehensive smoke tests for each page
- Creates maintainable page objects and step definitions
- Identifies optimal locator strategies

### Framework Integration

- Compatible with Cucumber
- Supports both Java and TypeScript implementations
- Works with Selenium and WebDriverIO

### Customizable Configuration

- Environment variable configuration
- Command-line interface
- Configurable depth and scope of testing

## Prerequisites

- Python 3.8+
- Java JDK 11+ (for Java tests) or Node.js 14+ (for TypeScript tests)
- Chrome browser
- OpenAI API key

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/llm-smoke-test-generator.git
cd llm-smoke-test-generator

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and modify .env file
cp .env.example config/.env
# Edit .env with your settings
```

## Quick Start

1. Configure your environment variables in `.env`
2. Run the crawler and test generator:

```bash
python runners/crawler_runner.py --url https://your-app.com --auth basic
```

3. Find generated tests in the `output/test_scripts` directory
4. Execute tests with your testing framework

## Usage

### Basic Usage

```bash
python runners/crawler_runner.py --url https://your-app.com
```

### Advanced Options

```bash
python runners/crawler_runner.py \
  --url https://your-app.com \
  --depth 4 \
  --auth okta \
  --output custom_output \
  --framework cucumber \
  --language typescript \
  --headless
```

### Command Line Options

| Option         | Description                             | Default   |
| -------------- | --------------------------------------- | --------- |
| `--url`        | Starting URL to crawl                   | From .env |
| `--depth`      | Maximum depth to crawl                  | 3         |
| `--auth`       | Authentication type (basic, ntlm, okta) | From .env |
| `--output`     | Output directory                        | output    |
| `--framework`  | Test framework (cucumber)               | cucumber  |
| `--language`   | Programming language (java, typescript) | java      |
| `--headless`   | Run in headless mode                    | False     |
| `--skip-crawl` | Skip crawling and use existing data     | False     |

## Project Structure

```
llm_smoke_test_framework/
│
├── config/                  # Configuration settings
│   ├── config.py            # Config loader
│   └── .env                 # Environment variables
│
├── core/                    # Core components
│   ├── crawler.py           # Web crawler
│   ├── auth_handler.py      # Authentication handling
│   ├── llm_analyzer.py      # LLM integration
│   └── test_generator.py    # Test script generation
│
├── utils/                   # Utility functions
│   ├── url_extractor.py     # URL extraction
│   ├── element_finder.py    # UI element detection
│   └── html_parser.py       # HTML parsing
│
├── output/                  # Generated output
│   ├── discovered_pages/    # Crawler results
│   ├── test_scripts/        # Generated tests
│   └── reports/             # Test reports
│
├── runners/                 # Execution scripts
│   ├── crawler_runner.py    # Main runner
│   └── test_runner.py       # Test executor
│
└── tests/                   # Tests for the framework
    ├── unit/                # Unit tests
    └── integration/         # Integration tests
```

## Configuration

Create a `.env` file in the root directory (or inside the config directory) with the following variables:

```
# Application settings
BASE_URL=https://example.com
BROWSER=chrome
HEADLESS=True

# Authentication settings
AUTH_TYPE=basic  # Options: basic, ntlm, okta
USERNAME=your_username
PASSWORD=your_password
OKTA_URL=https://your-company.okta.com

# Crawler settings
MAX_DEPTH=3
EXCLUDE_PATTERNS=logout,#,javascript:
INCLUDE_SUBDOMAINS=True

# Selenium settings
IMPLICIT_WAIT=10
PAGE_LOAD_TIMEOUT=30

# LLM settings
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini

# Output settings to save the results
OUTPUT_DIR=output
```

## Generated Test Structure

The framework generates the following for each discovered page:

1. **Feature File** - Cucumber scenario for smoke testing
2. **Page Object** - Encapsulated page interactions and locators
3. **Step Definitions** - Test steps implementation

Example structure:

```
output/test_scripts/
├── features/
│   └── login_page.feature
├── page_objects/
│   └── LoginPage.java
└── step_definitions/
    └── LoginPageSteps.java
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for API access
- Selenium and WebDriverIO communities
- Cucumber for BDD framework

## Contact

If you have any questions or feedback, please open an issue on GitHub.
