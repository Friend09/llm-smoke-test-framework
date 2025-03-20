
import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class BlogPageSteps {
    WebDriver driver;

    @Given("user launches browser in {string}")
    public void user_launches_browser_in(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Add other browsers if needed
    }

    @Given("user opens URL {string}")
    public void user_opens_URL(String url) {
        driver.get(url);
        Assert.assertTrue(driver.getTitle().contains("Blog | Practice Test Automation"));
    }

    @Then("user verifies the page title is {string}")
    public void user_verifies_the_page_title_is(String expectedTitle) {
        Assert.assertEquals(expectedTitle, driver.getTitle());
    }

    @Then("user verifies that the page loads without errors")
    public void user_verifies_that_the_page_loads_without_errors() {
        Assert.assertTrue(driver.getPageSource().contains("Unlock Your Future: Selenium WebDriver Career Launcher Part 6"));
    }

    @When("user clicks on the navigation link {string}")
    public void user_clicks_on_the_navigation_link(String linkText) {
        driver.findElement(By.linkText(linkText)).click();
    }

    @Then("user verifies the URL is {string}")
    public void user_verifies_the_URL_is(String expectedUrl) {
        Assert.assertEquals(expectedUrl, driver.getCurrentUrl());
    }

    @Then("user verifies the blog post title is {string}")
    public void user_verifies_the_blog_post_title_is(String postTitle) {
        Assert.assertTrue(driver.getPageSource().contains(postTitle));
    }

    @Then("user verifies the published date is {string}")
    public void user_verifies_the_published_date_is(String publishedDate) {
        Assert.assertTrue(driver.getPageSource().contains(publishedDate));
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}