
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class PracticeTestSteps {

    private PracticeTestPage practiceTestPage = new PracticeTestPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        practiceTestPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        practiceTestPage.openUrl(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        String actualTitle = practiceTestPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the heading {string} is present on screen")
    public void userVerifiesHeadingIsPresent(String heading) {
        Assert.assertTrue(practiceTestPage.isHeadingPresent(heading));
    }

    @When("user clicks on the link {string}")
    public void userClicksOnTheLink(String linkText) {
        practiceTestPage.clickLink(linkText);
    }

    @Then("user verifies the page title contains {string}")
    public void userVerifiesThePageTitleContains(String partialTitle) {
        String actualTitle = practiceTestPage.getPageTitle();
        Assert.assertTrue(actualTitle.contains(partialTitle));
    }

    @Then("user verifies that at least one blog post is displayed on screen")
    public void userVerifiesThatAtLeastOneBlogPostIsDisplayed() {
        Assert.assertTrue(practiceTestPage.isBlogPostDisplayed());
    }

    @Then("user verifies that at least one course is displayed on screen")
    public void userVerifiesThatAtLeastOneCourseIsDisplayed() {
        Assert.assertTrue(practiceTestPage.isCourseDisplayed());
    }

    @Then("user scrolls to the footer")
    public void userScrollsToTheFooter() {
        practiceTestPage.scrollToFooter();
    }

    @Then("user verifies the link {string} is present")
    public void userVerifiesTheLinkIsPresent(String linkText) {
        Assert.assertTrue(practiceTestPage.isLinkPresent(linkText));
    }
	