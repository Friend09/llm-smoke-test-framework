@landing

Feature: Blog Page Smoke Test

  Background: User is on the Blog page
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/blog/"
    And user verifies page title is "Blog | Practice Test Automation"

  Scenario: Verify navigation functionality
    When user clicks on the navigation link "Home"
    Then user should be navigated to the Home page
    When user clicks on the navigation link "Practice"
    Then user should be navigated to the Practice page
    When user clicks on the navigation link "Courses"
    Then user should be navigated to the Courses page
    When user clicks on the navigation link "Contact"
    Then user should be navigated to the Contact page

  Scenario: Verify article loads correctly
    When user clicks on the article title link "Unlock Your Future: Selenium WebDriver Career Launcher Part 6"
    Then user should see the article content loaded without errors

  Scenario: Verify content visibility
    Then user verifies that the article title, author, and body text are visible on the screen
    And user verifies that the navigation toggle button is present and clickable

  Scenario: Verify responsive design
    When user resizes the browser to mobile view
    Then user should see that the layout adjusts correctly
    When user resizes the browser to tablet view
    Then user should see that the layout adjusts correctly
    When user resizes the browser to desktop view
    Then user should see that the layout adjusts correctly
	