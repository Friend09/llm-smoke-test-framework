# LLM Analyzer

The LLM Analyzer is a core component of the framework responsible for analyzing web pages using Large Language Models and generating test scenarios.

## Overview

The `LLMAnalyzer` class processes page data extracted by the WebCrawler to identify key elements, understand page structure, and suggest test scenarios. It uses OpenAI's models for both text-based and vision-based analysis.

## Key Features

- **DOM Analysis**: Analyzes page structure based on HTML elements
- **Vision Analysis**: Uses GPT-4o-mini vision capabilities to analyze screenshots
- **Test Scenario Generation**: Identifies potential test scenarios based on page functionality
- **User Flow Integration**: Incorporates recorded user interactions into analysis
- **Comprehensive Test Prompting**: Creates detailed prompts with examples and formatting guidance

## Usage

```python
from core.llm_analyzer import LLMAnalyzer
from config.config import Config

# Initialize the analyzer
config = Config()
analyzer = LLMAnalyzer(config)

# Analyze a page
analysis = analyzer.analyze_page(page_data)

# Generate test script
test_script = analyzer.generate_test_script(analysis, framework="cucumber", language="java")
```

## Methods

### `analyze_page(page_data)`

Analyzes page data to identify key elements for testing.

```python
analysis = analyzer.analyze_page(page_data)
```

### `analyze_page_with_vision(page_data)`

Enhanced analysis using vision capabilities with screenshots.

```python
analysis = analyzer.analyze_page_with_vision(page_data)
```

### `generate_test_script(page_analysis, framework="cucumber", language="java")`

Generates test scripts based on page analysis.

```python
test_script = analyzer.generate_test_script(page_analysis, framework="cucumber", language="java")
```

### `generate_test_script_raw(page_analysis, framework="cucumber", language="java")`

Generates test scripts and returns the raw LLM response without JSON parsing.

```python
raw_response = analyzer.generate_test_script_raw(page_analysis, framework="cucumber", language="java")
```

### `generate_test_script_with_retry(page_analysis, framework="cucumber", language="java", max_retries=2)`

Generates test scripts with retry logic to handle potential errors.

```python
test_script = analyzer.generate_test_script_with_retry(page_analysis, framework="cucumber", language="java")
```

## Test Generation Prompting

The `_format_test_generation_prompt` method creates comprehensive prompts for the LLM that include:

1. **Examples of well-formed feature files** - Demonstrates proper Gherkin syntax
2. **Examples of step definitions** - Shows how steps should be implemented
3. **Context from page analysis** - Provides key elements, identifiers, and layout details
4. **User flow information** - Includes recorded user interactions when available
5. **Detailed guidelines** - Instructions for test quality and best practices
6. **Formatting instructions** - Ensures proper output structure

The prompt features sections for:

- URL and title information
- Page analysis summary
- Verified user interactions (from recorded flows)
- Unique page identifiers
- Key interactive elements
- Recommended test scenarios
- Suggested smoke test steps
- Locator strategies for elements

This comprehensive prompting approach ensures high-quality test generation with realistic scenarios based on actual page functionality and user behavior.

## Vision Analysis

When vision capabilities are enabled, the LLM Analyzer uses a multi-step process:

1. **Screenshot Optimization** - Prepares the screenshot for API submission
2. **Visual Element Detection** - Identifies elements visible in the UI
3. **Layout Understanding** - Analyzes the visual structure of the page
4. **DOM Integration** - Combines visual insights with DOM-based analysis

## Performance Optimization

To optimize LLM Analyzer performance:

1. Use caching for repeated analysis
2. Optimize screenshot quality for vision analysis
3. Use more efficient models for initial analysis
4. Implement batch processing for multiple pages

## Error Handling

The LLM Analyzer includes robust error handling:

```python
try:
    result = analyzer.analyze(page_data)
except APIKeyException:
    print("Invalid or missing OpenAI API key")
except APIQuotaException:
    print("OpenAI API quota exceeded")
except InvalidResponseException as e:
    print(f"Invalid response from LLM: {str(e)}")
except AnalysisException as e:
    print(f"Analysis error: {str(e)}")
```
