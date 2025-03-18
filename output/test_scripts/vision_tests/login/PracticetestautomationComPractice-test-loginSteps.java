
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class PracticeTestLoginSteps {

    PracticeTestLoginPage loginPage = new PracticeTestLoginPage();

    @Given("I navigate to the page URL {string}")
    public void iNavigateToThePageURL(String url) {
        loginPage.navigateTo(url);
    }

    @Then("I verify that the page title is {string}")
    public void iVerifyThatThePageTitleIs(String title) {
        String actualTitle = loginPage.getPageTitle();
        Assert.assertEquals(title, actualTitle);
    }

    @Given("I check that the 'username' input field is present and enabled")
    public void iCheckThatTheUsernameInputFieldIsPresentAndEnabled() {
        Assert.assertTrue(loginPage.isUsernameFieldPresentAndEnabled());
    }

    @When("I enter a valid username into the 'username' input field")
    public void iEnterAValidUsernameIntoTheUsernameInputField() {
        String validUsername = "testUser"; // Example username
        loginPage.enterUsername(validUsername);
    }

    @Then("I expect that the 'username' input field contains the entered username")
    public void iExpectThatTheUsernameInputFieldContainsTheEnteredUsername() {
        String expectedUsername = "testUser";
        String actualUsername = loginPage.getUsernameValue();
        Assert.assertEquals(expectedUsername, actualUsername);
    }

    @Given("I check that the 'submit' button is present and enabled")
    public void iCheckThatTheSubmitButtonIsPresentAndEnabled() {
        Assert.assertTrue(loginPage.isSubmitButtonPresentAndEnabled());
    }

    @When("I click on the 'submit' button")
    public void iClickOnTheSubmitButton() {
        loginPage.clickSubmitButton();
    }

    @Then("I expect that I am redirected to the appropriate page with a success message")
    public void iExpectThatIRedirectedToTheAppropriatePageWithASuccessMessage() {
        Assert.assertTrue(loginPage.isRedirectedToSuccessPage());
    }

    @Given("I click on the 'toggle-navigation' button")
    public void iClickOnTheToggleNavigationButton() {
        loginPage.clickToggleNavigation();
    }

    @Then("I expect that the navigation menu appears")
    public void iExpectThatTheNavigationMenuAppears() {
        Assert.assertTrue(loginPage.isNavigationMenuVisible());
    }

    @When("I click on the 'toggle-navigation' button again")
    public void iClickOnTheToggleNavigationButtonAgain() {
        loginPage.clickToggleNavigation();
    }

    @Then("I expect that the navigation menu disappears")
    public void iExpectThatTheNavigationMenuDisappears() {
        Assert.assertFalse(loginPage.isNavigationMenuVisible());
    }

    @When("I enter an invalid username into the 'username' input field")
    public void iEnterAnInvalidUsernameIntoTheUsernameInputField() {
        String invalidUsername = "invalidUser";
        loginPage.enterUsername(invalidUsername);
    }

    @Then("I expect to see an appropriate error message")
    public void iExpectToSeeAnAppropriateErrorMessage() {
        Assert.assertTrue(loginPage.isErrorMessageDisplayed());
    }
	