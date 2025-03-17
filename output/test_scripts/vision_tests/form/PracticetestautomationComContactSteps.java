import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class ContactPageSteps {
    ContactPage contactPage = new ContactPage();

    @Given("user opens the contact page")
    public void userOpensTheContactPage() {
        contactPage.navigateToContactPage();
        Assert.assertTrue(contactPage.isPageLoaded());
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        Assert.assertEquals(expectedTitle, contactPage.getPageTitle());
    }

    @Then("user verifies the {string} input field is present")
    public void userVerifiesInputFieldIsPresent(String fieldName) {
        Assert.assertTrue(contactPage.isInputFieldPresent(fieldName));
    }

    @When("user enters {string} into the {string} field")
    public void userEntersIntoField(String value, String fieldName) {
        contactPage.enterValueIntoField(fieldName, value);
    }

    @When("user clicks on the {string} button")
    public void userClicksOnButton(String buttonName) {
        contactPage.clickButton(buttonName);
    }

    @Then("user verifies that the submission is successful")
    public void userVerifiesSubmissionIsSuccessful() {
        Assert.assertTrue(contactPage.isSuccessMessageDisplayed());
    }

    @Then("user verifies that the validation message for the {string} field is displayed")
    public void userVerifiesValidationMessageForFieldIsDisplayed(String fieldName) {
        Assert.assertTrue(contactPage.isValidationMessageDisplayed(fieldName));
    }

    @When("user clicks on the {string} navigation link")
    public void userClicksOnNavigationLink(String linkName) {
        contactPage.clickNavigationLink(linkName);
    }

    @Then("user verifies that the user is navigated to the {string} page")
    public void userVerifiesNavigationToPage(String expectedPage) {
        Assert.assertTrue(contactPage.isNavigatedTo(expectedPage));
    }
}