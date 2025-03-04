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

    # OpenAI API settings
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.environ.get("LLM_MODEL", "gpt-4o-mini")
    LLM_TEMPERATURE: float = float(os.environ.get("LLM_TEMPERATURE", "0.0"))
    LLM_MAX_TOKENS: int = int(os.environ.get("LLM_MAX_TOKENS", "2000"))

    # Crawler settings
    CHROME_DRIVER_PATH: Optional[str] = os.environ.get("CHROME_DRIVER_PATH")
    HEADLESS: bool = os.environ.get("HEADLESS", "True").lower() == "true"
    PAGE_LOAD_TIMEOUT: int = int(os.environ.get("PAGE_LOAD_TIMEOUT", "30"))

    # Output settings
    OUTPUT_DIR: str = os.environ.get("OUTPUT_DIR", "output")
    PAGE_DATA_DIR: str = os.environ.get("PAGE_DATA_DIR", "page_data")
    ANALYSIS_DIR: str = os.environ.get("ANALYSIS_DIR", "analysis")
    TEST_SCRIPTS_DIR: str = os.environ.get("TEST_SCRIPTS_DIR", "test_scripts")

    def validate(self) -> bool:
        """Validate the configuration settings."""
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")

        # Create output directories if they don't exist
        for dir_name in [self.OUTPUT_DIR,
                         f"{self.OUTPUT_DIR}/{self.PAGE_DATA_DIR}",
                         f"{self.OUTPUT_DIR}/{self.ANALYSIS_DIR}",
                         f"{self.OUTPUT_DIR}/{self.TEST_SCRIPTS_DIR}"]:
            os.makedirs(dir_name, exist_ok=True)

        return True

    @property
    def page_data_path(self) -> str:
        return f"{self.OUTPUT_DIR}/{self.PAGE_DATA_DIR}"

    @property
    def analysis_path(self) -> str:
        return f"{self.OUTPUT_DIR}/{self.ANALYSIS_DIR}"

    @property
    def test_scripts_path(self) -> str:
        return f"{self.OUTPUT_DIR}/{self.TEST_SCRIPTS_DIR}"
