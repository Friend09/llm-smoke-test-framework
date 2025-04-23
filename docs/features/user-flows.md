# User Flow Integration

User flows are a powerful feature of the LLM Smoke Test Framework that allow you to incorporate real user interactions into your test generation.

## What Are User Flows?

User flows are recorded sequences of interactions that represent how real users navigate through your application. By incorporating these flows into the test generation process, the framework can create more realistic and valuable tests.

## Benefits of User Flows

- **Realistic Scenarios**: Tests that match real user behavior
- **Critical Path Testing**: Focus on the most important user journeys
- **Complex Interaction Support**: Handle multi-step processes like checkout flows
- **Validation Improvements**: Better assertions based on expected outcomes
- **Authentication Support**: Test protected areas of your application

## User Flow Format

User flows are defined in simple text files with one action per line. The framework supports various actions:

```
# Example user flow for login process
type "testuser" into #username
type "password123" into #password
click #login-button
wait 2
verify text "Welcome, testuser" exists
click .dashboard-link
```

### Supported Actions

| Action | Syntax                          | Example                               |
| ------ | ------------------------------- | ------------------------------------- |
| Type   | `type "text" into selector`     | `type "user@example.com" into #email` |
| Click  | `click selector`                | `click button[type="submit"]`         |
| Select | `select "option" from selector` | `select "California" from #state`     |
| Wait   | `wait seconds`                  | `wait 2`                              |
| Verify | `verify condition`              | `verify text "Success" exists`        |
| Hover  | `hover selector`                | `hover .dropdown-menu`                |
| Clear  | `clear selector`                | `clear #search-input`                 |
| Submit | `submit selector`               | `submit form#login`                   |

## How to Use User Flows

### 1. Creating User Flows

You can create user flows manually or record them using browser extensions:

**Manually**:

1. Create a text file with the `.txt` extension
2. Write one action per line using the syntax above
3. Save the file in the `flows/` directory

**Recording** (with browser extensions):

1. Use a browser extension like Selenium IDE to record actions
2. Export the recording in a compatible format
3. Convert to the framework's user flow format (utilities provided)

### 2. Using Flows in Test Generation

Include the user flow when generating tests:

```bash
python run.py vision-e2e https://example.com/login --with-flow flows/login_flow.txt
```

### 3. Multiple Flows

You can specify multiple flows for different scenarios:

```bash
python run.py vision-e2e https://example.com/shop --with-flows flows/login_flow.txt,flows/checkout_flow.txt
```

## Advanced User Flow Features

### Conditional Actions

The framework supports conditional actions in user flows:

```
# Conditional acceptance of cookies
if exists #cookie-banner
    click #accept-cookies
endif
```

### Variables

You can use variables in your user flows:

```
# Using variables
set $username to "testuser"
type $username into #username
```

### Loops

For repetitive actions, you can use loops:

```
# Loop example
set $count to 1
repeat 3 times
    click #add-item
    wait 1
    set $count to $count + 1
endrepeat
```

## Integration with Test Generation

The framework uses the user flow information in several ways:

1. **Scenario Creation**: Generates test scenarios based on the flow
2. **Step Definition**: Creates step definitions that match the flow
3. **Validation Points**: Adds assertions at key points in the flow
4. **Page Object Integration**: Includes accessed elements in page objects

## Example

Here's an example of a user flow and the resulting test:

**User Flow (`checkout_flow.txt`):**

```
click #add-to-cart
wait 1
click #view-cart
verify text "Shopping Cart" exists
click #checkout
type "John Doe" into #name
type "john@example.com" into #email
type "123 Main St" into #address
select "United States" from #country
click #complete-order
wait 2
verify text "Order Confirmation" exists
```

**Generated Test:**

```gherkin
Feature: Checkout Process

  Scenario: Complete checkout with valid information
    Given I am on the product page
    When I click the "Add to Cart" button
    And I click the "View Cart" button
    Then I should see "Shopping Cart" on the page
    When I click the "Checkout" button
    And I enter "John Doe" in the "Name" field
    And I enter "john@example.com" in the "Email" field
    And I enter "123 Main St" in the "Address" field
    And I select "United States" from the "Country" dropdown
    And I click the "Complete Order" button
    Then I should see "Order Confirmation" on the page
```

## Best Practices

1. **Keep Flows Focused**: Each flow should test one specific user journey
2. **Include Verification Points**: Add verify steps to validate important states
3. **Use Clear Selectors**: Use IDs and unique selectors when possible
4. **Maintain Flow Library**: Build a library of reusable flows for common paths
5. **Version Control**: Keep flows in version control alongside tests
