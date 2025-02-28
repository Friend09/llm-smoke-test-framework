"""Browser session management"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import Config

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, config: Config):
        self.config = config
        self.driver = None

    def create_session(self):
        """Create and configure browser session"""
        if self.config.BROWSER.lower() == "chrome":
            options = ChromeOptions()
            for option in self.config.BROWSER_OPTIONS:
                if option:
                    options.add_argument(option)

            # Fixed initialization to avoid duplicate options argument
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(
                    ChromeDriverManager().install()
                ),
                options=options
            )
        elif self.config.BROWSER.lower() == "firefox":
            options = FirefoxOptions()
            for option in self.config.BROWSER_OPTIONS:
                if option:
                    options.add_argument(option)
            self.driver = webdriver.Firefox(
                service=webdriver.firefox.service.Service(
                    GeckoDriverManager().install()
                ),
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {self.config.BROWSER}")

        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(10)
        return self.driver

    def close_session(self):
        """Safely close browser session"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error closing browser session: {str(e)}")
            finally:
                self.driver = None
