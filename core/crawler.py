# core/crawler.py
import json
import logging
import os
from typing import Dict, Any, Set
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import traceback
import time

logger = logging.getLogger(__name__)

load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
SCREENSHOT_DIR = os.path.join(OUTPUT_DIR, "screenshots")
PAGE_DATA_DIR = os.path.join(OUTPUT_DIR, "page_data")

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(PAGE_DATA_DIR, exist_ok=True)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

class PlaywrightCrawler:
    def __init__(self, base_url: str, max_pages: int = 100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited: Set[str] = set()
        self.page_data: Dict[str, Any] = {}
        self.to_visit = [base_url]

    async def _extract_links(self, page) -> Set[str]:
        links = set(await page.eval_on_selector_all(
            "a[href]", "elements => elements.map(e => e.href)"
        ))
        nav_selectors = [
            '[role="menu"]', '[role="navigation"]', '[role="tablist"]',
            'nav', '.menu', '.navbar', '.nav', '.sidebar', '.tabs', '.tab',
            'button', '[aria-expanded="false"]', '[aria-haspopup]'
        ]
        for selector in nav_selectors:
            elements = await page.query_selector_all(selector)
            for el in elements:
                try:
                    await el.click(timeout=1000)
                except Exception:
                    continue
        links.update(set(await page.eval_on_selector_all(
            "a[href]", "elements => elements.map(e => e.href)"
        )))
        return links

    async def _extract_page_data(self, page, url: str, screenshot: bool = True) -> Dict[str, Any]:
        screenshot_path = os.path.join(SCREENSHOT_DIR, self._safe_filename(url) + ".png")
        if screenshot:
            try:
                await page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"Screenshot captured for {url}: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot for {url}: {e}")
                screenshot_path = None
        dom = await page.content()
        title = await page.title()
        logger.info(f"Extracted title for {url}: {title}")
        forms = await page.eval_on_selector_all(
            "form", "forms => forms.map(f => ({id: f.id, name: f.name, action: f.action, method: f.method}))"
        )
        headings = []
        for h in range(1, 7):
            hs = await page.eval_on_selector_all(
                f"h{h}", f"els => els.map(e => e.textContent.trim())"
            )
            for text in hs:
                if text:
                    headings.append({"level": h, "text": text})
        data = {
            "url": url,
            "title": title,
            "screenshot_path": screenshot_path,
            "html_content": dom[:100000],
            "forms": forms,
            "headings": headings,
        }
        logger.info(f"Page data added for {url}")
        page_data_path = os.path.join(PAGE_DATA_DIR, self._safe_filename(url) + ".json")
        with open(page_data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data

    def _safe_filename(self, url: str) -> str:
        return url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")

    async def _handle_login(self, page) -> bool:
        username_selector = 'input[type="text"], input[type="email"], input[name*="user" i], input[name*="email" i]'
        password_selector = 'input[type="password"], input[name*="pass" i]'
        login_button_selector = 'button[type="submit"], input[type="submit"], button, [role="button"]'
        username = USERNAME
        password = PASSWORD
        if not username or not password:
            return False
        try:
            user_input = await page.query_selector(username_selector)
            pass_input = await page.query_selector(password_selector)
            if user_input and pass_input:
                await user_input.fill(username)
                await pass_input.fill(password)
                login_btn = await page.query_selector(login_button_selector)
                if login_btn:
                    await login_btn.click()
                else:
                    await pass_input.press('Enter')
                await page.wait_for_load_state('networkidle', timeout=5000)
                return True
        except Exception:
            pass
        return False

    async def crawl(self, single_page_only=False, enable_tracing=False):
        """
        Crawl the website starting from base_url.
        If single_page_only is True, only visit the initial page and return its data.
        Returns a dict: {url: page_data}
        """
        results = {}
        trace_path = None
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            tracing_started = False
            page = await context.new_page()
            try:
                logger.info(f"About to visit site: {self.base_url}")
                await page.goto(self.base_url)
                logger.info(f"Visited site: {self.base_url}")
                page_data = await self._extract_page_data(page, self.base_url)
                results[self.base_url] = page_data
                if single_page_only:
                    await browser.close()
                    return results
                # Otherwise, crawl all reachable pages (up to max_pages)
                to_visit = [self.base_url]
                visited = set()
                while to_visit and len(results) < self.max_pages:
                    url = to_visit.pop(0)
                    if url in visited:
                        logger.info(f"Skipping already visited URL: {url}")
                        continue
                    try:
                        logger.info(f"About to visit page: {url} (crawled {len(results)}/{self.max_pages})")
                        await page.goto(url, timeout=60000)
                        logger.info(f"Visited page: {url}")
                        page_data = await self._extract_page_data(page, url)
                        results[url] = page_data
                        visited.add(url)
                        # Extract links to follow
                        links = await page.eval_on_selector_all('a', 'elements => elements.map(e => e.href)')
                        for link in links:
                            if link.startswith(self.base_url) and link not in visited and link not in to_visit:
                                to_visit.append(link)
                    except Exception as e:
                        logger.error(f"Error visiting {url}: {e}")
                        # Start tracing if not already started and enabled
                        if enable_tracing and not tracing_started:
                            await context.tracing.start(screenshots=True, snapshots=True, sources=True)
                            tracing_started = True
                            logger.info("Playwright tracing started due to error.")
                        # Save error page HTML for later analysis
                        try:
                            error_html = await page.content()
                            error_file = os.path.join(PAGE_DATA_DIR, self._safe_filename(url) + "_error.html")
                            with open(error_file, "w", encoding="utf-8") as f:
                                f.write(error_html)
                            logger.info(f"Saved error page HTML for {url} to {error_file}")
                        except Exception as html_e:
                            logger.error(f"Failed to save error HTML for {url}: {html_e}")
                        logger.debug(traceback.format_exc())
                        continue
                # Stop tracing if it was started
                if tracing_started:
                    trace_path = f"playwright_trace_{int(time.time())}.zip"
                    await context.tracing.stop(path=trace_path)
                    logger.info(f"Playwright trace saved to {trace_path}")
                await browser.close()
            except KeyboardInterrupt:
                logger.warning("Crawl interrupted by user. Cleaning up...")
                if tracing_started:
                    trace_path = f"playwright_trace_{int(time.time())}.zip"
                    await context.tracing.stop(path=trace_path)
                    logger.info(f"Playwright trace saved to {trace_path}")
                await browser.close()
                raise
        return results
