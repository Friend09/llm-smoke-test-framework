@form
Feature: Contact Page Smoke Test

  Scenario: Verify Contact Page Title
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/contact/"
    Then user verifies the title is "Contact | Practice Test Automation | Selenium WebDriver"

  Scenario: Verify Contact Form Elements
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/contact/"
    Then user verifies "Your Name" input field is present on screen
    Then user verifies "Your Email" input field is present on screen
    Then user verifies "Your Message" text area is present on screen
    Then user verifies "Send Message" button is present on screen

  Scenario: Submit Contact Form
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/contact/"
    When user enters "Test User" into the input field "Your Name"
    And user enters "test@example.com" into the input field "Your Email"
    And user enters "This is a test message." into the text area "Your Message"
    And user clicks on the button "Send Message"
    Then user verifies success message is displayed on screen