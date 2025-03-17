@landing

Feature: Blog Smoke Testing

    Scenario: Verify Blog Page Title
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/blog/"
        Then user verifies page title is "Blog | Practice Test Automation"

    Scenario: Verify Blog Page Content
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/blog/"
        Then user verifies "Welcome to Practice Test Automation" is present on screen
        And user verifies "Latest Posts" is present on screen
        And user verifies at least one blog post is displayed

    Scenario: Verify Navigation to a Blog Post
        Given user launches browser in "Chrome"
        And user opens URL "https://practicetestautomation.com/blog/"
        When user clicks on the first blog post title
        Then user verifies the blog post page is displayed
        And user verifies the blog post title is present on screen
	