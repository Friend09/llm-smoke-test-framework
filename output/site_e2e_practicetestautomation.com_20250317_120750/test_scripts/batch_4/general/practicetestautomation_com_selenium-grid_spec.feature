@general

Feature: Smoke Test for Selenium Grid Page

    Scenario: verify page title
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/selenium-grid"
        Then user verifies the page title is "Just a moment..."
        
    Scenario: check for static content
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/selenium-grid"
        Then user verifies that the text "This page is using a script to ensure you are human." is present on the screen
        And user verifies that the text "Please wait while we take you to the appropriate page." is present on the screen
	