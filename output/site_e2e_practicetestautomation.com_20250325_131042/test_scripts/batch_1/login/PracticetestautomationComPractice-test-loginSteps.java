
import io.cucumber.java.en.*;
import org.junit.Assert;

public class LoginPageSteps {
    LoginPage loginPage = new LoginPage();

    @Given("user opens the URL {string}")
    public void userOpensTheURL(String url) {
        loginPage.navigateTo(url);
        Assert.assertTrue(loginPage.isPageLoaded());
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        Assert.assertEquals(expectedTitle, loginPage.getPageTitle());
    }

    @Then("user verifies the username input field is present")
    public void userVerifiesUsernameInputFieldIsPresent() {
        Assert.assertTrue(loginPage.isUsernameFieldPresent());
    }

    @Then("user verifies the password input field is present")
    public void userVerifiesPasswordInputFieldIsPresent() {
        Assert.assertTrue(loginPage.isPasswordFieldPresent());
    }

    @Then("user verifies the submit button is present")
    public void userVerifiesSubmitButtonIsPresent() {
        Assert.assertTrue(loginPage.isSubmitButtonPresent());
    }

    @When("user enters {string} into the username input field")
    public void userEntersIntoUsernameInputField(String username) {
        loginPage.enterUsername(username);
    }

    @When("user enters {string} into the password input field")
    public void userEntersIntoPasswordInputField(String password) {
        loginPage.enterPassword(password);
    }

    @When("user clicks the submit button")
    public void userClicksTheSubmitButton() {
        loginPage.clickSubmitButton();
    }

    @Then("user expects to see a successful login message or redirection")
    public void userExpectsToSeeSuccessfulLogin() {
        Assert.assertTrue(loginPage.isLoginSuccessful());
    }

    @When("user clicks the submit button without entering credentials")
    public void userClicksSubmitButtonWithoutCredentials() {
        loginPage.clickSubmitButton();
    }

    @Then("user expects to see validation messages for empty fields")
    public void userExpectsToSeeValidationMessages() {
        Assert.assertTrue(loginPage.isValidationMessageDisplayed());
    }
}