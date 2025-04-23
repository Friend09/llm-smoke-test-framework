# Sitemap Crawler

The Sitemap Crawler is a specialized component of the LLM Smoke Test Framework responsible for discovering and mapping the structure of websites for site-wide testing.

## Overview

The `SitemapCrawler` class discovers pages on a website by following links and builds a structured representation of the site. This enables the framework to generate comprehensive test suites that cover entire websites rather than just individual pages.

## Features

- **Automated Discovery**: Finds all accessible pages on a website
- **Depth Control**: Limits crawling to a specified depth
- **Pattern Filtering**: Includes or excludes pages based on URL patterns
- **Link Relationship Mapping**: Creates a map of how pages are connected
- **Crawl Optimization**: Intelligently manages crawling to avoid redundancy
- **External Sitemap Support**: Works with existing XML sitemaps

## Usage

The Sitemap Crawler can be used directly or through the framework's site-wide commands:

```python
from core.sitemap_crawler import SitemapCrawler
from core.crawler import WebCrawler

# Initialize the crawlers
web_crawler = WebCrawler()
sitemap_crawler = SitemapCrawler(max_pages=20, depth=2)

# Crawl a site starting from the homepage
sitemap = sitemap_crawler.crawl_site("https://example.com", web_crawler)

# Access all discovered pages
for page_url in sitemap.urls:
    print(f"Discovered: {page_url}")

# Access the relationship map
for page_url, links in sitemap.link_map.items():
    print(f"Page {page_url} links to: {links}")
```

## Configuration Options

The Sitemap Crawler behavior can be customized through several options:

| Option                  | Description                       | Default              |
| ----------------------- | --------------------------------- | -------------------- |
| `max_pages`             | Maximum number of pages to crawl  | `10`                 |
| `depth`                 | Maximum crawl depth               | `2`                  |
| `include_pattern`       | Regex pattern for URLs to include | None (all included)  |
| `exclude_pattern`       | Regex pattern for URLs to exclude | None (none excluded) |
| `respect_robots`        | Respect robots.txt                | `True`               |
| `follow_external_links` | Follow links to external domains  | `False`              |
| `crawl_delay`           | Delay between requests in seconds | `0.1`                |

## Sitemap Structure

The Sitemap Crawler generates a `Sitemap` object with the following structure:

```python
class Sitemap:
    base_url: str              # The base URL of the site
    urls: list                 # List of all discovered URLs
    link_map: dict             # Map of URLs to their outgoing links
    page_types: dict           # Map of URLs to their page types
    visited: set               # Set of URLs that have been crawled
    metadata: dict             # Additional metadata about the site
    crawl_info: dict           # Information about the crawl process
```

## Advanced Usage

### Using with External Sitemaps

The framework can also work with pre-existing XML sitemaps:

```python
from core.sitemap_loader import SitemapLoader

# Load from an XML sitemap
loader = SitemapLoader()
sitemap = loader.load_from_url("https://example.com/sitemap.xml")

# Process the loaded sitemap
for url in sitemap.urls:
    page_data = web_crawler.crawl(url)
    analysis_result = analyzer.analyze(page_data)
    # Generate tests...
```

### Controlling Crawl Scope

You can control which pages are included in the crawl:

```python
# Include only certain paths
sitemap_crawler = SitemapCrawler(
    max_pages=30,
    include_pattern=r"(login|checkout|product)",
    exclude_pattern=r"(blog|news|faq)"
)

# Crawl with these filters
sitemap = sitemap_crawler.crawl_site("https://example.com", web_crawler)
```

### Batched Processing

For large sites, you can process pages in batches:

```python
# Get all URLs from the sitemap
urls = sitemap.urls

# Process in batches of 10
batch_size = 10
for i in range(0, len(urls), batch_size):
    batch_urls = urls[i:i+batch_size]

    # Process this batch
    for url in batch_urls:
        # Process each URL...
```

## Sitemap Visualization

The Sitemap Crawler can generate visualizations of the site structure:

```python
# Generate a visual representation (requires graphviz)
sitemap.generate_visualization("sitemap.png")
```

This creates a visual graph showing pages and their relationships, which can be useful for understanding the site structure.

## Working with Large Sites

When working with large sites, consider these strategies:

1. **Start Small**: Begin with a limited depth and max pages
2. **Use Filters**: Focus on specific areas of the site
3. **Incremental Crawling**: Crawl different sections in separate runs
4. **Save Intermediate Results**: Save the sitemap to disk for later use

Example for incremental crawling:

```python
# First run - crawl the product section
product_sitemap = sitemap_crawler.crawl_site(
    "https://example.com/products",
    web_crawler,
    include_pattern=r"product"
)
product_sitemap.save("product_sitemap.json")

# Second run - crawl the checkout section
checkout_sitemap = sitemap_crawler.crawl_site(
    "https://example.com/checkout",
    web_crawler,
    include_pattern=r"checkout"
)
checkout_sitemap.save("checkout_sitemap.json")

# Combine sitemaps
combined_sitemap = Sitemap.combine([product_sitemap, checkout_sitemap])
```

## Best Practices

1. **Respect Website Limits**: Use appropriate delays between requests
2. **Focus on Key Paths**: Use include/exclude patterns to focus on important pages
3. **Monitor Resource Usage**: Large crawls can consume significant resources
4. **Incremental Approach**: Start with a small section of the site and expand
5. **Authenticated Crawling**: For protected areas, combine with user flows
