@login

Feature: Smoke Test for Practice Test Automation Login Page

    Scenario: Verify page title and elements
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        Then user verifies the page title is "Test Login | Practice Test Automation"
        And user verifies the username input field is present
        And user verifies the password input field is present
        And user verifies the submit button is present

    Scenario: Verify successful login with valid credentials
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        When user enters "valid_username" into the username input field
        And user enters "valid_password" into the password input field
        And user clicks the submit button
        Then user expects to see a successful login message or redirection

    Scenario: Verify validation message for empty fields
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        When user clicks the submit button without entering credentials
        Then user expects to see validation messages for empty fields
