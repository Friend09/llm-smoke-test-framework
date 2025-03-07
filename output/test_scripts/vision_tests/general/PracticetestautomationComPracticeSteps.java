
import io.cucumber.java.en.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.junit.Assert;

public class PracticePageSteps {
    private WebDriver driver;

    @Given("I am on the Practice page")
    public void i_am_on_the_Practice_page() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        driver.get("https://practicetestautomation.com/practice/");
    }

    @When("I click on the {string} link")
    public void i_click_on_the_link(String linkText) {
        driver.findElement(By.linkText(linkText)).click();
    }

    @Then("I should be redirected to the Login Test page")
    public void i_should_be_redirected_to_the_Login_Test_page() {
        String expectedUrl = "https://practicetestautomation.com/practice/#login";
        Assert.assertEquals(expectedUrl, driver.getCurrentUrl());
        driver.quit();
    }

    @Then("I should be redirected to the Exceptions page")
    public void i_should_be_redirected_to_the_Exceptions_page() {
        String expectedUrl = "https://practicetestautomation.com/practice/#exceptions";
        Assert.assertEquals(expectedUrl, driver.getCurrentUrl());
        driver.quit();
    }

    @Then("the page title should be {string}")
    public void the_page_title_should_be(String title) {
        Assert.assertEquals(title, driver.getTitle());
        driver.quit();
    }

    @Then("the description for {string} should be displayed")
    public void the_description_for_should_be_displayed(String page) {
        String expectedDescription = page.equals("Test Login Page") ? "A test page for logging in" : "A test page for exceptions";
        String actualDescription = driver.findElement(By.xpath("//h3[contains(text(), '" + page + "')]//following-sibling::p")).getText();
        Assert.assertEquals(expectedDescription, actualDescription);
        driver.quit();
    }

    @Then("I should be directed to the corresponding pages")
    public void i_should_be_directed_to_the_corresponding_pages() {
        // Implement checking for each link in the header
        String[] links = {"Home", "Practice", "Courses", "Blog", "Contact"};
        for (String link : links) {
            driver.findElement(By.linkText(link)).click();
            Assert.assertTrue(driver.getCurrentUrl().contains(link.toLowerCase()));
            driver.navigate().back();
        }
        driver.quit();
    }
