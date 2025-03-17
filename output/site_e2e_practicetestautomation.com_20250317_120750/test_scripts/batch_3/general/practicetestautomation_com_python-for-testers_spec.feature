@general

Feature: Smoke Test for Python for Testers Page

  Scenario: Verify Page Title and Content
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/python-for-testers"
    Then I expect that the page title is "Just a moment..."
    And I verify that the content is present on the screen

  Scenario: Verify Page Load
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/python-for-testers"
    Then I expect that the page has loaded successfully
    And I verify that there are no errors displayed on the page
	