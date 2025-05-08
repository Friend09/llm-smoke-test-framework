# LLM Smoke Test Framework (Playwright Edition)

A simple, powerful framework for automated smoke testing of any web application using Playwright and LLMs.

## Features
- Crawls all pages of a web app (including dynamic navigation, menus, tabs, etc.) using Playwright
- Handles login automatically if required (credentials from `.env`)
- Captures screenshots and page data for every page
- Uses LLM to analyze pages, detect login, and generate smoke test scripts
- **Generates both Gherkin feature files and Selenium automation scripts in Java by default**
- Optionally generates automation scripts for other frameworks (Playwright, Cypress, etc.) and languages (JS, Python, etc.)
- Minimal setup, works with most web apps (including ASPX, React, etc.)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Set up your `.env` file:**
   ```env
   OPENAI_API_KEY=your-openai-key
   USERNAME=your-login-username
   PASSWORD=your-login-password
   # Add any other credentials as needed
   ```

## Usage

Run the framework from the command line:

```bash
python run.py vision-e2e <website_url> [--page-only | --site] [--max-pages N]
```

### Options
- `--page-only` : Only generate a test for the initial page (no crawling)
- `--site` : Crawl and generate tests for the entire site (default)
- `--max-pages N` : Limit the number of pages to crawl and generate tests for (e.g., `--max-pages 10`)

### Examples
- **Test only the initial page:**
  ```bash
  python run.py vision-e2e https://example.com --page-only
  ```
- **Test the entire site (default):**
  ```bash
  python run.py vision-e2e https://example.com --site
  ```
- **Test up to 10 pages:**
  ```bash
  python run.py vision-e2e https://example.com --max-pages 10
  ```

- The framework will:
  1. Launch a browser and visit the URL
  2. Take a screenshot and extract page data
  3. Ask the LLM if the page is a login page
  4. If login is required, it will log in using `.env` credentials
  5. Recursively crawl all pages, including those behind navigation menus, tabs, and dynamic elements
  6. For each page, capture a screenshot, extract data, and generate:
     - a Gherkin feature file (`.feature`)
     - a Selenium automation script in Java (`.java`)
     - (optionally) scripts for other frameworks/languages if specified
  7. Save all results (screenshots, data, test scripts) to the output directory

### Customizing Script Generation

By default, the framework generates Selenium scripts in Java. To generate scripts for other frameworks/languages (e.g., Playwright in JS, Cypress, etc.), update your call to the LLM analyzer:

```python
# Example: Generate Playwright script in JS
llm_analyzer.generate_test_script(page_analysis, framework="playwright", language="js")
```

## Output
- Screenshots: `output/screenshots/`
- Page data: `output/page_data/`
- Test scripts:
  - Gherkin feature files: `output/tests/*_smoketest.feature`
  - Selenium Java scripts: `output/tests/*_smoketest.java`
  - (Other frameworks/languages as requested)

## Supported Applications
- Works with most web applications, including:
  - ASPX/.NET
  - React, Angular, Vue
  - Traditional server-rendered sites
  - Sites with dynamic navigation/menus

## Extending
- Add more credentials to `.env` as needed
- Customize LLM prompts in `core/llm_analyzer.py`
- Change the default script framework/language by passing parameters to `generate_test_script`

## License
MIT
