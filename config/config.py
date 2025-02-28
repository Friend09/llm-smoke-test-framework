"""Configuration Module for LLM-Enhanced Test Generator"""

import os
from typing import List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # Application settings
    BASE_URL: str = os.getenv("BASE_URL", "")
    APP_NAME: str = os.getenv("APP_NAME", "web_app")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"

    # Authentication settings
    AUTH_TYPE: str = os.getenv("AUTH_TYPE", "none")
    USERNAME: str = os.getenv("USERNAME", "")
    PASSWORD: str = os.getenv("PASSWORD", "")
    AUTH_CONFIG: dict = field(default_factory=lambda: {
        "username": os.getenv("USERNAME", ""),
        "password": os.getenv("PASSWORD", ""),
        "token_url": os.getenv("TOKEN_URL", ""),
        "client_id": os.getenv("CLIENT_ID", ""),
        "client_secret": os.getenv("CLIENT_SECRET", ""),
    })

    # LLM settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))

    # Crawler settings
    MAX_DEPTH: int = int(os.getenv("MAX_DEPTH", "3"))
    EXCLUDE_PATTERNS: List[str] = field(
        default_factory=lambda: os.getenv("EXCLUDE_PATTERNS", "logout,#,javascript:").split(",")
    )
    INCLUDE_SUBDOMAINS: bool = os.getenv("INCLUDE_SUBDOMAINS", "False").lower() == "true"
    REQUEST_DELAY: float = float(os.getenv("REQUEST_DELAY", "0.5"))

    # Browser settings
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() == "true"
    IMPLICIT_WAIT: int = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT: int = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    BROWSER_OPTIONS: List[str] = field(default_factory=lambda: [
        "--headless" if os.getenv("HEADLESS", "True").lower() == "true" else "",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920,1080"
    ])

    def validate(self) -> bool:
        """Validate required configuration settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for test generation")
        if not self.BASE_URL:
            raise ValueError("BASE_URL is required")
        return True
