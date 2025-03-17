@login

Feature: Smoke Testing for Practice Test Automation Login Page

    Scenario: Verify the login page title
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        Then user verifies the page title is "Test Login | Practice Test Automation"

    Scenario: Verify login functionality with valid credentials
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        When user enters "student" into the username field
        And user enters "Password123" into the password field
        And user clicks the login button
        Then user verifies the message "Welcome to Practice Test Automation" is present on the screen

    Scenario: Verify the error message for invalid login
        Given user opens the URL "https://practicetestautomation.com/practice-test-login/"
        When user enters "invalidUser" into the username field
        And user enters "invalidPassword" into the password field
        And user clicks the login button
        Then user verifies the message "Your username is invalid!" is present on the screen
	