@general

Feature: Smoke Test for Rest Assured Course Coupon Page

  Scenario: Verify page title and content
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/rest-assured-course-coupon"
    Then user verifies the title is "Just a moment..."
    And user verifies that the content is present on the screen

  Scenario: Verify link functionality
    Given user launches browser in "Chrome"
    And user opens URL "https://practicetestautomation.com/rest-assured-course-coupon"
    When user verifies that the 'Get Your Coupon' link is present
    And user clicks on the link 'Get Your Coupon'
    Then user expects that a new page loads with appropriate content
	