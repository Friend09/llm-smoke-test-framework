@landing

Feature: Privacy Policy Page

  Scenario: verify privacy policy page title
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/privacy-policy/"
    Then user verifies the page title is "Privacy Policy | Practice Test Automation"

  Scenario: verify privacy policy content
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/privacy-policy/"
    Then user verifies the element "Privacy Policy" is present on screen
    And user verifies that the content includes the text "This privacy policy document outlines the types of personal information that is received and collected by Practice Test Automation and how it is used."
  