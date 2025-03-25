import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class PracticeTestAutomationSteps {
    PracticeTestAutomationPage practicePage = new PracticeTestAutomationPage();

    @Given("user opens the page {string}")
    public void userOpensThePage(String url) {
        practicePage.navigateTo(url);
        Assert.assertTrue(practicePage.isPageLoaded());
    }

    @Then("user verifies that the page title is {string}")
    public void userVerifiesThatThePageTitleIs(String expectedTitle) {
        String actualTitle = practicePage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the navigation button is displayed and clickable")
    public void userVerifiesTheNavigationButton() {
        Assert.assertTrue(practicePage.isToggleNavigationButtonDisplayed());
        Assert.assertTrue(practicePage.isToggleNavigationButtonClickable());
    }

    @When("user enters {string} into the input field with ID {string}")
    public void userEntersIntoInputField(String value, String fieldId) {
        practicePage.enterValueIntoField(value, fieldId);
    }

    @Then("user verifies that all links on the page are functioning correctly")
    public void userVerifiesLinks() {
        Assert.assertTrue(practicePage.areAllLinksWorking());
    }

    @Then("user checks that the header section is visible")
    public void userChecksHeaderSection() {
        Assert.assertTrue(practicePage.isHeaderVisible());
    }

    @Then("user checks that the experience and expertise section is visible")
    public void userChecksExperienceSection() {
        Assert.assertTrue(practicePage.isExperienceSectionVisible());
    }
}