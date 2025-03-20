
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class PracticePageSteps {

    PracticePage practicePage = new PracticePage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        practicePage.navigateTo(url);
        Assert.assertTrue(practicePage.isPageLoaded());
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitle(String title) {
        Assert.assertEquals(title, practicePage.getPageTitle());
    }

    @Then("user verifies the link {string} is present and clickable")
    public void userVerifiesLinkIsPresentAndClickable(String linkText) {
        Assert.assertTrue(practicePage.isLinkPresent(linkText));
        practicePage.clickLink(linkText);
    }

    @When("user clicks on the link {string}")
    public void userClicksOnTheLink(String linkText) {
        practicePage.clickLink(linkText);
    }

    @Then("user verifies the current URL is {string}")
    public void userVerifiesCurrentURL(String expectedUrl) {
        Assert.assertEquals(expectedUrl, practicePage.getCurrentURL());
    }

    @Then("user verifies the title contains {string}")
    public void userVerifiesTitleContains(String titlePart) {
        Assert.assertTrue(practicePage.getPageTitle().contains(titlePart));
    }

    @When("user clicks on the toggle navigation button")
    public void userClicksOnTheToggleNavigationButton() {
        practicePage.clickToggleNavigation();
    }

    @Then("user verifies that the navigation menu is displayed")
    public void userVerifiesNavigationMenuIsDisplayed() {
        Assert.assertTrue(practicePage.isNavigationMenuDisplayed());
    }

    @Then("user verifies that the navigation menu is hidden")
    public void userVerifiesNavigationMenuIsHidden() {
        Assert.assertFalse(practicePage.isNavigationMenuDisplayed());
    }
	