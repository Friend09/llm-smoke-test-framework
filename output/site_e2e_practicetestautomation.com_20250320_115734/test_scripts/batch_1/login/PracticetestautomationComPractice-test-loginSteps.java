
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class PracticeTestSteps {
    
    PracticeTestLoginPage loginPage = new PracticeTestLoginPage();

    @Given("user opens the URL {string}")
    public void userOpensTheUrl(String url) {
        loginPage.navigateTo(url);
        Assert.assertTrue(loginPage.isPageLoaded());
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitle(String expectedTitle) {
        String actualTitle = loginPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }
    
    @Then("user verifies the username input field is present")
    public void userVerifiesUsernameInputFieldIsPresent() {
        Assert.assertTrue(loginPage.isUsernameFieldPresent());
    }

    @Then("user verifies the submit button is visible")
    public void userVerifiesSubmitButtonIsVisible() {
        Assert.assertTrue(loginPage.isSubmitButtonVisible());
    }

    @Then("user verifies the toggle navigation button is visible")
    public void userVerifiesToggleNavigationButtonIsVisible() {
        Assert.assertTrue(loginPage.isToggleNavigationButtonVisible());
    }

    @When("user enters {string} into the username field")
    public void userEntersIntoTheUsernameField(String username) {
        loginPage.enterUsername(username);
    }

    @Then("user verifies that the username input is accepted")
    public void userVerifiesUsernameInputIsAccepted() {
        Assert.assertTrue(loginPage.isUsernameInputAccepted());
    }
  