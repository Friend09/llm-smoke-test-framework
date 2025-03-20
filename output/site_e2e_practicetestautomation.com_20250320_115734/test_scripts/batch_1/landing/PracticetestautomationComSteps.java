
import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class PracticeTestAutomationSteps {
    WebDriver driver;

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        driver = new ChromeDriver();
        driver.get(url);
        Assert.assertTrue(driver.getTitle() != null);
    }

    @Then("user verifies that the page title is {string}")
    public void userVerifiesPageTitle(String title) {
        Assert.assertEquals(title, driver.getTitle());
    }

    @Then("user verifies that the page loads successfully without errors")
    public void userVerifiesPageLoadsSuccessfully() {
        Assert.assertFalse(driver.getPageSource().contains("404") || driver.getPageSource().contains("error"));
    }

    @When("user clicks on the link {string}")
    public void userClicksOnLink(String linkText) {
        driver.findElement(By.linkText(linkText)).click();
    }

    @Then("user should be redirected to the homepage")
    public void userShouldBeRedirectedToHomePage() {
        Assert.assertTrue(driver.getCurrentUrl().contains("homepage-url")); // Replace with actual homepage URL
    }

    @Then("user verifies the appearance on {string}")
    public void userVerifiesAppearance(String deviceType) {
        // Logic to verify appearance based on device type (desktop, tablet, smartphone)
        // Placeholder for actual implementation
    }

    @Then("user verifies that the author's introduction is readable")
    public void userVerifiesAuthorsIntroduction() {
        Assert.assertTrue(driver.getPageSource().contains("Author Introduction")); // Replace with actual text or identifier
    }

    @Then("user verifies that the author's experience is displayed correctly")
    public void userVerifiesAuthorsExperience() {
        Assert.assertTrue(driver.getPageSource().contains("Author Experience")); // Replace with actual text or identifier
    }

    @After
    public void tearDown() {
        driver.quit();
    }
	