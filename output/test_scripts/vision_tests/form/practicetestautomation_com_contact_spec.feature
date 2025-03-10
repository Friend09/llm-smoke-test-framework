
Feature: Contact Form Submission

  Background:
    Given I navigate to the contact page

  Scenario: Attempt to submit the contact form without filling out required fields
    When I click the submit button
    Then I should see validation messages for Name and Email fields

  Scenario: Submit the contact form with valid data
    Given I fill in the contact form with valid data
      | Name          | Email               | Message            |
      | John Doe     | john.doe@example.com| This is a test message. |
    When I click the submit button
    Then I should see a confirmation message

  Scenario: Submit the contact form with invalid email format
    Given I fill in the contact form with invalid email
      | Name          | Email               | Message            |
      | Jane Doe     | jane.doe@invalid    | This is a test message. |
    When I click the submit button
    Then I should see a validation message for the email format

  Scenario: Verify navigation links
    When I click on the Home link
    Then I should be redirected to the Home page
    When I click on the Practice link
    Then I should be redirected to the Practice page
    When I click on the Courses link
    Then I should be redirected to the Courses page
    When I click on the Blog link
    Then I should be redirected to the Blog page
    When I click on the Contact link
    Then I should be redirected to the Contact page
  