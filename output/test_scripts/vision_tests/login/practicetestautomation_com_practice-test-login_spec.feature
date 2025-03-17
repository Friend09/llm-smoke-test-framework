Feature: Smoke Testing for Practice Test Login Page

  Scenario: Verify Page Title
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    Then user verifies page title is "Test Login | Practice Test Automation"

  Scenario: Positive Login Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "testuser" into the username field
    And user enters "Password123" into the password field
    And user clicks on the Submit button
    Then user expects to see a successful login message

  Scenario: Negative Login Test (Invalid Credentials)
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "invaliduser" into the username field
    And user enters "wrongpassword" into the password field
    And user clicks on the Submit button
    Then user expects to see an error message

  Scenario: Empty Fields Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user leaves username and password fields empty
    And user clicks on the Submit button
    Then user expects to see validation messages for required fields

  Scenario: Field Length Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user enters "a very long username that exceeds the limit" into the username field
    And user enters "a very long password that exceeds the limit" into the password field
    And user clicks on the Submit button
    Then user expects appropriate validation messages for input limits

  Scenario: Password Visibility Toggle Test
    Given user opens URL "https://practicetestautomation.com/practice-test-login/"
    When user clicks on the password visibility toggle
    Then user expects the password to be visible