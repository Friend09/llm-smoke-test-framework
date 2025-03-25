
import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class BlogPageSteps {
    WebDriver driver;
    BlogPage blogPage;

    @Given("user launches browser in {string}")
    public void userLaunchesBrowser(String browser) {
        if (browser.equals("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browser logic can be added here
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        driver.get(url);
    }

    @Given("user verifies page title is {string}")
    public void userVerifiesPageTitle(String expectedTitle) {
        Assert.assertEquals(expectedTitle, driver.getTitle());
    }

    @When("user clicks on the navigation link {string}")
    public void userClicksOnNavigationLink(String linkText) {
        blogPage.clickNavigationLink(linkText);
    }

    @Then("user should be navigated to the {string} page")
    public void userShouldBeNavigatedToPage(String expectedPage) {
        // Logic to verify the current page matches the expected page
    }

    @When("user clicks on the article title link {string}")
    public void userClicksOnArticleTitleLink(String articleTitle) {
        blogPage.clickArticleTitle(articleTitle);
    }

    @Then("user should see the article content loaded without errors")
    public void userShouldSeeArticleLoaded() {
        Assert.assertTrue(blogPage.isArticleContentVisible());
    }

    @Then("user verifies that the article title, author, and body text are visible on the screen")
    public void userVerifiesContentVisibility() {
        Assert.assertTrue(blogPage.isContentVisible());
    }

    @Then("user verifies that the navigation toggle button is present and clickable")
    public void userVerifiesToggleButton() {
        Assert.assertTrue(blogPage.isToggleButtonPresent());
    }

    @When("user resizes the browser to {string} view")
    public void userResizesBrowser(String view) {
        // Logic to resize browser based on view (mobile, tablet, desktop)
    }

    @Then("user should see that the layout adjusts correctly")
    public void userVerifiesLayoutAdjustment() {
        // Logic to verify layout adjustments
    }
}
	