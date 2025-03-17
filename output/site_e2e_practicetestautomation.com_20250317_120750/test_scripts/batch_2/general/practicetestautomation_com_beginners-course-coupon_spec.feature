@general

Feature: Smoke Test for Beginners Course Coupon Page

  Scenario: Verify the page loads correctly
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/beginners-course-coupon"
    Then user verifies the page title is "Just a moment..."

  Scenario: Verify the page content is present
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/beginners-course-coupon"
    Then user verifies the content "This is a sample page for testing" is present on screen
  