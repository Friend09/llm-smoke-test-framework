# LLM Smoke Test Framework

An automated framework that uses LLM to generate smoke tests for web applications.

## Features

- Web page crawling and data extraction
- LLM-based analysis of page elements
- Automatic generation of test scripts for multiple frameworks
- Support for Cucumber/Gherkin test format

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/llm-smoke-test-framework.git
cd llm-smoke-test-framework
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### End-to-End Process

Process a URL through the entire pipeline:

```bash
python run.py e2e https://example.com
```

### Individual Steps

1. Crawl a webpage:

```bash
python run.py crawl https://example.com
```

2. Analyze page data:

```bash
python run.py analyze output/page_data/example_com_home.json
```

3. Generate test scripts:

```bash
python run.py generate output/analysis/example_com_home_analysis.json
```

### Additional Options

- Specify output filenames:

  ```bash
  python run.py crawl https://example.com -o custom_name.json
  ```

- Choose a different test framework:

  ```bash
  python run.py e2e https://example.com -f playwright
  ```

## Output

The framework generates:

1. Page data in JSON format
2. Analysis of the page with test recommendations
3. Test scripts:

- Cucumber feature files (`.feature`)
- Step definitions (Java)
- Page Object Model (Java)

## License

MIT

## Usage Instructions

To use this production setup:

1. Install the requirements:

```bash
pip install -r requirements.txt
```

2. Create the `.env` file with your API key.

3. Run the end-to-end process:

```bash
python run.py e2e https://practicetestautomation.com/practice-test-login/
```

Or run individual steps:

```bash
python run.py crawl https://practicetestautomation.com/practice-test-login/
python run.py analyze output/page_data/practicetestautomation_com_practice-test-login.json
python run.py generate output/analysis/practicetestautomation_com_practice-test-login_analysis.json
```

This production setup includes:

- Proper error handling throughout the code
- Comprehensive logging
- Command-line interface with multiple commands
- Configuration via environment variables
- Structured output directories
- Support for different test frameworks
- Detailed documentation

It's ready to be used as a reliable tool in your testing workflow.
