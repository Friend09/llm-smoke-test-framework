@landing
Feature: Smoke Testing for Practice Test Automation Page

  Scenario: Verify page title and primary elements
    Given user opens the page "https://practicetestautomation.com/"
    Then user verifies that the page title is "Practice Test Automation | Learn Selenium WebDriver"
    And user verifies the navigation button is displayed and clickable
    And user enters "John" into the input field with ID "form_first_name_7"
    And user enters "john@example.com" into the input field with ID "form_email_7"
    And user verifies that all links on the page are functioning correctly
    And user checks that the header section is visible
    And user checks that the experience and expertise section is visible
