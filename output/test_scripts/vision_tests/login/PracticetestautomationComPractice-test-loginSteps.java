import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class LoginSteps {
    LoginPage loginPage = new LoginPage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        loginPage.navigateTo(url);
        Assert.assertTrue(loginPage.isPageLoaded());
    }

    @When("user enters {string} into the username field")
    public void userEntersIntoUsernameField(String username) {
        loginPage.enterUsername(username);
    }

    @When("user enters {string} into the password field")
    public void userEntersIntoPasswordField(String password) {
        loginPage.enterPassword(password);
    }

    @When("user clicks on the Submit button")
    public void userClicksOnSubmitButton() {
        loginPage.clickSubmit();
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitleIs(String title) {
        Assert.assertEquals(title, loginPage.getPageTitle());
    }

    @Then("user expects to see a successful login message")
    public void userExpectsToSeeSuccessfulLoginMessage() {
        Assert.assertTrue(loginPage.isSuccessfulLoginMessageDisplayed());
    }

    @Then("user expects to see an error message")
    public void userExpectsToSeeErrorMessage() {
        Assert.assertTrue(loginPage.isErrorMessageDisplayed());
    }

    @Then("user expects to see validation messages for required fields")
    public void userExpectsValidationMessages() {
        Assert.assertTrue(loginPage.areValidationMessagesDisplayed());
    }

    @Then("user expects appropriate validation messages for input limits")
    public void userExpectsValidationMessagesForInputLimits() {
        Assert.assertTrue(loginPage.isInputLengthValidationMessageDisplayed());
    }

    @When("user clicks on the password visibility toggle")
    public void userClicksOnPasswordVisibilityToggle() {
        loginPage.togglePasswordVisibility();
    }

    @Then("user expects the password to be visible")
    public void userExpectsPasswordToBeVisible() {
        Assert.assertTrue(loginPage.isPasswordVisible());
    }
}