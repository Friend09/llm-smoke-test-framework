
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class PracticePageSteps {
    PracticePage practicePage = new PracticePage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        practicePage.navigateTo(url);
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitleIs(String expectedTitle) {
        String actualTitle = practicePage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the button with ID {string} is visible and clickable")
    public void userVerifiesButtonIsVisibleAndClickable(String buttonId) {
        Assert.assertTrue(practicePage.isButtonVisibleAndClickable(buttonId));
    }

    @When("user clicks on the link {string}")
    public void userClicksOnTheLink(String linkText) {
        practicePage.clickLink(linkText);
    }

    @Then("user expects to be redirected to the homepage")
    public void userExpectsToBeRedirectedToHomepage() {
        Assert.assertEquals("https://practicetestautomation.com/", practicePage.getCurrentUrl());
    }

    @Then("user expects to remain on the practice page")
    public void userExpectsToRemainOnThePracticePage() {
        Assert.assertEquals("https://practicetestautomation.com/practice/", practicePage.getCurrentUrl());
    }

    @Then("user expects to see content for {string}")
    public void userExpectsToSeeContentFor(String content) {
        Assert.assertTrue(practicePage.isContentDisplayed(content));
    }
}