// Step Definitions for Java for Testers Page

import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class JavaForTestersSteps {
    private JavaForTestersPage javaForTestersPage = new JavaForTestersPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        javaForTestersPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        javaForTestersPage.openURL(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        String actualTitle = javaForTestersPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies that the page is accessible")
    public void userVerifiesThatThePageIsAccessible() {
        Assert.assertTrue(javaForTestersPage.isPageAccessible());
    }
}