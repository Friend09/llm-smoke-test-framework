@landing

Feature: Smoke Test for Practice Test Automation Page

  Scenario: Verify the Practice page is accessible
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies the title is "Practice | Practice Test Automation"

  Scenario: Verify elements are displayed on the Practice page
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/practice/"
    Then user verifies the element "Sample A" is present on the screen
    And user verifies the element "Sample B" is present on the screen
    And user verifies the element "Sample C" is present on the screen

  Scenario: Verify the functionality of the test automation elements
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/practice/"
    When user clicks on the "Sample A" link
    Then user expects the URL to contain "sample-a"
    And user navigates back
    When user clicks on the "Sample B" link
    Then user expects the URL to contain "sample-b"
    And user navigates back
