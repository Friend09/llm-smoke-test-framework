@landing

Feature: Smoke Testing for Blog Page

  Scenario: Verify Blog Page Loads Correctly
    Given user opens the URL "https://practicetestautomation.com/blog/"
    Then user verifies the page title is "Blog | Practice Test Automation"
    And user verifies the toggle navigation button is present

  Scenario: Toggle Navigation Menu
    Given user opens the URL "https://practicetestautomation.com/blog/"
    When user clicks on the toggle navigation button
    Then user expects the navigation menu to be visible
    When user clicks on the toggle navigation button again
    Then user expects the navigation menu to be hidden

  Scenario: Verify Interactive Elements
    Given user opens the URL "https://practicetestautomation.com/blog/"
    Then user verifies the navigation links "Home", "Practice", "Courses", "Blog", "Contact" are present
    And user verifies the first name input field is present
    And user verifies the email input field is present
    And user verifies the footer links are present
	