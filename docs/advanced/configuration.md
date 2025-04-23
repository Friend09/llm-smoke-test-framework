# Configuration

This page explains how to configure the LLM Smoke Test Framework to suit your specific needs.

## Configuration Options

The framework can be configured in multiple ways, with settings that affect crawling, analysis, test generation, and output handling.

## Configuration Methods

The framework supports three configuration methods, in order of precedence:

1. **Command-line Arguments**: Highest precedence, overrides all other settings
2. **Environment Variables**: Overrides default settings
3. **Default Settings**: Used when no overrides are provided

## Environment Variables

Environment variables can be set in your system or in a `.env` file in the project root:

```bash
# Example .env file
OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=gpt-4o-mini
OUTPUT_DIR=my_custom_output
CHROME_DRIVER_PATH=/path/to/chromedriver
MAX_PAGES=15
```

## Core Configuration Options

### API Configuration

| Environment Variable | Command-line Option | Description         | Default         |
| -------------------- | ------------------- | ------------------- | --------------- |
| `OPENAI_API_KEY`     | N/A                 | Your OpenAI API key | None (Required) |
| `LLM_MODEL`          | `--model`           | OpenAI model to use | `gpt-4o-mini`   |

### Output Configuration

| Environment Variable | Command-line Option  | Description                | Default   |
| -------------------- | -------------------- | -------------------------- | --------- |
| `OUTPUT_DIR`         | `--output`, `-o`     | Directory for output files | `output`  |
| `OUTPUT_STRUCTURE`   | `--output-structure` | Output directory structure | `default` |
| `SAVE_SCREENSHOTS`   | `--save-screenshots` | Save screenshots in output | `True`    |
| `SAVE_ANALYSIS`      | `--save-analysis`    | Save analysis results      | `True`    |

### Crawler Configuration

| Environment Variable | Command-line Option | Description                  | Default       |
| -------------------- | ------------------- | ---------------------------- | ------------- |
| `CHROME_DRIVER_PATH` | N/A                 | Path to ChromeDriver         | Auto-detected |
| `PAGE_TIMEOUT`       | `--timeout`         | Page load timeout in seconds | `30`          |
| `HEADLESS_BROWSER`   | `--headless`        | Run browser in headless mode | `True`        |
| `VIEWPORT_WIDTH`     | `--viewport-width`  | Browser viewport width       | `1280`        |
| `VIEWPORT_HEIGHT`    | `--viewport-height` | Browser viewport height      | `800`         |

### Site-Wide Crawling Configuration

| Environment Variable | Command-line Option | Description                   | Default |
| -------------------- | ------------------- | ----------------------------- | ------- |
| `MAX_PAGES`          | `--max-pages`       | Maximum pages to crawl        | `10`    |
| `CRAWL_DEPTH`        | `--depth`           | Maximum crawl depth           | `2`     |
| `EXCLUDE_PATTERN`    | `--exclude-pattern` | Regex pattern to exclude URLs | None    |
| `INCLUDE_PATTERN`    | `--include-pattern` | Regex pattern to include URLs | None    |
| `BATCH_SIZE`         | `--batch-size`      | Batch size for processing     | `10`    |

### Vision Configuration

| Environment Variable       | Command-line Option | Description              | Default |
| -------------------------- | ------------------- | ------------------------ | ------- |
| `VISION_ENABLED`           | `--vision-enabled`  | Enable vision analysis   | `True`  |
| `VISION_QUALITY`           | `--vision-quality`  | Image quality for vision | `auto`  |
| `SCREENSHOT_MAX_DIMENSION` | N/A                 | Max screenshot dimension | `1200`  |
| `SCREENSHOT_QUALITY`       | N/A                 | JPEG quality (0-100)     | `85`    |

### Test Generation Configuration

| Environment Variable    | Command-line Option       | Description                    | Default    |
| ----------------------- | ------------------------- | ------------------------------ | ---------- |
| `TEST_LANGUAGE`         | `--language`              | Target language for tests      | `java`     |
| `TEST_FRAMEWORK`        | `--framework`             | Test framework to use          | `cucumber` |
| `SCENARIOS_PER_PAGE`    | `--scenarios`             | Scenarios to generate per page | `3`        |
| `INCLUDE_ASSERTIONS`    | `--include-assertions`    | Include detailed assertions    | `True`     |
| `GENERATE_PAGE_OBJECTS` | `--generate-page-objects` | Generate page object classes   | `True`     |

## The Config Class

Internally, the framework uses a `Config` class to manage configuration. You can access this programmatically:

```python
from config.config import Config

# Get the current configuration
config = Config()

# Access configuration values
api_key = config.openai_api_key
output_dir = config.output_dir

# Override configuration values
config.max_pages = 20
config.vision_enabled = False
```

## Configuration File (Experimental)

The framework also supports an experimental YAML configuration file for project-specific settings:

```yaml
# config.yaml example
llm:
  model: gpt-4o-mini
  max_tokens: 4000
  temperature: 0.1

crawler:
  timeout: 30
  headless: true
  viewport:
    width: 1280
    height: 800

output:
  dir: custom_output
  save_screenshots: true
  save_analysis: true

site_crawler:
  max_pages: 15
  depth: 3
  exclude_pattern: "(blog|news|faq)"
  batch_size: 5

test_generation:
  language: java
  framework: cucumber
  scenarios_per_page: 3
  generate_page_objects: true
```

To use this configuration file:

```bash
python run.py vision-e2e https://example.com --config config.yaml
```

## Best Practices

1. **Use a .env File**: Store your API key and common settings in a `.env` file
2. **Command-line for Variations**: Use command-line options for run-specific variations
3. **Environment Variables for CI/CD**: Use environment variables in CI/CD pipelines
4. **Version Control**: Include example configuration files in version control, but exclude files with secrets

## Troubleshooting

If you're experiencing configuration issues:

1. Check for typos in environment variable names
2. Verify the precedence (command-line overrides environment variables)
3. Use the `--verbose` flag to see the effective configuration
4. Check for conflicting settings
