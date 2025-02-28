# Quick Start Guide

This guide will help you quickly set up and run the LLM-Enhanced Smoke Test Generator framework.

## Prerequisites

Before you begin, make sure you have:

- Python 3.9 or higher installed
- Chrome browser installed
- OpenAI API key
- A web application to test. eg: [practice-test-login](https://practicetestautomation.com/practice-test-login/)

## Step 1: Clone and Set Up

```bash
# Clone the repository
git clone git@github.com:Friend09/llm-smoke-test-framework.git
cd llm-smoke-test-generator

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Your Environment

Create a `.env` file in the root directory (or inside the config directory):

```bash
cp .env.example .env
```

Edit the `.env` file with your specific settings:

```
# Application settings
BASE_URL=https://your-application-url.com
BROWSER=chrome
HEADLESS=True

# Authentication settings
AUTH_TYPE=basic  # Options: basic, ntlm, okta
USERNAME=your_username
PASSWORD=your_password

# OpenAI API key (required)
OPENAI_API_KEY=your-openai-api-key
```

## Step 3: Run the Framework

```bash
# Run with basic settings
python runners/crawler_runner.py

# Run with additional options
python runners/crawler_runner.py --depth 3 --auth basic --headless
```

## Step 4: Review Generated Tests

Once the crawler and test generator have completed, you'll find your generated tests in the `output/test_scripts` directory:

```
output/test_scripts/
├── features/            # Cucumber feature files
├── page_objects/        # Page object implementations
└── step_definitions/    # Step definition implementations
```

## Step 5: Execute Tests

To run the generated tests, you'll need to copy them to your existing test framework or set up a new one:

### For Java/Selenium:

```bash
# Copy files to your Maven project
cp -r output/test_scripts/* path/to/your/test/project/src/test/

# Run with Maven
cd path/to/your/test/project
mvn test
```

### For TypeScript/WebdriverIO:

```bash
# Copy files to your WebdriverIO project
cp -r output/test_scripts/* path/to/your/wdio/project/

# Run with WebdriverIO
cd path/to/your/wdio/project
npx wdio run wdio.conf.ts
```

## Troubleshooting

### Common Issues

1. **Authentication fails**

   - Check your credentials in the `.env` file
   - Check if your `.env` file is at the root directory or inside the `./config` directory
   - Verify the authentication method is correct

2. **No pages discovered**

   - Check if the start URL is accessible
   - Try increasing the timeout values in `.env`

3. **LLM errors**
   - Verify your OpenAI API key is valid
   - Verify if you need to add a base url, api_version, etc if using Azure OpenAI
   - Check your internet connection, SSL certificate issues

For more detailed information, check the [README.md](../README.md) file and full documentation.
