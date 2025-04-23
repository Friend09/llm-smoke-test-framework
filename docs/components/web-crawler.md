# Web Crawler

The Web Crawler is a core component of the LLM Smoke Test Framework responsible for extracting data from web pages.

## Overview

The `WebCrawler` class handles all interactions with web pages, including navigation, DOM extraction, and screenshot capture. It uses Selenium WebDriver to automate browser interactions and extract page information.

## Features

- **Browser Automation**: Uses Selenium WebDriver to control Chrome/Chromium
- **DOM Extraction**: Captures full HTML structure and element metadata
- **Screenshot Capture**: Takes optimized screenshots for vision analysis
- **Responsive Testing**: Can simulate different viewport sizes
- **Element Detection**: Identifies interactive elements like forms and buttons
- **Error Handling**: Gracefully handles page load timeouts and errors

## Usage

The Web Crawler can be used directly or through the framework's main commands:

```python
from core.crawler import WebCrawler

# Initialize the crawler
crawler = WebCrawler()

# Crawl a single page
page_data = crawler.crawl("https://example.com/login")

# Access extracted data
html = page_data.html
screenshot_path = page_data.screenshot_path
interactive_elements = page_data.interactive_elements
```

## Configuration Options

The Web Crawler behavior can be customized through several options:

| Option                  | Description                  | Default       |
| ----------------------- | ---------------------------- | ------------- |
| `timeout`               | Page load timeout in seconds | 30            |
| `headless`              | Run browser in headless mode | True          |
| `viewport_width`        | Browser viewport width       | 1280          |
| `viewport_height`       | Browser viewport height      | 800           |
| `user_agent`            | Custom user agent string     | None          |
| `wait_for_network_idle` | Wait for network to be idle  | True          |
| `chrome_driver_path`    | Path to ChromeDriver         | Auto-detected |

## Page Data Structure

When a page is crawled, the `WebCrawler` returns a `PageData` object with the following properties:

```python
class PageData:
    url: str                  # The URL that was crawled
    title: str                # Page title
    html: str                 # Full HTML content
    screenshot_path: str      # Path to the screenshot file
    interactive_elements: list # List of interactive elements found
    forms: list               # List of forms detected
    links: list               # List of links on the page
    metadata: dict            # Additional page metadata
    timestamp: datetime       # When the page was crawled
```

## Advanced Usage

### Handling Authentication

The Web Crawler can handle authenticated sessions:

```python
# Login flow
crawler.navigate_to("https://example.com/login")
crawler.find_element("input#username").send_keys("user")
crawler.find_element("input#password").send_keys("pass")
crawler.find_element("button[type=submit]").click()
crawler.wait_for_navigation()

# Now crawl authenticated pages
page_data = crawler.crawl("https://example.com/dashboard")
```

### Using User Flows

The Web Crawler can execute pre-recorded user flows:

```python
from core.crawler import WebCrawler, UserFlow

# Load a user flow
flow = UserFlow.from_file("flows/login_flow.txt")

# Execute the flow
crawler = WebCrawler()
crawler.execute_flow(flow, "https://example.com/login")

# Capture the resulting page
page_data = crawler.capture_current_page()
```

### Site-Wide Crawling

For crawling entire sites, the `SitemapCrawler` extension should be used:

```python
from core.sitemap_crawler import SitemapCrawler

# Initialize the sitemap crawler
sitemap_crawler = SitemapCrawler(max_pages=20, depth=2)

# Crawl a site starting from the homepage
sitemap = sitemap_crawler.crawl_site("https://example.com")

# Access all crawled pages
for page_url in sitemap.urls:
    page_data = sitemap.get_page_data(page_url)
```

## Error Handling

The Web Crawler includes robust error handling:

```python
try:
    page_data = crawler.crawl("https://example.com/page")
except PageLoadTimeoutException:
    print("Page load timed out")
except ElementNotFoundException as e:
    print(f"Element not found: {e.selector}")
except BrowserException as e:
    print(f"Browser error: {str(e)}")
```

## Performance Optimization

For better performance, consider:

1. Using headless mode (`headless=True`)
2. Adjusting timeouts for your target site
3. Limiting screenshot quality for faster processing
4. Using batch processing for multiple pages
