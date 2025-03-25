@form

Feature: Contact Form Smoke Testing

  Scenario: Verify Page Title
    Given user opens URL "https://practicetestautomation.com/contact/"
    Then user verifies the page title is "Contact | Practice Test Automation | Selenium WebDriver"

  Scenario: Verify Empty Form Submission
    Given user opens URL "https://practicetestautomation.com/contact/"
    When user submits the form without filling any fields
    Then user verifies the validation messages are displayed

  Scenario: Verify Valid Input Submission
    Given user opens URL "https://practicetestautomation.com/contact/"
    When user enters "John" into the first name input field
    And user enters "Doe" into the last name input field
    And user enters "john.doe@example.com" into the email input field
    And user enters "This is a test message." into the message input field
    And user clicks the submit button
    Then user verifies a successful submission acknowledgment is displayed

  Scenario: Verify Invalid Email Format Submission
    Given user opens URL "https://practicetestautomation.com/contact/"
    When user enters "John" into the first name input field
    And user enters "Doe" into the last name input field
    And user enters "invalid-email-format" into the email input field
    And user enters "This is a test message." into the message input field
    And user clicks the submit button
    Then user verifies the appropriate error message for invalid email is displayed

  Scenario: Verify Field Length Validation for Message
    Given user opens URL "https://practicetestautomation.com/contact/"
    When user enters "John" into the first name input field
    And user enters "Doe" into the last name input field
    And user enters "john.doe@example.com" into the email input field
    And user enters a message longer than 500 characters into the message input field
    And user clicks the submit button
    Then user verifies the appropriate error message for message length is displayed

  Scenario: Verify Navigation Links
    Given user opens URL "https://practicetestautomation.com/contact/"
    When user clicks the navigation link "Home"
    Then user verifies the URL is correct for the Home page
    When user clicks the navigation link "Practice"
    Then user verifies the URL is correct for the Practice page
    When user clicks the navigation link "Courses"
    Then user verifies the URL is correct for the Courses page
    When user clicks the navigation link "Blog"
    Then user verifies the URL is correct for the Blog page
