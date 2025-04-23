# Architecture Overview

This document provides an overview of the LLM Smoke Test Framework architecture and how the different components interact with each other.

## High-Level Architecture

The LLM Smoke Test Framework is designed with a modular architecture that separates concerns and allows for flexibility in implementation. The main components are:

![Architecture Diagram](../assets/architecture.png)

## Core Components

### WebCrawler

The WebCrawler is responsible for extracting page data from websites. It:

- Loads web pages using Selenium WebDriver
- Extracts DOM structure and page metadata
- Captures screenshots for vision analysis
- Handles navigation and page interactions

### LLM Analyzer

The LLM Analyzer processes the extracted page data using Large Language Models. It:

- Analyzes DOM structure to identify interactive elements
- Uses vision capabilities to understand page layout and visual elements
- Classifies page types (login, form, landing, etc.)
- Identifies test scenarios based on page functionality

### Test Generator

The Test Generator creates test scripts based on the analysis results. It:

- Generates Cucumber feature files with realistic scenarios
- Creates step definitions for test implementation
- Builds page object classes for better maintainability
- Tailors tests to specific page types and functionality

### Sitemap Crawler

The Sitemap Crawler discovers and maps website structure. It:

- Crawls websites to discover linked pages
- Builds a site map with page relationships
- Filters pages based on patterns and crawl depth
- Provides a structured representation of the website

## Data Flow

1. **Input**: URL or sitemap
2. **Crawling**: Extract page data, DOM, and screenshots
3. **Analysis**: Process data with LLM to understand page functionality
4. **Generation**: Create test scripts based on analysis
5. **Output**: Structured test files in the specified format

## Integration Points

The framework integrates with several external technologies:

- **Selenium WebDriver**: For browser automation and page interaction
- **OpenAI API**: For LLM-powered analysis and generation
- **Cucumber**: For behavior-driven test script format
- **Various Test Frameworks**: For implementing the generated tests

## Configuration System

The framework uses a layered configuration approach:

- **Environment Variables**: For system-wide settings
- **Configuration Files**: For project-specific settings
- **Command-Line Arguments**: For run-specific options

This hierarchy allows for flexible configuration while maintaining sensible defaults.

## Extension Points

The framework is designed to be extensible in several ways:

1. **Custom Analyzers**: Implement custom analysis strategies
2. **Additional Test Frameworks**: Support new test framework outputs
3. **Integration Plugins**: Connect with test management systems
4. **Custom Crawlers**: Implement specialized crawling strategies

## Technical Stack

- **Python**: Primary implementation language
- **Selenium**: For web interaction
- **OpenAI API**: For LLM integration
- **Various Output Languages**: Java, Python, JavaScript/TypeScript

## Class Diagram

```
┌────────────────┐       ┌───────────────┐       ┌─────────────────┐
│  WebCrawler    │──────▶│  LLMAnalyzer  │──────▶│  TestGenerator  │
└────────────────┘       └───────────────┘       └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
┌────────────────┐       ┌───────────────┐       ┌─────────────────┐
│   PageData     │       │AnalysisResult │       │  TestScript     │
└────────────────┘       └───────────────┘       └─────────────────┘
        ▲                        ▲                        ▲
        │                        │                        │
        │                        │                        │
┌────────────────┐       ┌───────────────┐       ┌─────────────────┐
│SitemapCrawler  │       │ Config         │       │OutputFormatter  │
└────────────────┘       └───────────────┘       └─────────────────┘
```

## Performance Considerations

The framework includes several optimizations:

- **Caching**: Analysis results are cached to avoid redundant API calls
- **Parallel Processing**: Site-wide generation can be parallelized
- **Batching**: Large sites are processed in batches
- **Image Optimization**: Screenshots are optimized for vision analysis

For more detailed information on each component, refer to their respective documentation pages.
