
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class TestExceptionsSteps {

    private TestExceptionsPage testExceptionsPage;

    public TestExceptionsSteps() {
        testExceptionsPage = new TestExceptionsPage();
    }

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        testExceptionsPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        testExceptionsPage.openURL(url);
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitleIs(String title) {
        Assert.assertEquals(title, testExceptionsPage.getPageTitle());
    }

    @Then("user verifies element {string} is present on screen")
    public void userVerifiesElementIsPresentOnScreen(String element) {
        Assert.assertTrue(testExceptionsPage.isElementPresent(element));
    }
}
