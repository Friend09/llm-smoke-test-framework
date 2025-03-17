@general
Feature: Smoke Test for XPath Course Coupon Page

  Scenario: Verify page title
    Given I navigate to the XPath Course Coupon page
    Then I expect that the page title is "Just a moment..."

  Scenario: Verify page load
    Given I navigate to the XPath Course Coupon page
    Then I expect that the page is loaded successfully
    And I expect that no error message is displayed