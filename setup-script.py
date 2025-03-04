#!/usr/bin/env python3
"""
Setup script to create the directory structure for LLM Smoke Test Framework.
This script creates the directory structure and starter files for the project.
"""

import os
import sys

def create_directory_structure():
    """Create the directory structure for the LLM Smoke Test Framework."""

    # Main directories
    directories = [
        'config',
        'core',
        'output/page_data',
        'output/analysis',
        'output/test_scripts',
        'tests/unit',
        'tests/integration',
        'docs',
        '.github/workflows',
        '.github/ISSUE_TEMPLATE'
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

    # Create __init__.py files for Python packages
    init_files = [
        'config/__init__.py',
        'core/__init__.py',
        'tests/__init__.py',
        'tests/unit/__init__.py',
        'tests/integration/__init__.py'
    ]

    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write("# Package initialization\n")
        print(f"Created file: {init_file}")

    # Create template for config.py
    config_content = """
# config/config.py
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    \"\"\"Configuration for the LLM Smoke Test Framework.\"\"\"

    # OpenAI API settings
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
    LLM_TEMPERATURE: float = float(os.environ.get("LLM_TEMPERATURE", "0.2"))
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
        \"\"\"Validate the configuration settings.\"\"\"
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
"""

    # Create template for .env file
    env_content = """# OpenAI API settings
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-40-mini
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=2000

# Crawler settings
HEADLESS=True
PAGE_LOAD_TIMEOUT=30

# Output settings
OUTPUT_DIR=output
"""

    # Create template for requirements.txt
    requirements_content = """langchain==0.1.7
langchain-openai==0.0.5
openai==1.12.0
selenium==4.17.2
python-dotenv==1.0.0
webdriver-manager==4.0.1
"""

    # Create core files with templates
    core_files = {
        'config/config.py': config_content,
        'core/crawler.py': "# core/crawler.py - Web crawler for extracting page data\n",
        'core/llm_analyzer.py': "# core/llm_analyzer.py - LLM-based analyzer for generating test recommendations\n",
        'run.py': "#!/usr/bin/env python3\n# Main entry point for the LLM Smoke Test Framework\n",
        '.env.example': env_content,
        'requirements.txt': requirements_content,
        'tests/unit/test_llm_analyzer.py': "# tests/unit/test_llm_analyzer.py - Unit tests for LLM analyzer\n",
        'tests/integration/test_end_to_end.py': "# tests/integration/test_end_to_end.py - Integration tests for the full pipeline\n"
    }

    for file_path, content in core_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created file: {file_path}")

    # Create documentation files
    doc_files = [
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        '.github/ISSUE_TEMPLATE/bug_report.md',
        '.github/ISSUE_TEMPLATE/feature_request.md',
        '.github/workflows/python-tests.yml',
        '.gitignore',
    ]

    for file in doc_files:
        with open(file, 'w') as f:
            f.write(f"# {file} - Add your content here\n")
        print(f"Created file: {file}")

    # Create a .gitignore file with common Python ignores
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
env/
ENV/

# Environment variables
.env

# IDE files
.idea/
.vscode/

# Test coverage
.coverage
htmlcov/

# Output directories (but keep the structure)
output/*
!output/page_data/.gitkeep
!output/analysis/.gitkeep
!output/test_scripts/.gitkeep

# Logs
*.log
"""

    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)

    # Create .gitkeep files to preserve empty directories
    for dir_path in ['output/page_data', 'output/analysis', 'output/test_scripts']:
        with open(f"{dir_path}/.gitkeep", 'w') as f:
            pass
        print(f"Created file: {dir_path}/.gitkeep")

    # Make run.py executable
    os.chmod('run.py', 0o755)

    print("\nLLM Smoke Test Framework structure created successfully!")
    print("Next steps:")
    print("1. Create a virtualenv: python -m venv venv")
    print("2. Activate it: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Copy .env.example to .env and add your OpenAI API key")
    print("5. Run the framework: python run.py e2e https://example.com")

if __name__ == "__main__":
    create_directory_structure()
