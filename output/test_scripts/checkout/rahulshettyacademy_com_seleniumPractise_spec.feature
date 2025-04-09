@general

Feature: GreenKart Smoke Test

  Scenario: Verify Page Title
    Given user opens URL "https://rahulshettyacademy.com/seleniumPractise"
    Then user verifies the page title is "GreenKart - veg and fruits kart"

  Scenario: Verify Search Functionality
    Given user opens URL "https://rahulshettyacademy.com/seleniumPractise"
    When user enters "Cucumber" in the search bar
    And user clicks on the search button
    Then user verifies that search results are displayed

  Scenario: Verify Add to Cart Functionality
    Given user opens URL "https://rahulshettyacademy.com/seleniumPractise"
    When user clicks on the "Add to Cart" button for a product
    Then user verifies that the cart icon updates to reflect the number of items added

  Scenario: Verify Checkout Button
    Given user opens URL "https://rahulshettyacademy.com/seleniumPractise"
    When user clicks on the Checkout button
    Then user verifies that the checkout page is displayed
	