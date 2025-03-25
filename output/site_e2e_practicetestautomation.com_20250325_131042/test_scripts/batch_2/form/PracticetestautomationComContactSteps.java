
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class ContactFormSteps {
    
    ContactPage contactPage = new ContactPage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        contactPage.navigateTo(url);
        Assert.assertTrue("Page did not load correctly.", contactPage.isPageLoaded());
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesPageTitle(String expectedTitle) {
        String actualTitle = contactPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @When("user submits the form without filling any fields")
    public void userSubmitsEmptyForm() {
        contactPage.clickSubmitButton();
    }

    @Then("user verifies the validation messages are displayed")
    public void userVerifiesValidationMessages() {
        Assert.assertTrue(contactPage.isValidationMessagesDisplayed());
    }

    @When("user enters {string} into the first name input field")
    public void userEntersFirstName(String firstName) {
        contactPage.enterFirstName(firstName);
    }

    @When("user enters {string} into the last name input field")
    public void userEntersLastName(String lastName) {
        contactPage.enterLastName(lastName);
    }

    @When("user enters {string} into the email input field")
    public void userEntersEmail(String email) {
        contactPage.enterEmail(email);
    }

    @When("user enters {string} into the message input field")
    public void userEntersMessage(String message) {
        contactPage.enterMessage(message);
    }

    @When("user clicks the submit button")
    public void userClicksSubmitButton() {
        contactPage.clickSubmitButton();
    }

    @Then("user verifies a successful submission acknowledgment is displayed")
    public void userVerifiesSubmissionAcknowledgment() {
        Assert.assertTrue(contactPage.isSubmissionAcknowledgmentDisplayed());
    }

    @Then("user verifies the appropriate error message for invalid email is displayed")
    public void userVerifiesInvalidEmailError() {
        Assert.assertTrue(contactPage.isInvalidEmailErrorDisplayed());
    }

    @Then("user verifies the appropriate error message for message length is displayed")
    public void userVerifiesMessageLengthError() {
        Assert.assertTrue(contactPage.isMessageLengthErrorDisplayed());
    }

    @Then("user verifies the URL is correct for the {string} page")
    public void userVerifiesPageURL(String page) {
        Assert.assertTrue(contactPage.isCorrectPageURL(page));
    }
}