Feature: Smoke Testing Example Domain

  Scenario: Verify Example Domain Page
    Given I open the page URL "https://example.com"
    Then the page title should be "Example Domain"
    And the heading "Example Domain" should be present
    And the link with text "More information..." should be visible and enabled
    When I click on the link "More information..."
    Then I should be redirected to "https://www.iana.org/domains/example"