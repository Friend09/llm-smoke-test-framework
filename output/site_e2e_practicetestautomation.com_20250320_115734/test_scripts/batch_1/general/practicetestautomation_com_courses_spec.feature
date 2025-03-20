@landing

Feature: Smoke Testing for Courses Page

  Background: 
    Given I navigate to the courses page

  Scenario: Verify Page Load
    Then I expect the page title to be "Courses | Practice Test Automation"
    And I expect the page URL to be "https://practicetestautomation.com/courses/"

  Scenario: Verify Navigation Toggle Button
    When I click on the navigation toggle button
    Then I expect the navigation menu to be visible

  Scenario: Verify First Name Input Field
    When I click on the first name input field
    Then I expect the first name input field to be editable
    And I expect the first name input field to accept text input

  Scenario: Verify Email Input Field
    When I click on the email input field
    Then I expect the email input field to be editable
    And I expect the email input field to accept valid email formats
    And I expect the email input field to display appropriate placeholder text
