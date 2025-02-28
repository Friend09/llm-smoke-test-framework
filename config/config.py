# config/config.py
"""1. Configuration Module"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Base application settings
    BASE_URL = os.getenv("BASE_URL", "https://example.com")

    # Authentication settings
    AUTH_TYPE = os.getenv("AUTH_TYPE", "basic")  # Options: basic, ntlm, okta
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    OKTA_URL = os.getenv("OKTA_URL")

    # Crawler settings
    MAX_DEPTH = int(os.getenv("MAX_DEPTH", 3))
    EXCLUDE_PATTERNS = os.getenv("EXCLUDE_PATTERNS", "logout,#,javascript:").split(",")
    INCLUDE_SUBDOMAINS = os.getenv("INCLUDE_SUBDOMAINS", "True").lower() == "true"

    # Selenium settings
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))

    # LLM settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # Output settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    CUCUMBER_TEMPLATE_DIR = os.getenv("CUCUMBER_TEMPLATE_DIR", "templates/cucumber")

    # Report settings
    REPORT_FORMAT = os.getenv("REPORT_FORMAT", "html")
