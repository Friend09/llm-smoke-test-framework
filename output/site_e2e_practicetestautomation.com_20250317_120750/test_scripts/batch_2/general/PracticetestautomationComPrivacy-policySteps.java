
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class PrivacyPolicySteps {

    private PrivacyPolicyPage privacyPolicyPage;

    public PrivacyPolicySteps() {
        privacyPolicyPage = new PrivacyPolicyPage();
    }

    @Given("user launches browser in {string}")
    public void user_launches_browser_in(String browser) {
        privacyPolicyPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void user_opens_URL(String url) {
        privacyPolicyPage.openUrl(url);
    }

    @Then("user verifies the page title is {string}")
    public void user_verifies_the_page_title_is(String expectedTitle) {
        String actualTitle = privacyPolicyPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the element {string} is present on screen")
    public void user_verifies_the_element_is_present_on_screen(String element) {
        Assert.assertTrue(privacyPolicyPage.isElementPresent(element));
    }

    @Then("user verifies that the content includes the text {string}")
    public void user_verifies_that_the_content_includes_the_text(String text) {
        Assert.assertTrue(privacyPolicyPage.isTextPresent(text));
    }
}
	