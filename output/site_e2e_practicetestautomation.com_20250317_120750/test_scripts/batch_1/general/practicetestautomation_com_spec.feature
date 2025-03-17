@landing

Feature: Smoke Testing for Practice Test Automation Page

  Scenario: Verify page title and content
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/"
    Then user verifies the page title is "Practice Test Automation | Learn Selenium WebDriver"
    And user verifies the heading "Practice Test Automation" is present on screen
    And user verifies the subheading "Learn Selenium WebDriver" is present on screen

  Scenario: Verify navigation to the blog section
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/"
    When user clicks on the link "Blog"
    Then user verifies the page title contains "Blog"
    And user verifies that at least one blog post is displayed on screen

  Scenario: Verify navigation to the courses section
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/"
    When user clicks on the link "Courses"
    Then user verifies the page title contains "Courses"
    And user verifies that at least one course is displayed on screen

  Scenario: Verify footer links
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/"
    When user scrolls to the footer
    Then user verifies the link "Privacy Policy" is present
    And user verifies the link "Terms of Service" is present
    And user verifies the link "Contact Us" is present
	