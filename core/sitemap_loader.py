import os
import logging
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SitemapLoader:
    """
    Loads pre-generated sitemaps from external sources and makes them available
    for the smoke test framework.
    """

    def __init__(self, config=None):
        """Initialize the sitemap loader.

        Args:
            config: Configuration object
        """
        from config.config import Config
        self.config = config or Config()

    def load_sitemap_from_file(self, file_path: str) -> List[str]:
        """
        Load URLs from a pre-generated sitemap file.

        Args:
            file_path: Path to the sitemap file

        Returns:
            List of URLs from the sitemap
        """
        try:
            logger.info(f"Loading sitemap from {file_path}")

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Sitemap file not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

            logger.info(f"Loaded {len(urls)} URLs from sitemap file")
            return urls

        except Exception as e:
            logger.error(f"Error loading sitemap from file: {str(e)}")
            raise

    def filter_urls(self, urls: List[str], base_url: Optional[str] = None,
                   include_patterns: Optional[List[str]] = None,
                   exclude_patterns: Optional[List[str]] = None) -> List[str]:
        """
        Filter URLs from the sitemap based on patterns.

        Args:
            urls: List of URLs to filter
            base_url: Base URL to restrict to (optional)
            include_patterns: URL patterns to include (optional)
            exclude_patterns: URL patterns to exclude (optional)

        Returns:
            Filtered list of URLs
        """
        filtered_urls = []

        for url in urls:
            # Skip empty URLs
            if not url:
                continue

            # Check if URL belongs to base domain
            if base_url and not url.startswith(base_url):
                continue

            # Check include patterns
            if include_patterns:
                if not any(pattern in url for pattern in include_patterns):
                    continue

            # Check exclude patterns
            if exclude_patterns:
                if any(pattern in url for pattern in exclude_patterns):
                    continue

            filtered_urls.append(url)

        logger.info(f"Filtered {len(urls)} URLs down to {len(filtered_urls)} URLs")
        return filtered_urls

    def prepare_sitemap_for_testing(self, urls: List[str], output_dir: Optional[str] = None) -> Dict[str, Dict]:
        """
        Prepare a sitemap dictionary for the test generator.

        Args:
            urls: List of URLs to include in the sitemap
            output_dir: Directory to save prepared sitemap data

        Returns:
            Dictionary mapping URLs to their metadata
        """
        output_dir = output_dir or self.config.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)

        sitemap = {}
        timestamp = datetime.now().strftime("%Y-%m-%d")

        for url in urls:
            # Create a safe filename from URL
            safe_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            if not safe_filename:
                safe_filename = "index"

            # Extract page title from URL (as placeholder)
            path = urllib.parse.urlparse(url).path
            page_title = path.strip('/').split('/')[-1].replace('-', ' ').replace('_', ' ').title()
            if not page_title:
                page_title = "Home Page"

            sitemap[url] = {
                "url": url,
                "title": page_title,
                "lastmod": timestamp,
                "changefreq": "weekly"
            }

        # Save the prepared sitemap
        sitemap_path = os.path.join(output_dir, "prepared_sitemap.json")
        import json
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            json.dump(sitemap, f, indent=2)

        logger.info(f"Prepared sitemap with {len(sitemap)} URLs, saved to {sitemap_path}")
        return sitemap
