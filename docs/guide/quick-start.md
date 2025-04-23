# Quick Start

This guide will help you get up and running with the LLM Smoke Test Framework quickly.

## Basic Usage

After [installing](installation.md) the framework, you can start generating smoke tests with just a few commands.

### 1. Simple Single-Page Test Generation

To analyze a single page and generate tests:

```bash
python run.py vision-e2e https://example.com/login --language java
```

This command:

1. Crawls the specified URL
2. Captures a screenshot
3. Analyzes the page using both DOM and vision capabilities
4. Generates Cucumber feature files and step definitions

### 2. Check Your Output

The generated test scripts will be in the `output` directory (or the directory specified in your `.env` file):

```
output/
├── analysis/           # Analysis results in JSON format
├── page_data/          # Raw page data
├── screenshots/        # Screenshots used for vision analysis
└── test_scripts/       # Your generated test scripts
```

### 3. Execute the Generated Tests

The generated tests are ready to use with popular test runners. For Cucumber Java tests:

1. Copy the tests to your test project
2. Install dependencies (Selenium, Cucumber)
3. Run with your preferred test runner

## Example Output

Here's an example of what a generated Cucumber feature file might look like:

```gherkin
Feature: Login Page Tests

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "testuser" in the username field
    And I enter "password123" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see a welcome message

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter "invaliduser" in the username field
    And I enter "wrongpassword" in the password field
    And I click the "Login" button
    Then I should see an error message
    And I should remain on the login page
```

## Next Steps

Now that you've run your first test generation, you can explore more advanced features:

- Learn about [User Flow Integration](../features/user-flows.md) to capture real user interactions
- Try [Site-Wide Testing](../features/site-wide-testing.md) to generate tests for entire websites
- Explore [Vision Analysis](../features/vision-analysis.md) for better visual element detection
- Check the [Command Reference](command-reference.md) for all available options
