
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class SeleniumGridSteps {

    private SeleniumGridPage seleniumGridPage = new SeleniumGridPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        seleniumGridPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        seleniumGridPage.openURL(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        String actualTitle = seleniumGridPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies that the text {string} is present on the screen")
    public void userVerifiesThatTheTextIsPresentOnTheScreen(String expectedText) {
        Assert.assertTrue(seleniumGridPage.isTextPresent(expectedText));
    }
}
	