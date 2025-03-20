@landing

Feature: Smoke Testing for Practice Test Automation Page

  Scenario: Verify Page Load
    Given user opens URL "https://practicetestautomation.com/"
    Then user verifies that the page title is "Practice Test Automation | Learn Selenium WebDriver"
    And user verifies that the page loads successfully without errors

  Scenario: Verify Navigation Functionality
    Given user opens URL "https://practicetestautomation.com/"
    When user clicks on the link "HOME"
    Then user should be redirected to the homepage
    When user clicks on the link "PRACTICE"
    Then user should be redirected to the practice page
    When user clicks on the link "COURSES"
    Then user should be redirected to the courses page
    When user clicks on the link "BLOG"
    Then user should be redirected to the blog page
    When user clicks on the link "CONTACT"
    Then user should be redirected to the contact page

  Scenario: Verify Responsive Design
    Given user opens URL "https://practicetestautomation.com/"
    Then user verifies the appearance on desktop
    And user verifies the appearance on tablet
    And user verifies the appearance on smartphone

  Scenario: Verify Content
    Given user opens URL "https://practicetestautomation.com/"
    Then user verifies that the author's introduction is readable
    And user verifies that the author's experience is displayed correctly
	