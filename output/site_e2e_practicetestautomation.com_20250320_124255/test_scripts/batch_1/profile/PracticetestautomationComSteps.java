
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class PracticeTestAutomationSteps {
    PracticeTestAutomationPage practicePage = new PracticeTestAutomationPage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        practicePage.navigateTo(url);
        Assert.assertTrue(practicePage.isPageLoaded());
    }

    @Then("user expects that the page title is {string}")
    public void userExpectsPageTitle(String expectedTitle) {
        Assert.assertEquals(expectedTitle, practicePage.getPageTitle());
    }

    @When("user clicks on the navigation link {string}")
    public void userClicksOnNavigationLink(String linkText) {
        practicePage.clickNavigationLink(linkText);
    }

    @Then("user expects that the current URL is {string}")
    public void userExpectsCurrentURL(String expectedURL) {
        Assert.assertEquals(expectedURL, practicePage.getCurrentURL());
    }

    @When("user clicks on the profile image")
    public void userClicksOnProfileImage() {
        practicePage.clickProfileImage();
    }

    @Then("user expects that the profile information is displayed")
    public void userExpectsProfileInformationDisplayed() {
        Assert.assertTrue(practicePage.isProfileInfoDisplayed());
    }

    @Then("user verifies that the greeting {string} is present on screen")
    public void userVerifiesGreetingPresent(String greeting) {
        Assert.assertTrue(practicePage.isGreetingPresent(greeting));
    }

    @Then("user verifies that the introduction text is displayed correctly")
    public void userVerifiesIntroductionTextDisplayed() {
        Assert.assertTrue(practicePage.isIntroductionTextDisplayed());
    }

    @When("user resizes the browser to {string}")
    public void userResizesBrowser(String size) {
        practicePage.resizeBrowser(size);
    }

    @Then("user expects that the navigation links are accessible")
    public void userExpectsNavigationLinksAccessible() {
        Assert.assertTrue(practicePage.areNavigationLinksAccessible());
    }

    @Then("user expects that the full layout is displayed correctly")
    public void userExpectsFullLayoutDisplayed() {
        Assert.assertTrue(practicePage.isFullLayoutDisplayed());
    }
