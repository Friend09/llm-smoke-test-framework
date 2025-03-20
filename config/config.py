# config/config.py
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    """Configuration for the LLM Smoke Test Framework."""

    # Crawler settings
    HEADLESS: bool = True
    PAGE_LOAD_TIMEOUT: int = 30
    CAPTURE_SCREENSHOTS: bool = True
    ANALYZE_LAYOUT: bool = True
    CHROME_DRIVER_PATH: Optional[str] = None

    # Output settings
    OUTPUT_DIR: str = "output"
    BASE_URL: str = ""  # Base URL for the application under test

    # LLM settings
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"  # Using non-vision model
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 500  # Further reduced for split analysis
    LLM_MAX_CONTEXT: int = 8000  # Maximum context size for mini model
    VISUAL_ANALYSIS_TOKENS: int = 300  # Specific limit for visual analysis

    # Screenshot optimization settings
    SCREENSHOT_MAX_DIMENSION: int = 1280  # Maximum dimension in pixels
    SCREENSHOT_QUALITY: int = 75  # JPEG quality (1-100)

    # Add a parameter to organize files by site
    ORGANIZE_BY_SITE: bool = os.getenv("ORGANIZE_BY_SITE", "True").lower() == "true"

    def __post_init__(self):
        """Load configuration from environment variables."""
        # Load from environment variables
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", self.OPENAI_API_KEY)
        self.CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", self.CHROME_DRIVER_PATH)
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", self.OUTPUT_DIR)
        self.BASE_URL = os.getenv("BASE_URL", self.BASE_URL)
        self.LLM_MODEL = os.getenv("LLM_MODEL", self.LLM_MODEL)
        self.LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", str(self.LLM_TEMPERATURE)))
        self.LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", str(self.LLM_MAX_TOKENS)))

        # Create output directories
        self._create_output_directories()

        self.validate()

    def validate(self):
        """Validate configuration."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set")

    def _create_output_directories(self):
        """Create all required output directories."""
        directories = {
            "page_data_path": os.path.join(self.OUTPUT_DIR, "page_data"),
            "analysis_path": os.path.join(self.OUTPUT_DIR, "analysis"),
            "test_scripts_path": os.path.join(self.OUTPUT_DIR, "test_scripts"),
            "screenshots_path": os.path.join(self.OUTPUT_DIR, "screenshots")
        }

        for path in directories.values():
            os.makedirs(path, exist_ok=True)

        # Add directory paths as properties
        for name, path in directories.items():
            setattr(self, name, path)
