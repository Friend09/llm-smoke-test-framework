
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import static org.junit.Assert.*;

public class PythonForTestersSteps {
    private WebDriver driver;
    private PythonForTestersPage pythonForTestersPage;

    @Given("user launches browser in \"Chrome\"")
    public void user_launches_browser_in_Chrome() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        pythonForTestersPage = new PythonForTestersPage(driver);
    }

    @Given("user opens URL \"(.*?)\"")
    public void user_opens_url(String url) {
        driver.get(url);
    }

    @Then("I expect that the page title is \"(.*?)\"")
    public void i_expect_that_the_page_title_is(String expectedTitle) {
        String actualTitle = driver.getTitle();
        assertEquals(expectedTitle, actualTitle);
    }

    @Then("I verify that the content is present on the screen")
    public void i_verify_that_the_content_is_present() {
        assertTrue(pythonForTestersPage.isContentVisible());
    }

    @Then("I expect that the page has loaded successfully")
    public void i_expect_that_the_page_has_loaded_successfully() {
        assertTrue(pythonForTestersPage.isPageLoaded());
    }

    @Then("I verify that there are no errors displayed on the page")
    public void i_verify_that_there_are_no_errors_displayed_on_the_page() {
        assertFalse(pythonForTestersPage.hasErrors());
    }
	
    // Clean up after tests
    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
	