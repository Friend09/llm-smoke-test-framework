import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class PracticePageSteps {
    WebDriver driver;

    @Given("user opens URL {string}")
    public void openURL(String url) {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        driver.get(url);
    }

    @Then("user verifies the page title is {string}")
    public void verifyPageTitle(String expectedTitle) {
        String actualTitle = driver.getTitle();
        assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the toggle navigation button is visible")
    public void verifyToggleButtonVisible() {
        WebElement toggleButton = driver.findElement(By.id("toggle-navigation"));
        assertTrue(toggleButton.isDisplayed());
    }

    @When("user clicks the toggle navigation button")
    public void clickToggleButton() {
        WebElement toggleButton = driver.findElement(By.id("toggle-navigation"));
        toggleButton.click();
    }

    @Then("user verifies the navigation menu is displayed")
    public void verifyNavigationMenuDisplayed() {
        WebElement navMenu = driver.findElement(By.id("navigation")); // Replace with actual ID or class
        assertTrue(navMenu.isDisplayed());
    }

    @When("user clicks on the link {string}")
    public void clickLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }

    @Then("user verifies the URL is {string}")
    public void verifyURL(String expectedURL) {
        String actualURL = driver.getCurrentUrl();
        assertEquals(expectedURL, actualURL);
    }

    // Clean up method to close the browser
    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}