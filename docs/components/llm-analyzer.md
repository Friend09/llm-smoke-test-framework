# LLM Analyzer

The LLM Analyzer component uses Large Language Models to analyze web pages and identify test scenarios.

## Overview

The `LLMAnalyzer` class processes page data extracted by the Web Crawler, using OpenAI models to understand page structure, functionality, and identify testing opportunities. It combines traditional DOM analysis with vision-based analysis for a comprehensive understanding of the page.

## Features

- **Multi-modal Analysis**: Combines DOM analysis with vision capabilities
- **Page Classification**: Automatically detects page types (login, form, landing, etc.)
- **Element Identification**: Identifies interactive elements and their purpose
- **Test Scenario Detection**: Suggests relevant test scenarios for each page
- **User Flow Understanding**: Interprets and incorporates user flows
- **Context Awareness**: Maintains context between related pages

## Usage

The LLM Analyzer can be used directly or through the framework's main commands:

```python
from core.llm_analyzer import LLMAnalyzer
from core.crawler import PageData

# Initialize the analyzer
analyzer = LLMAnalyzer()

# Analyze a page
page_data = crawler.crawl("https://example.com/login")
analysis_result = analyzer.analyze(page_data)

# Access analysis results
page_type = analysis_result.page_type
elements = analysis_result.interactive_elements
test_scenarios = analysis_result.suggested_scenarios
```

## Configuration Options

The LLM Analyzer behavior can be customized through several options:

| Option           | Description                 | Default       |
| ---------------- | --------------------------- | ------------- |
| `model`          | OpenAI model to use         | `gpt-4o-mini` |
| `vision_enabled` | Enable vision analysis      | `True`        |
| `vision_quality` | Image quality for vision    | `auto`        |
| `max_tokens`     | Maximum tokens for response | `4000`        |
| `temperature`    | Creativity level (0-1)      | `0.1`         |
| `cache_results`  | Cache analysis results      | `True`        |
| `api_key`        | OpenAI API key              | From `.env`   |

## Analysis Result Structure

When a page is analyzed, the `LLMAnalyzer` returns an `AnalysisResult` object with the following properties:

```python
class AnalysisResult:
    page_url: str              # The URL that was analyzed
    page_type: str             # Detected page type (login, form, etc.)
    interactive_elements: list # Interactive elements with details
    suggested_scenarios: list  # Suggested test scenarios
    form_fields: list          # Form fields with validation info
    buttons: list              # Buttons with actions
    links: list                # Important links on the page
    assertions: list           # Suggested assertions
    metadata: dict             # Additional analysis metadata
    timestamp: datetime        # When the analysis was performed
```

## Vision Analysis

The LLM Analyzer uses OpenAI's vision capabilities to analyze page screenshots:

```python
# Enable vision analysis
analyzer = LLMAnalyzer(vision_enabled=True, vision_quality="high")

# Analyze a page with vision
result = analyzer.analyze_with_vision(page_data)

# Vision-specific findings
visual_elements = result.visual_elements
layout_analysis = result.layout_analysis
```

## Advanced Usage

### Custom Analysis Prompts

You can customize the analysis by providing custom prompts:

```python
# Custom prompt for special page types
custom_prompt = """
Analyze this e-commerce product page and identify:
1. Product information fields
2. Add to cart functionality
3. Product image gallery behavior
4. Price display and discount calculation
"""

result = analyzer.analyze_with_custom_prompt(page_data, custom_prompt)
```

### Incorporating User Flows

The analyzer can incorporate user flows for better context:

```python
# With user flow
from core.crawler import UserFlow

flow = UserFlow.from_file("flows/checkout_flow.txt")
result = analyzer.analyze_with_user_flow(page_data, flow)

# Flow-aware results
flow_steps = result.flow_steps
critical_paths = result.critical_paths
```

### Batch Processing

For analyzing multiple pages efficiently:

```python
# Batch analysis
page_data_list = [
    crawler.crawl("https://example.com/login"),
    crawler.crawl("https://example.com/register"),
    crawler.crawl("https://example.com/checkout")
]

results = analyzer.analyze_batch(page_data_list)
```

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
