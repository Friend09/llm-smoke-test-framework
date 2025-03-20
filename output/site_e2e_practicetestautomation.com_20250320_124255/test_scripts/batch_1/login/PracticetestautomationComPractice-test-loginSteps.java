
import io.cucumber.java.en.*;
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

    @When("user clicks the submit button")
    public void userClicksSubmitButton() {
        loginPage.clickSubmit();
    }

    @Then("user should see a successful login message")
    public void userShouldSeeSuccessfulLoginMessage() {
        Assert.assertTrue(loginPage.isLoginSuccessful());
    }

    @Then("user should see an error message")
    public void userShouldSeeErrorMessage() {
        Assert.assertTrue(loginPage.isErrorDisplayed());
    }

    @Then("user should see error messages for empty fields")
    public void userShouldSeeErrorMessagesForEmptyFields() {
        Assert.assertTrue(loginPage.isEmptyFieldErrorDisplayed());
    }

    @Then("the username field should be active")
    public void usernameFieldShouldBeActive() {
        Assert.assertTrue(loginPage.isUsernameFieldActive());
    }

    @Then("the password field should be active")
    public void passwordFieldShouldBeActive() {
        Assert.assertTrue(loginPage.isPasswordFieldActive());
    }
}