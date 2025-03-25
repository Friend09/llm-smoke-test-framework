@landing

Feature: Courses Page Smoke Test

    Scenario: Verify Page Title
        Given user opens URL "https://practicetestautomation.com/courses/"
        Then user verifies the page title is "Courses | Practice Test Automation"

    Scenario: Verify Page URL
        Given user opens URL "https://practicetestautomation.com/courses/"
        Then user verifies the current URL is "https://practicetestautomation.com/courses/"

    Scenario: Verify Navigation Button Functionality
        Given user opens URL "https://practicetestautomation.com/courses/"
        When user clicks on the navigation button "Toggle Navigation"
        Then user verifies the navigation menu appears

    Scenario: Check First Name Input Field
        Given user opens URL "https://practicetestautomation.com/courses/"
        Then user verifies the first name input field is present
        And user enters "Test First Name" into the first name input field

    Scenario: Check Email Input Field
        Given user opens URL "https://practicetestautomation.com/courses/"
        Then user verifies the email input field is present
        And user enters "test@example.com" into the email input field

    Scenario: Test Input Validation
        Given user opens URL "https://practicetestautomation.com/courses/"
        When user enters "invalid_email" into the email input field
        And user submits the form
        Then user verifies the validation message is displayed

    Scenario: Empty Field Validation
        Given user opens URL "https://practicetestautomation.com/courses/"
        When user submits the form without filling any fields
        Then user verifies the appropriate validation messages are displayed
	