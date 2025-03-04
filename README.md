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
    - [LLM Analyzer](#llm-analyzer)
    - [Web Crawler](#web-crawler)
  - [⚙️ Usage](#️-usage)
    - [End-to-End Process](#end-to-end-process)
    - [Individual Steps](#individual-steps)
  - [📤 Output](#-output)
  - [🤝 Contributing](#-contributing)
  - [📜 License](#-license)

## ✨ Features

- **Automated Test Generation:** Leverages LLMs to create robust smoke tests
- **Web Crawling:** Discovers and extracts key elements from web pages
- **Configurable:** Easily adaptable to different testing frameworks and environments
- **Modular Design:** Supports individual step execution for customized workflows

## 🚀 Quick Setup

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/llm-smoke-test-framework.git
cd llm-smoke-test-framework
```

2. **Run the setup script:**

```bash
python setup.py
```

3. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Configure environment variables:**

```bash
cp .env.example .env
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
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

## 🗂️ Project Structure

```
llm-smoke-test-framework/
├── config/             # Configuration management
├── core/              # Core functionality
├── output/            # Generated outputs
├── tests/             # Tests
├── .env.example       # Environment variables template
├── requirements.txt   # Project dependencies
└── run.py            # Main entry point
```

## 🔧 Implementation Details

### LLM Analyzer

- `analyze_page`: Processes crawler data through LLM
- `generate_test_script`: Creates test scripts from analysis
- `_generate_cucumber_script`: Handles Cucumber-specific generation

### Web Crawler

- `extract_page_data`: Extracts page elements and structure
- `save_page_data`: Stores extracted data in JSON format

## ⚙️ Usage

### End-to-End Process

```bash
python run.py e2e https://example.com
```

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

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

## 📜 License

[MIT License](LICENSE)
