@general

Feature: Smoke Test for Just a Moment Page

  Scenario: Verify page title and content
    Given user navigates to the page "https://practicetestautomation.com/selenium-webdriver-test-framework-from-scratch-referralCode"
    Then user verifies the page title is "Just a moment..."
    And user verifies the page contains a loading message

  Scenario: Verify page loading process
    Given user navigates to the page "https://practicetestautomation.com/selenium-webdriver-test-framework-from-scratch-referralCode"
    When user waits for the loading to complete
    Then user verifies the expected content is displayed after loading
