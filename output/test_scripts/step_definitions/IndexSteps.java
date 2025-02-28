import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.junit.Assert;

public class ExampleDomainSteps {
    private WebDriver driver;

    @Given("I open the page URL {string}")
    public void openPage(String url) {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver"); // Set your own path
        driver = new ChromeDriver();
        driver.get(url);
    }

    @Then("the page title should be {string}")
    public void verifyPageTitle(String expectedTitle) {
        String actualTitle = driver.getTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("the heading {string} should be present")
    public void verifyHeading(String headingText) {
        WebElement heading = driver.findElement(By.xpath("//h1[text()='" + headingText + "']"));
        Assert.assertTrue(heading.isDisplayed());
    }

    @Then("the link with text {string} should be visible and enabled")
    public void verifyLink(String linkText) {
        WebElement link = driver.findElement(By.xpath("//a[text()='" + linkText + "']"));
        Assert.assertTrue(link.isDisplayed());
        Assert.assertTrue(link.isEnabled());
    }

    @When("I click on the link {string}")
    public void clickLink(String linkText) {
        WebElement link = driver.findElement(By.xpath("//a[text()='" + linkText + "']"));
        link.click();
    }

    @Then("I should be redirected to {string}")
    public void verifyRedirect(String expectedUrl) {
        String actualUrl = driver.getCurrentUrl();
        Assert.assertEquals(expectedUrl, actualUrl);
        driver.quit(); // Close the browser
    }
}