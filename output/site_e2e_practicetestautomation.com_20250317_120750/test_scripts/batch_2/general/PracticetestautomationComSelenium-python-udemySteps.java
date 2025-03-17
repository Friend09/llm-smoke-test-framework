import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class SmokeTestSteps {
    private JustAMomentPage justAMomentPage = new JustAMomentPage();

    @Given("user launches browser in {string}")
    public void user_launches_browser_in(String browser) {
        // Code to launch the specified browser
    }

    @Given("user opens URL {string}")
    public void user_opens_URL(String url) {
        justAMomentPage.navigateTo(url);
    }

    @Then("user verifies the page title is {string}")
    public void user_verifies_the_page_title_is(String expectedTitle) {
        String actualTitle = justAMomentPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the loading indicator is not displayed")
    public void user_verifies_the_loading_indicator_is_not_displayed() {
        Assert.assertFalse(justAMomentPage.isLoadingIndicatorDisplayed());
    }

    @Then("user verifies the content is loaded on the screen")
    public void user_verifies_the_content_is_loaded_on_the_screen() {
        Assert.assertTrue(justAMomentPage.isContentLoaded());
    }
}