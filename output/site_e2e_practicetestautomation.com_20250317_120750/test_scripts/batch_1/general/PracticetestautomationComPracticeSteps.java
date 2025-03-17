
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class PracticePageSteps {
    PracticePage practicePage = new PracticePage();

    @Given("user launches browser in {string}")
    public void user_launches_browser_in(String browser) {
        practicePage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void user_opens_URL(String url) {
        practicePage.openUrl(url);
    }

    @Then("user verifies the title is {string}")
    public void user_verifies_the_title_is(String expectedTitle) {
        String actualTitle = practicePage.getTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the element {string} is present on the screen")
    public void user_verifies_the_element_is_present_on_the_screen(String elementName) {
        Assert.assertTrue(practicePage.isElementPresent(elementName));
    }

    @When("user clicks on the {string} link")
    public void user_clicks_on_the_link(String elementName) {
        practicePage.clickElement(elementName);
    }

    @Then("user expects the URL to contain {string}")
    public void user_expects_the_URL_to_contain(String expectedSubString) {
        String currentUrl = practicePage.getCurrentUrl();
        Assert.assertTrue(currentUrl.contains(expectedSubString));
    }

    @When("user navigates back")
    public void user_navigates_back() {
        practicePage.navigateBack();
    }
}