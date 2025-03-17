
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class LoginPageSteps {
    
    private LoginPage loginPage = new LoginPage();

    @Given("user opens the URL {string}")
    public void userOpensTheURL(String url) {
        loginPage.navigateTo(url);
        Assert.assertTrue(loginPage.isPageLoaded());
    }

    @When("user enters {string} into the username field")
    public void userEntersIntoTheUsernameField(String username) {
        loginPage.enterUsername(username);
    }

    @When("user enters {string} into the password field")
    public void userEntersIntoThePasswordField(String password) {
        loginPage.enterPassword(password);
    }

    @When("user clicks the login button")
    public void userClicksTheLoginButton() {
        loginPage.clickLoginButton();
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        Assert.assertEquals(expectedTitle, loginPage.getPageTitle());
    }

    @Then("user verifies the message {string} is present on the screen")
    public void userVerifiesTheMessageIsPresentOnTheScreen(String expectedMessage) {
        Assert.assertTrue(loginPage.isMessageDisplayed(expectedMessage));
    }
}
	