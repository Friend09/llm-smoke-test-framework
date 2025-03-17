@general
Feature: Smoke Test for Just a Moment Page

  Scenario: Verify Page Title
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/selenium-python-udemy"
    Then user verifies the page title is "Just a moment..."

  Scenario: Verify Page Loading
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/selenium-python-udemy"
    Then user verifies the loading indicator is not displayed
    And user verifies the content is loaded on the screen