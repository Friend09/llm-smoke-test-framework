@landing

Feature: Smoke Test for Practice Page

  Scenario: Verify Page Title and Navigation Links
    Given user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies page title is "Practice | Practice Test Automation"
    And user verifies the link "HOME" is present and clickable
    And user verifies the link "PRACTICE" is present and clickable
    And user verifies the link "COURSES" is present and clickable
    And user verifies the link "BLOG" is present and clickable
    And user verifies the link "CONTACT" is present and clickable

  Scenario: Access Test Login Page
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the link "Test Login Page"
    Then user verifies the current URL is "https://practicetestautomation.com/practice/#test-login"
    And user verifies the title contains "Test Login"

  Scenario: Access Test Exceptions Page
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the link "Test Exceptions"
    Then user verifies the current URL is "https://practicetestautomation.com/practice/#test-exceptions"
    And user verifies the title contains "Test Exceptions"

  Scenario: Verify Toggle Navigation Button
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the toggle navigation button
    Then user verifies that the navigation menu is displayed
    When user clicks on the toggle navigation button again
    Then user verifies that the navigation menu is hidden
	