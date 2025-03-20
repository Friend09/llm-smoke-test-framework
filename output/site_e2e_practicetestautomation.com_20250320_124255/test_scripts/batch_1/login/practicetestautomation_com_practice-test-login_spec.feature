@login

Feature: Smoke Tests for Test Login Page

  Scenario: Verify Page Title
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    Then user verifies page title is "Test Login | Practice Test Automation"

  Scenario: Positive Login Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "student" into the username field
    And user enters "Password123" into the password field
    And user clicks the submit button
    Then user should see a successful login message

  Scenario: Negative Login Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "invalidUser" into the username field
    And user enters "invalidPassword" into the password field
    And user clicks the submit button
    Then user should see an error message

  Scenario: Empty Fields Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user clicks the submit button without entering credentials
    Then user should see error messages for empty fields

  Scenario: Focus and Blur Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user focuses on the username field
    Then the username field should be active
    When user shifts focus to the password field
    Then the password field should be active