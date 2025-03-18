@login

Feature: Smoke Testing for Practice Test Login Page

  Background: 
    Given I navigate to the page URL "https://practicetestautomation.com/practice-test-login/"
    Then I verify that the page title is "Test Login | Practice Test Automation"

  Scenario: Verify Username Input Field
    Given I check that the 'username' input field is present and enabled
    When I enter a valid username into the 'username' input field
    Then I expect that the 'username' input field contains the entered username

  Scenario: Verify Submit Button Functionality
    Given I check that the 'submit' button is present and enabled
    When I enter a valid username into the 'username' input field
    And I click on the 'submit' button
    Then I expect that I am redirected to the appropriate page with a success message

  Scenario: Verify Toggle Navigation Button
    Given I click on the 'toggle-navigation' button
    Then I expect that the navigation menu appears
    When I click on the 'toggle-navigation' button again
    Then I expect that the navigation menu disappears

  Scenario: Verify Error Handling with Invalid Credentials
    Given I check that the 'username' input field is present and enabled
    When I enter an invalid username into the 'username' input field
    And I click on the 'submit' button
    Then I expect to see an appropriate error message
	