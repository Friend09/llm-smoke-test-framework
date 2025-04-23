# Command Reference

This page provides a complete reference for all commands and options available in the LLM Smoke Test Framework.

## Main Commands

The framework supports several main commands that determine the operation mode:

| Command      | Description                                                   |
| ------------ | ------------------------------------------------------------- |
| `vision`     | Analyze a page with vision capabilities (screenshot analysis) |
| `vision-e2e` | End-to-end process using vision capabilities                  |
| `crawl`      | Extract page data only without analysis                       |
| `analyze`    | Analyze pre-extracted page data                               |
| `generate`   | Generate tests from analysis results                          |
| `e2e`        | Complete end-to-end process without vision                    |
| `sitemap`    | Work with pre-generated sitemaps                              |

## Basic Options

These options can be used with most commands:

| Option            | Description                      | Default  |
| ----------------- | -------------------------------- | -------- |
| `--language`      | Target language for test scripts | `java`   |
| `--output`, `-o`  | Custom output directory          | `output` |
| `--verbose`, `-v` | Enable verbose logging           | `False`  |
| `--help`, `-h`    | Show help message                | -        |
| `--version`       | Show version information         | -        |

## URL and Input Options

| Option           | Description                                      |
| ---------------- | ------------------------------------------------ |
| `--urls-file`    | File containing URLs to process (one per line)   |
| `--sitemap-file` | Pre-generated sitemap file to use                |
| `--base-url`     | Base URL for relative links in sitemap           |
| `--with-flow`    | User flow file to incorporate in test generation |

## Crawling Options

| Option              | Description                       | Default |
| ------------------- | --------------------------------- | ------- |
| `--site`            | Enable site-wide crawling         | `False` |
| `--max-pages`       | Maximum number of pages to crawl  | `10`    |
| `--depth`           | Maximum crawl depth               | `2`     |
| `--timeout`         | Page load timeout in seconds      | `30`    |
| `--exclude-pattern` | Regex pattern for URLs to exclude | -       |
| `--include-pattern` | Regex pattern for URLs to include | -       |

## Analysis Options

| Option             | Description                                   | Default       |
| ------------------ | --------------------------------------------- | ------------- |
| `--page-types`     | Comma-separated list of page types to analyze | `all`         |
| `--model`          | OpenAI model to use                           | `gpt-4o-mini` |
| `--vision-quality` | Image quality for vision analysis             | `auto`        |
| `--dom-only`       | Use only DOM analysis (no vision)             | `False`       |
| `--no-cache`       | Disable caching of analysis results           | `False`       |

## Test Generation Options

| Option                    | Description                              | Default    |
| ------------------------- | ---------------------------------------- | ---------- |
| `--framework`             | Test framework to use                    | `cucumber` |
| `--scenarios`             | Number of scenarios to generate per page | `3`        |
| `--export-format`         | Format for exporting tests               | `default`  |
| `--include-assertions`    | Include detailed assertions              | `True`     |
| `--generate-page-objects` | Generate page object classes             | `True`     |

## Output Control Options

| Option               | Description                         | Default   |
| -------------------- | ----------------------------------- | --------- |
| `--output-structure` | Output directory structure          | `default` |
| `--batch-size`       | Batch size for site-wide processing | `10`      |
| `--save-screenshots` | Save screenshots in output          | `True`    |
| `--save-analysis`    | Save analysis results in output     | `True`    |

## Environment Variable Equivalents

Most command-line options can also be specified as environment variables:

| Environment Variable | Equivalent Option         |
| -------------------- | ------------------------- |
| `OPENAI_API_KEY`     | (Required for API access) |
| `LLM_MODEL`          | `--model`                 |
| `OUTPUT_DIR`         | `--output`                |
| `CHROME_DRIVER_PATH` | (Path to ChromeDriver)    |
| `MAX_PAGES`          | `--max-pages`             |
| `CRAWL_DEPTH`        | `--depth`                 |
| `PAGE_TIMEOUT`       | `--timeout`               |
| `TEST_LANGUAGE`      | `--language`              |
| `TEST_FRAMEWORK`     | `--framework`             |
| `SCREENSHOT_QUALITY` | `--vision-quality`        |

## Command Examples

### Vision E2E Command

```bash
python run.py vision-e2e https://example.com/login \
  --language java \
  --output myoutput \
  --with-flow flows/login_flow.txt \
  --page-types login,form \
  --generate-page-objects
```

### Site-Wide Crawling

```bash
python run.py vision-e2e https://example.com \
  --site \
  --max-pages 20 \
  --depth 3 \
  --exclude-pattern "blog|news" \
  --batch-size 5
```

### Working with Sitemaps

```bash
python run.py sitemap \
  --sitemap-file sitemap.xml \
  --base-url https://example.com \
  --output sitemap_output
```

### Advanced Analysis Options

```bash
python run.py analyze \
  --input-data page_data/example_page.json \
  --model gpt-4o \
  --vision-quality high \
  --no-cache
```
