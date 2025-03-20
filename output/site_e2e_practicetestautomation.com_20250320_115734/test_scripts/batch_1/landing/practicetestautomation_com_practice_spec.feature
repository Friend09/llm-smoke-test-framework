@landing

Feature: Smoke Test for Practice Page

  Scenario: Verify page loads and title
    Given user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies page title is "Practice | Practice Test Automation"
    And user verifies the button with ID "toggle-navigation" is visible and clickable

  Scenario: Verify navigation links
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the link "HOME"
    Then user expects to be redirected to the homepage
    When user clicks on the link "PRACTICE"
    Then user expects to remain on the practice page

  Scenario: Verify content links
    Given user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the link "Test Login Page"
    Then user expects to see content for "Test Login Page"
    When user clicks on the link "Test Exceptions"
    Then user expects to see content for "Test Exceptions"