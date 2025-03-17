@general

Feature: Smoke Test for Advanced Course Coupon Page

  Scenario: Verify the page title
    Given user opens URL "https://practicetestautomation.com/advanced-course-coupon"
    Then user verifies the title is "Just a moment..."

  Scenario: Verify the page loads without errors
    Given user opens URL "https://practicetestautomation.com/advanced-course-coupon"
    Then user expects the page loads successfully
