Feature: Contact Page Smoke Testing

  Scenario: Verify page title and elements
    Given user opens the contact page
    Then user verifies the page title is "Contact | Practice Test Automation | Selenium WebDriver"
    And user verifies the "Name" input field is present
    And user verifies the "Email" input field is present
    And user verifies the "Comment/Message" text area is present
    And user verifies the "Submit" button is present

  Scenario: Form Submission with valid data
    Given user opens the contact page
    When user enters "John Doe" into the "Name" field
    And user enters "john.doe@example.com" into the "Email" field
    And user enters "This is a test message." into the "Comment/Message" field
    And user clicks on the "Submit" button
    Then user verifies that the submission is successful

  Scenario: Field Validation Test
    Given user opens the contact page
    When user leaves the "Name" field empty
    And user enters "john.doe@example.com" into the "Email" field
    And user enters "This is a test message." into the "Comment/Message" field
    And user clicks on the "Submit" button
    Then user verifies that the validation message for the "Name" field is displayed
    
    When user enters "" into the "Email" field
    And user clicks on the "Submit" button
    Then user verifies that the validation message for the "Email" field is displayed

  Scenario: Navigation Test
    Given user opens the contact page
    When user clicks on the "Home" navigation link
    Then user verifies that the user is navigated to the home page
    When user clicks on the "Practice" navigation link
    Then user verifies that the user is navigated to the practice page
    When user clicks on the "Courses" navigation link
    Then user verifies that the user is navigated to the courses page
    When user clicks on the "Blog" navigation link
    Then user verifies that the user is navigated to the blog page