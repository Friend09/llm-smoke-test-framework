@landing

Feature: Smoke Testing for Courses Page

  Scenario: Verify page loads successfully
    Given user opens URL "https://practicetestautomation.com/courses/"
    Then I expect that the page title is "Courses | Practice Test Automation"
    And I verify that the page loads successfully with a 200 HTTP response status

  Scenario: Verify navigation toggle button functionality
    Given user opens URL "https://practicetestautomation.com/courses/"
    When user clicks on the navigation toggle button
    Then I expect that the navigation menu is displayed

  Scenario: Verify first name input field validation
    Given user opens URL "https://practicetestautomation.com/courses/"
    When user enters valid first name "John" in the input field with id "form_first_name_8"
    Then I expect that the first name input is accepted

  Scenario: Verify email input field validation
    Given user opens URL "https://practicetestautomation.com/courses/"
    When user enters invalid email "invalid-email" in the input field with id "form_email_8"
    Then I expect that an error message is displayed for invalid email format
    When user enters valid email "john.doe@example.com" in the input field with id "form_email_8"
    Then I expect that the email input is accepted
