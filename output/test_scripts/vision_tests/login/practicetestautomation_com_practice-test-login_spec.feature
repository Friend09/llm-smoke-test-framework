
Feature: Test Login Functionality

  Scenario: Verify Page Title
    Given I open the login page
    Then the page title should be "Test Login | Practice Test Automation"

  Scenario: Verify Username Input Field
    Given I open the login page
    Then the username input field should be present and enabled

  Scenario: Submit Form with Empty Fields
    Given I open the login page
    When I click the "Submit" button
    Then I should see an error message for empty username and password fields

  Scenario: Submit Form with Invalid Credentials
    Given I open the login page
    When I enter a valid username and an incorrect password
    And I click the "Submit" button
    Then I should see an error message for incorrect credentials

  Scenario: Submit Form with Valid Credentials
    Given I open the login page
    When I enter a valid username and a valid password
    And I click the "Submit" button
    Then I should see a success message

  Scenario: Test Navigation Menu
    Given I open the login page
    When I click the "Toggle Navigation" button
    Then the navigation menu should expand or collapse
