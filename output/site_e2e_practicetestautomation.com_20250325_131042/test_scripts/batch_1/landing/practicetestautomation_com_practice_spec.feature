@landing
Feature: Practice Page Smoke Test

  Scenario: Verify page title
    Given user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies the page title is "Practice | Practice Test Automation"

  Scenario: Verify navigation toggle button
    Given user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies the toggle navigation button is visible
    When user clicks the toggle navigation button
    Then user verifies the navigation menu is displayed

  Scenario: Verify navigation links
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the link "Home"
    Then user verifies the URL is "https://practicetestautomation.com/"
    And user navigates back to the previous page
    When user clicks on the link "Practice"
    Then user verifies the URL is "https://practicetestautomation.com/practice/"