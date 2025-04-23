# Installation

Setting up the LLM Smoke Test Framework is straightforward. Follow these steps to get started.

## Prerequisites

Before installing the framework, ensure you have the following prerequisites:

- Python 3.8 or higher
- Chrome or Chromium browser (for web crawling)
- OpenAI API key (for LLM analysis)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/llm_smoke_test_framework.git
cd llm_smoke_test_framework
```

### 2. Install Dependencies

Install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

This will install all necessary Python packages, including:

- Selenium for web crawling
- OpenAI for LLM integration
- Pillow for image processing
- Other utility libraries

### 3. Configure Environment Variables

Create a `.env` file in the root of the project with the following variables:

```bash
OPENAI_API_KEY=your_openai_api_key
CHROME_DRIVER_PATH=/path/to/chromedriver  # Optional, auto-detected in most cases
OUTPUT_DIR=output  # Default output directory
```

Alternatively, you can set these environment variables in your system.

### 4. ChromeDriver Setup (Optional)

The framework will attempt to auto-detect and use ChromeDriver. If you have issues, you can:

1. Download the appropriate version of ChromeDriver from [the official site](https://sites.google.com/chromium.org/driver/)
2. Specify the path in the `.env` file as shown above

### 5. Verify Installation

Run a simple test to verify that the installation was successful:

```bash
python run.py --version
```

If everything is set up correctly, you should see the version information for the LLM Smoke Test Framework.

## Next Steps

After installation, you're ready to start using the framework:

- Check out the [Quick Start Guide](quick-start.md) for a basic example
- Explore the [Usage Examples](usage-examples.md) for more detailed use cases
- Review the [Command Reference](command-reference.md) for all available options

If you encounter any issues during installation, please see the Troubleshooting section or submit an issue on GitHub.
