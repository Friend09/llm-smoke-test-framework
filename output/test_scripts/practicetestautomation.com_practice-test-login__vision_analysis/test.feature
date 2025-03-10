
Feature: Test Login Functionality

  Scenario: Verify Page Title
    Given I navigate to the login page
    Then the page title should be "Test Login | Practice Test Automation"

  Scenario: Verify Username Input Field Acceptance
    Given I navigate to the login page
    When I leave the username input field empty
    And I click the Submit button
    Then I should see an error message

  Scenario: Verify Valid Username Submission
    Given I navigate to the login page
    When I enter a valid username in the input field
    And I click the Submit button
    Then I should be redirected to the success page or see a success message

  Scenario: Verify Log Out Button Functionality
    Given I am logged in on the page
    When I click the Log Out button
    Then I should be redirected to the login page or see a logout confirmation message

  Scenario: Check Navigation Links
    Given I navigate to the login page
    When I click on each navigation link
    Then I should be redirected to the correct page

  Scenario: Verify Toggle Navigation Button Functionality
    Given I navigate to the login page
    When I click the Toggle Navigation button
    Then the navigation menu should toggle visibility