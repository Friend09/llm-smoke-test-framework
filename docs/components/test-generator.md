# Test Generator

The Test Generator is a core component of the LLM Smoke Test Framework responsible for creating test scripts based on the analysis of web pages.

## Overview

The `TestGenerator` class transforms analysis results from the LLM Analyzer into executable test scripts. It generates human-readable, maintainable test scripts in various formats and languages, with a focus on Cucumber-style behavior-driven development (BDD) tests.

## Features

- **Multiple Output Languages**: Generates tests in Java, Python, or JavaScript/TypeScript
- **BDD Format**: Creates Cucumber feature files with Gherkin syntax
- **Page Object Pattern**: Implements the Page Object pattern for maintainable tests
- **Realistic Scenarios**: Generates realistic test scenarios based on page functionality
- **Detailed Assertions**: Includes appropriate assertions for each scenario
- **Extensible Structure**: Pluggable architecture for supporting additional test frameworks

## Usage

The Test Generator can be used directly or through the framework's main commands:

```python
from core.test_generator import TestGenerator
from core.llm_analyzer import AnalysisResult

# Initialize the generator
generator = TestGenerator(language="java", framework="cucumber")

# Generate tests from analysis result
analysis_result = analyzer.analyze(page_data)
test_files = generator.generate(analysis_result)

# Write the test files to disk
generator.write_to_disk(test_files, output_dir="output/test_scripts")
```

## Configuration Options

The Test Generator behavior can be customized through several options:

| Option                  | Description                     | Default               |
| ----------------------- | ------------------------------- | --------------------- |
| `language`              | Target language for tests       | `java`                |
| `framework`             | Test framework to use           | `cucumber`            |
| `scenarios_per_page`    | Number of scenarios to generate | `3`                   |
| `include_assertions`    | Include detailed assertions     | `True`                |
| `generate_page_objects` | Use Page Object pattern         | `True`                |
| `output_dir`            | Output directory for test files | `output/test_scripts` |

## Generated Files

The Test Generator produces multiple types of files:

### 1. Feature Files

Cucumber feature files containing test scenarios in Gherkin syntax:

```gherkin
Feature: Login Page Tests

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "testuser" in the username field
    And I enter "password123" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see a welcome message
```

### 2. Step Definition Files

Implementation of the steps defined in feature files:

```java
// Java example
public class LoginSteps {
    private LoginPage loginPage;
    private WebDriver driver;

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        driver = new ChromeDriver();
        driver.get("https://example.com/login");
        loginPage = new LoginPage(driver);
    }

    @When("I enter {string} in the username field")
    public void iEnterInTheUsernameField(String username) {
        loginPage.enterUsername(username);
    }

    // More step implementations...
}
```

### 3. Page Object Files

Page Object classes for better test maintainability:

```java
// Java example
public class LoginPage {
    private WebDriver driver;

    // Element locators
    private By usernameField = By.id("username");
    private By passwordField = By.id("password");
    private By loginButton = By.id("login-button");

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void enterUsername(String username) {
        driver.findElement(usernameField).sendKeys(username);
    }

    public void enterPassword(String password) {
        driver.findElement(passwordField).sendKeys(password);
    }

    public void clickLoginButton() {
        driver.findElement(loginButton).click();
    }

    // More page methods...
}
```

## Supported Languages and Frameworks

The Test Generator currently supports the following combinations:

| Language              | Frameworks        |
| --------------------- | ----------------- |
| Java                  | Cucumber, JUnit   |
| Python                | Behave, Pytest    |
| JavaScript/TypeScript | Cucumber-JS, Jest |

## Advanced Usage

### Custom Templates

You can customize the generated code by providing custom templates:

```python
# Custom templates
templates = {
    "feature": "/path/to/custom/feature.template",
    "step_definitions": "/path/to/custom/steps.template",
    "page_object": "/path/to/custom/page_object.template"
}

generator = TestGenerator(language="java", templates=templates)
```

### Integrating with User Flows

When user flows are available, the Test Generator can create tests that follow these flows:

```python
# With user flow
generator = TestGenerator(language="java")
test_files = generator.generate_with_flow(analysis_result, user_flow)
```

### Batch Generation

For generating tests for multiple pages efficiently:

```python
# Batch generation
generator = TestGenerator(language="java")
test_files = generator.generate_batch(analysis_results_list)
```

## Test Generation Process

1. **Analysis Interpretation**: The generator interprets the analysis results
2. **Scenario Selection**: It selects the most valuable test scenarios
3. **Step Creation**: Steps are created for each scenario
4. **Assertion Addition**: Appropriate assertions are added
5. **Element Mapping**: Page elements are mapped to locators
6. **Code Generation**: Code is generated using templates
7. **File Organization**: Files are organized in a structured layout

## Best Practices

1. **Review Generated Tests**: Always review and potentially refine generated tests
2. **Maintain Page Objects**: Update page objects as your UI changes
3. **Add Custom Assertions**: Add custom assertions for business-specific validations
4. **Integrate with CI/CD**: Run the generated tests in your CI/CD pipeline
5. **Version Control**: Keep the generated tests in version control
