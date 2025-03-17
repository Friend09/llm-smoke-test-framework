import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class ContactPageSteps {

    private ContactPage contactPage;

    public ContactPageSteps() {
        contactPage = new ContactPage();
    }

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        contactPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        contactPage.navigateTo(url);
    }

    @Then("user verifies the title is {string}")
    public void userVerifiesTheTitleIs(String expectedTitle) {
        String actualTitle = contactPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies {string} input field is present on screen")
    public void userVerifiesInputFieldIsPresent(String fieldName) {
        Assert.assertTrue(contactPage.isInputFieldPresent(fieldName));
    }

    @Then("user verifies {string} text area is present on screen")
    public void userVerifiesTextAreaIsPresent(String areaName) {
        Assert.assertTrue(contactPage.isTextAreaPresent(areaName));
    }

    @Then("user verifies {string} button is present on screen")
    public void userVerifiesButtonIsPresent(String buttonName) {
        Assert.assertTrue(contactPage.isButtonPresent(buttonName));
    }

    @When("user enters {string} into the input field {string}")
    public void userEntersIntoInputField(String value, String fieldName) {
        contactPage.enterValueInInputField(value, fieldName);
    }

    @When("user clicks on the button {string}")
    public void userClicksOnButton(String buttonName) {
        contactPage.clickButton(buttonName);
    }

    @Then("user verifies success message is displayed on screen")
    public void userVerifiesSuccessMessage() {
        Assert.assertTrue(contactPage.isSuccessMessageDisplayed());
    }
}