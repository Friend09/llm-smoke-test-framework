# Usage Examples

This guide provides detailed examples of how to use the LLM Smoke Test Framework in various scenarios.

## Basic Usage Examples

### 1. Single Page Analysis with Vision

Analyze a login page with vision capabilities and generate tests:

```bash
python run.py vision-e2e https://example.com/login --language java
```

### 2. Site-Wide Test Generation

Generate tests for an entire website (limited to 20 pages):

```bash
python run.py vision-e2e https://example.com --site --max-pages 20
```

### 3. Analyze Without Vision Capabilities

If you want to use DOM analysis only without the vision capabilities:

```bash
python run.py e2e https://example.com/checkout
```

## User Flow Examples

### 1. Using a Predefined User Flow

Generate tests based on a recorded user flow:

```bash
python run.py vision-e2e https://example.com/login --with-flow flows/login_flow.txt
```

Example content of `login_flow.txt`:

```
type "testuser" into #username
type "password123" into #password
click button#login-button
wait 2
verify text "Welcome, testuser" exists
```

### 2. Recording a New User Flow

You can create your own user flow files. The format is simple:

- One action per line
- Actions include: `type`, `click`, `select`, `wait`, `verify`
- CSS selectors or XPaths for element identification

## Advanced Usage Examples

### 1. Custom Output Directory

Specify a custom output directory:

```bash
python run.py vision-e2e https://example.com/products --output custom_output
```

### 2. Multiple Page Analysis

Analyze multiple specific pages:

```bash
python run.py vision-e2e --urls-file urls.txt --language java
```

Where `urls.txt` contains one URL per line.

### 3. Using with External Sitemaps

Generate tests from an existing sitemap:

```bash
python run.py vision-e2e --sitemap-file sitemap.xml --base-url https://example.com
```

For more information, see [Using External Sitemaps](../advanced/using-external-sitemaps.md).

### 4. Language Selection

Generate tests in a specific language (default is Java):

```bash
python run.py vision-e2e https://example.com --language python
```

Currently supported languages:

- Java (default)
- Python
- JavaScript/TypeScript

### 5. Debugging Mode

Run with verbose logging for debugging:

```bash
python run.py vision-e2e https://example.com --verbose
```

## Automation Integration Examples

### 1. Integration with CI/CD

Example GitHub Actions workflow:

```yaml
name: Generate Smoke Tests

on:
  schedule:
    - cron: "0 0 * * 1" # Run weekly on Mondays
  workflow_dispatch: # Allow manual triggers

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Generate tests
        run: python run.py vision-e2e https://example.com --site --max-pages 10
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      - name: Archive test artifacts
        uses: actions/upload-artifact@v2
        with:
          name: smoke-tests
          path: output/
```

### 2. Integration with Test Management Systems

You can automate the import of generated tests into test management systems:

```bash
python run.py vision-e2e https://example.com --site --export-format jira
```

This will generate tests in a format compatible with Jira Xray or other test management imports.

## Filter Options Examples

### 1. Filtering by Page Type

Generate tests only for specific page types:

```bash
python run.py vision-e2e https://example.com --site --page-types login,form,landing
```

### 2. Excluding Pages by Pattern

Exclude certain URLs matching patterns:

```bash
python run.py vision-e2e https://example.com --site --exclude-pattern "blog|news|faq"
```

This will exclude URLs containing "blog", "news", or "faq".
