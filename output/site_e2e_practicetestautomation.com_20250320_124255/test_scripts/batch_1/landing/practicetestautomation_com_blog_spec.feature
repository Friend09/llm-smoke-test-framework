@landing

Feature: Blog Page Smoke Tests

  Scenario: Verify blog page loads correctly
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/blog/"
    Then user verifies the page title is "Blog | Practice Test Automation"
    And user verifies that the page loads without errors

  Scenario: Verify navigation links
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/blog/"
    When user clicks on the navigation link "Home"
    Then user verifies the URL is "https://practicetestautomation.com/"
    When user clicks on the navigation link "Practice"
    Then user verifies the URL is "https://practicetestautomation.com/practice/"
    When user clicks on the navigation link "Courses"
    Then user verifies the URL is "https://practicetestautomation.com/courses/"
    When user clicks on the navigation link "Contact"
    Then user verifies the URL is "https://practicetestautomation.com/contact/"

  Scenario: Verify blog content accessibility
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/blog/"
    Then user verifies the blog post title is "Unlock Your Future: Selenium WebDriver Career Launcher Part 6"
    And user verifies the published date is "Published by Dmitry Shyshkin on July 22, 2024"