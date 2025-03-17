@landing

Feature: Smoke Testing for Test Exceptions Page

    Scenario: Verify the page title
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/practice-test-exceptions/"
        Then user verifies page title is "Test Exceptions | Practice Test Automation"

    Scenario: Verify presence of key elements
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/practice-test-exceptions/"
        Then user verifies element "Test Exceptions" is present on screen
        Then user verifies element "Test Exception 1" is present on screen
        Then user verifies element "Test Exception 2" is present on screen
        Then user verifies element "Test Exception 3" is present on screen
    