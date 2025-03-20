
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class CoursesPageSteps {
    private CoursesPage coursesPage = new CoursesPage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        coursesPage.navigateTo(url);
        Assert.assertTrue(coursesPage.isPageLoaded());
    }

    @Then("I expect that the page title is {string}")
    public void iExpectThatThePageTitleIs(String expectedTitle) {
        Assert.assertEquals(expectedTitle, coursesPage.getPageTitle());
    }

    @Then("I verify that the page loads successfully with a {int} HTTP response status")
    public void iVerifyThatThePageLoadsSuccessfully(int statusCode) {
        Assert.assertEquals(statusCode, coursesPage.getHTTPResponseStatus());
    }

    @When("user clicks on the navigation toggle button")
    public void userClicksOnTheNavigationToggleButton() {
        coursesPage.clickNavigationToggle();
    }

    @Then("I expect that the navigation menu is displayed")
    public void iExpectThatTheNavigationMenuIsDisplayed() {
        Assert.assertTrue(coursesPage.isNavigationMenuDisplayed());
    }

    @When("user enters valid first name {string} in the input field with id {string}")
    public void userEntersValidFirstName(String firstName, String fieldId) {
        coursesPage.enterFirstName(firstName, fieldId);
    }

    @Then("I expect that the first name input is accepted")
    public void iExpectThatTheFirstNameInputIsAccepted() {
        Assert.assertTrue(coursesPage.isFirstNameAccepted());
    }

    @When("user enters invalid email {string} in the input field with id {string}")
    public void userEntersInvalidEmail(String email, String fieldId) {
        coursesPage.enterEmail(email, fieldId);
    }

    @Then("I expect that an error message is displayed for invalid email format")
    public void iExpectThatAnErrorMessageIsDisplayed() {
        Assert.assertTrue(coursesPage.isEmailErrorDisplayed());
    }

    @When("user enters valid email {string} in the input field with id {string}")
    public void userEntersValidEmail(String email, String fieldId) {
        coursesPage.enterEmail(email, fieldId);
    }

    @Then("I expect that the email input is accepted")
    public void iExpectThatTheEmailInputIsAccepted() {
        Assert.assertTrue(coursesPage.isEmailAccepted());
    }
