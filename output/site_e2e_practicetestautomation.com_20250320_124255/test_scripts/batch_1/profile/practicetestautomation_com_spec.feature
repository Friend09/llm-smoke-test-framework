@landing

Feature: Smoke Testing Practice Test Automation Page

  Scenario: Verify page loads successfully
    Given user opens URL "https://practicetestautomation.com/"
    Then user expects that the page title is "Practice Test Automation | Learn Selenium WebDriver"

  Scenario: Verify navigation links functionality
    Given user opens URL "https://practicetestautomation.com/"
    When user clicks on the navigation link "Home"
    Then user expects that the current URL is "https://practicetestautomation.com/"
    When user clicks on the navigation link "Practice"
    Then user expects that the current URL is "https://practicetestautomation.com/practice/"
    When user clicks on the navigation link "Courses"
    Then user expects that the current URL is "https://practicetestautomation.com/courses/"
    When user clicks on the navigation link "Blog"
    Then user expects that the current URL is "https://practicetestautomation.com/blog/"
    When user clicks on the navigation link "Contact"
    Then user expects that the current URL is "https://practicetestautomation.com/contact/"

  Scenario: Verify profile image interaction
    Given user opens URL "https://practicetestautomation.com/"
    When user clicks on the profile image
    Then user expects that the profile information is displayed

  Scenario: Verify content display
    Given user opens URL "https://practicetestautomation.com/"
    Then user verifies that the greeting "Hello" is present on screen
    And user verifies that the introduction text is displayed correctly

  Scenario: Verify responsive design
    Given user opens URL "https://practicetestautomation.com/"
    When user resizes the browser to "mobile"
    Then user expects that the navigation links are accessible
    When user resizes the browser to "tablet"
    Then user expects that the layout is displayed correctly
    When user resizes the browser to "desktop"
    Then user expects that the full layout is displayed correctly
