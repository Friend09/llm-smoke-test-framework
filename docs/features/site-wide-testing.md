# Site-Wide Testing

The site-wide testing feature allows you to generate comprehensive test suites for entire websites instead of just individual pages.

## Overview

While testing individual pages is valuable, many applications require end-to-end testing across multiple interconnected pages. The site-wide testing feature crawls entire websites, analyzes the relationships between pages, and generates cohesive test suites that cover complete user journeys.

## Benefits of Site-Wide Testing

- **Comprehensive Coverage**: Test all key pages in your application
- **Path-Based Testing**: Generate tests that follow user paths through your site
- **Cross-Page Validation**: Verify data persistence between pages
- **Navigation Testing**: Ensure navigation elements work correctly
- **Structure Understanding**: Tests that understand your site's architecture

## Using Site-Wide Testing

To enable site-wide testing, use the `--site` flag with the `vision-e2e` command:

```bash
python run.py vision-e2e https://example.com --site --max-pages 20
```

### Key Options

| Option              | Description                   | Default |
| ------------------- | ----------------------------- | ------- |
| `--site`            | Enable site-wide crawling     | `False` |
| `--max-pages`       | Maximum pages to crawl        | `10`    |
| `--depth`           | Maximum crawl depth           | `2`     |
| `--exclude-pattern` | Regex pattern to exclude URLs | None    |
| `--include-pattern` | Regex pattern to include URLs | None    |
| `--batch-size`      | Batch size for processing     | `10`    |

## How It Works

1. **Discovery Phase**: The SitemapCrawler component discovers pages starting from the provided URL
2. **Crawling Phase**: Each discovered page is crawled to extract data and screenshots
3. **Analysis Phase**: Pages are analyzed individually and in relation to each other
4. **Generation Phase**: Tests are generated considering the relationship between pages
5. **Output Phase**: Test files are organized in a structured directory layout

## Output Structure

When using site-wide testing, the output is organized in a special structure:

```
output/
├── site_e2e_example.com_20250423_124255/      # Site-specific directory with timestamp
│   ├── analysis/                              # Site-specific analysis results
│   ├── page_data/                             # Site-specific extracted page data
│   ├── screenshots/                           # Site-specific screenshots
│   ├── test_scripts/                          # Site-specific test scripts
│   │   └── batch_1/                           # Test scripts organized in batches
│   │       ├── login/                         # Scripts organized by page type
│   │       ├── form/                          # Scripts organized by page type
│   │       └── landing/                       # Scripts organized by page type
│   └── sitemap.json                           # Site structure information
```

## Advanced Usage

### Controlling Crawl Scope

You can control which pages are included in the crawl:

```bash
python run.py vision-e2e https://example.com --site \
  --include-pattern "(login|checkout|product)" \
  --exclude-pattern "(blog|news|faq)" \
  --max-pages 30 \
  --depth 3
```

### Processing Large Sites

For large sites, you can use batching to process pages in manageable groups:

```bash
python run.py vision-e2e https://example.com --site \
  --max-pages 100 \
  --batch-size 20
```

### Using with Sitemap XML

If the site has a sitemap.xml file, you can use it to guide the crawling:

```bash
python run.py vision-e2e --sitemap-file https://example.com/sitemap.xml --site
```

## Best Practices

1. **Start Small**: Begin with a limited number of pages (5-10) to test the process
2. **Use Include/Exclude Patterns**: Focus on the most important parts of your site
3. **Consider Authentication**: Use user flows for authenticated sections
4. **Monitor Resources**: Site-wide testing uses more API resources and time
5. **Incremental Testing**: Add new sections of your site over time

## Example: E-commerce Site Testing

Here's how you might test an e-commerce site:

```bash
python run.py vision-e2e https://example-shop.com --site \
  --include-pattern "(product|cart|checkout|account)" \
  --exclude-pattern "(blog|support|about)" \
  --max-pages 25 \
  --with-flow flows/login_flow.txt \
  --with-flow flows/checkout_flow.txt
```

This would:

1. Crawl up to 25 pages of the e-commerce site
2. Focus on product, cart, checkout, and account pages
3. Skip blog, support, and about pages
4. Include login and checkout user flows for authenticated testing

## Limitations

- **Dynamic Content**: Very dynamic sites may need additional configuration
- **Rate Limits**: Respect website rate limits to avoid being blocked
- **API Usage**: Larger sites consume more API tokens
- **Authentication**: Some sites may require authenticated testing

## Performance Tips

1. **Use DOM-only for Initial Crawl**: Skip vision for the initial site mapping

   ```bash
   python run.py e2e https://example.com --site --dom-only
   ```

2. **Use Selective Vision**: Apply vision only to complex pages

   ```bash
   python run.py vision-e2e https://example.com --site --page-types form,checkout
   ```

3. **Batch Processing**: Use batches for large sites
   ```bash
   python run.py vision-e2e https://example.com --site --batch-size 10
   ```
