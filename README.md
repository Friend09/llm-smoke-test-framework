# LLM Smoke Test Framework

An AI-powered framework for automatically generating smoke tests for web applications using Large Language Models (LLMs) and computer vision capabilities.

## Overview

This framework uses OpenAI's language models (like GPT-4o-mini) to analyze webpages and generate comprehensive smoke test scripts in Cucumber format. It can:

- Crawl single pages or entire websites
- Analyze page structure using both DOM analysis and vision capabilities
- Generate Cucumber feature files, step definitions, and page objects
- Record and incorporate user flows for more accurate tests
- Process and analyze screenshots for better visual understanding

## Key Features

- **Multi-mode Analysis**: Combines traditional DOM analysis with vision-powered screenshot analysis
- **User Flow Integration**: Records and analyzes successful user interactions to generate more realistic tests
- **Site-Wide Testing**: Crawls entire websites and generates cohesive test suites
- **Visual Analysis**: Uses GPT-4o-mini's vision capabilities to analyze page layouts and visual elements
- **Adaptive Test Generation**: Tailors tests to specific page types (login, form, landing, etc.)
- **Flexible Output**: Generates tests in Cucumber format with Java implementations (extensible to other languages)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/llm_smoke_test_framework.git
cd llm_smoke_test_framework
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables (create a `.env` file):

```bash
OPENAI_API_KEY=your_openai_api_key
CHROME_DRIVER_PATH=/path/to/chromedriver  # Optional
OUTPUT_DIR=output  # Default output directory
```

## Usage

### Vision-Enhanced End-to-End Process

Analyze a page with vision capabilities and generate tests:

```bash
python run.py vision-e2e https://example.com/login --language java
```

### Process a Captured User Flow

Record a user flow and generate tests based on it:

```bash
python run.py vision-e2e https://example.com/login --with-flow user_flows/login_flow.txt
```

### Site-Wide Test Generation

Crawl and generate tests for an entire website (limited to max pages):

```bash
python run.py vision-e2e https://example.com --site --max-pages 10
```

### Command Options

- `vision`: Analyze a page with vision capabilities
- `vision-e2e`: End-to-end process using vision capabilities
- `crawl`: Extract page data only
- `analyze`: Analyze pre-extracted page data
- `generate`: Generate tests from analysis
- `e2e`: Complete end-to-end process without vision
- `sitemap`: Work with pre-generated sitemaps

## User Flow Features

The framework can now process complex user interactions beyond just credentials. Supported interactions:

- Click actions (`click button`)
- Text input (`type text into field`)
- Selections (`select option from dropdown`)
- And more interaction types

These interactions are recorded and used to generate more realistic test scripts that replicate actual user behavior.

## Architecture

The framework consists of several core components:

- **WebCrawler**: Extracts page data and captures screenshots
- **LLMAnalyzer**: Analyzes pages using OpenAI models with both text and vision capabilities
- **TestGenerator**: Generates test scripts from analysis results
- **SitemapCrawler**: Discovers and maps website structure

## Config Options

Configuration is handled through the `Config` class and environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LLM_MODEL`: Model to use (default: "gpt-4o-mini")
- `CHROME_DRIVER_PATH`: Optional path to ChromeDriver
- `OUTPUT_DIR`: Directory for output files
- `SCREENSHOT_MAX_DIMENSION`: Max screenshot dimension for vision analysis
- `SCREENSHOT_QUALITY`: JPEG quality for screenshots

## Output Structure

Generated files are organized differently based on whether you're processing a single page or an entire site:

### Single Page Mode (default)

```
output/
├── analysis/           # Analysis results
├── page_data/          # Extracted page data
├── screenshots/        # Captured screenshots
└── test_scripts/       # Generated test scripts
    ├── login/          # Scripts organized by page type
    ├── form/
    └── landing/
```

### Site-Wide Mode (when using --site flag)

```
output/
├── site_e2e_example.com_20250320_124255/      # Site-specific directory with timestamp
│   ├── analysis/                              # Site-specific analysis results
│   ├── page_data/                             # Site-specific extracted page data
│   ├── screenshots/                           # Site-specific screenshots
│   ├── test_scripts/                          # Site-specific test scripts
│   │   └── batch_1/                           # Test scripts organized in batches
│   │       ├── login/                         # Scripts organized by page type
│   │       ├── form/                          # Scripts organized by page type
│   │       └── landing/                       # Scripts organized by page type
│   └── sitemap.json                           # Site structure information
└── another_site_e2e_example2.com_20250320_125045/  # Another site analysis
    ├── ...
```

This organization helps keep tests for different sites separate and makes it easier to manage multiple test generation runs.

## Recent Updates

- **Enhanced User Flow Analysis**: Now extracts and uses all types of interactions, not just login credentials
- **Fixed Test Generation**: Resolved prompt formatting issue for reliable test generation
- **Improved Vision Analysis**: Better integration of DOM and vision-based analysis
- **Site-Wide Processing**: Added support for crawling and analyzing entire websites
- **Optimized Screenshot Handling**: Better image optimization for vision analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
