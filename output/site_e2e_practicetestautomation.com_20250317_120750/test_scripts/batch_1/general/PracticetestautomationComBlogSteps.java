
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class BlogSteps {
    
    BlogPage blogPage = new BlogPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        blogPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        blogPage.openURL(url);
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitleIs(String expectedTitle) {
        String actualTitle = blogPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies {string} is present on screen")
    public void userVerifiesIsPresentOnScreen(String elementText) {
        Assert.assertTrue(blogPage.isElementPresent(elementText));
    }

    @Then("user verifies at least one blog post is displayed")
    public void userVerifiesAtLeastOneBlogPostIsDisplayed() {
        Assert.assertTrue(blogPage.isBlogPostDisplayed());
    }

    @When("user clicks on the first blog post title")
    public void userClicksOnFirstBlogPostTitle() {
        blogPage.clickFirstBlogPost();
    }

    @Then("user verifies the blog post page is displayed")
    public void userVerifiesTheBlogPostPageIsDisplayed() {
        Assert.assertTrue(blogPage.isBlogPostPageDisplayed());
    }
	