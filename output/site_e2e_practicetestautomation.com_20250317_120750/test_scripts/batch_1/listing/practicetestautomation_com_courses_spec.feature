@landing
Feature: Courses Page Smoke Test

  Scenario: Verify Courses Page Title
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/courses/"
    Then user verifies page title is "Courses | Practice Test Automation"

  Scenario: Verify Course Elements are Present
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/courses/"
    Then user verifies course section is present on screen
    And user verifies course list is displayed
