@general
Feature: Smoke Test for Java for Testers Page

  Scenario: Verify page title and accessibility
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/java-for-testers-udemy"
    Then user verifies the page title is "Just a moment..."
    And user verifies that the page is accessible