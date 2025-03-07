
Feature: Practice Page Smoke Test

  Scenario: Validate that clicking on "Test Login Page" successfully redirects to the correct login test page.
    Given I am on the Practice page
    When I click on the "Test Login Page" link
    Then I should be redirected to the Login Test page

  Scenario: Validate that clicking on "Test Exceptions" successfully redirects to the page for reproducing Selenium exceptions.
    Given I am on the Practice page
    When I click on the "Test Exceptions" link
    Then I should be redirected to the Exceptions page

  Scenario: Ensure that all navigation links in the header are clickable and direct to the corresponding pages.
    Given I am on the Practice page
    When I click on each navigation link in the header
    Then I should be directed to the corresponding pages

  Scenario: Check that the page title "Practice" displays correctly in the browser tab.
    Given I am on the Practice page
    Then the page title should be "Practice"

  Scenario: Verify that the descriptions of each test page are correctly displayed beneath their respective links.
    Given I am on the Practice page
    Then the description for "Test Login Page" should be displayed
    And the description for "Test Exceptions" should be displayed
