
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class SmokeTestSteps {

    private final Page page = new Page();

    @Given("user navigates to the page {string}")
    public void userNavigatesToThePage(String url) {
        page.navigateTo(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        String actualTitle = page.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the page contains a loading message")
    public void userVerifiesThePageContainsLoadingMessage() {
        Assert.assertTrue(page.isLoadingMessageDisplayed());
    }

    @When("user waits for the loading to complete")
    public void userWaitsForTheLoadingToComplete() {
        page.waitForLoading();
    }

    @Then("user verifies the expected content is displayed after loading")
    public void userVerifiesExpectedContentDisplayedAfterLoading() {
        Assert.assertTrue(page.isExpectedContentDisplayed());
    }
}