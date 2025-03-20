@login

Feature: Smoke Testing for Practice Test Login Page

  Scenario: Verify Page Title and URL
    Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
    Then user verifies page title is "Test Login | Practice Test Automation"

  Scenario: Verify Input Fields and Buttons
    Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
    Then user verifies the username input field is present
    And user verifies the submit button is visible
    And user verifies the toggle navigation button is visible

  Scenario: Test Username Input
    Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "testuser" into the username field
    Then user verifies that the username input is accepted
  