
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class CoursesPageSteps {
    
    private CoursesPage coursesPage = new CoursesPage();

    @Given("I navigate to the courses page")
    public void iNavigateToTheCoursesPage() {
        coursesPage.navigateTo();
        Assert.assertTrue(coursesPage.isPageLoaded());
    }

    @Then("I expect the page title to be {string}")
    public void iExpectThePageTitleToBe(String expectedTitle) {
        String actualTitle = coursesPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("I expect the page URL to be {string}")
    public void iExpectThePageURLToBe(String expectedURL) {
        String actualURL = coursesPage.getPageURL();
        Assert.assertEquals(expectedURL, actualURL);
    }

    @When("I click on the navigation toggle button")
    public void iClickOnTheNavigationToggleButton() {
        coursesPage.clickNavigationToggle();
    }

    @Then("I expect the navigation menu to be visible")
    public void iExpectTheNavigationMenuToBeVisible() {
        Assert.assertTrue(coursesPage.isNavigationMenuVisible());
    }

    @When("I click on the first name input field")
    public void iClickOnTheFirstNameInputField() {
        coursesPage.clickFirstNameInputField();
    }

    @Then("I expect the first name input field to be editable")
    public void iExpectTheFirstNameInputFieldToBeEditable() {
        Assert.assertTrue(coursesPage.isFirstNameInputEditable());
    }

    @Then("I expect the first name input field to accept text input")
    public void iExpectTheFirstNameInputFieldToAcceptTextInput() {
        Assert.assertTrue(coursesPage.canInputTextInFirstNameField());
    }

    @When("I click on the email input field")
    public void iClickOnTheEmailInputField() {
        coursesPage.clickEmailInputField();
    }

    @Then("I expect the email input field to be editable")
    public void iExpectTheEmailInputFieldToBeEditable() {
        Assert.assertTrue(coursesPage.isEmailInputEditable());
    }

    @Then("I expect the email input field to accept valid email formats")
    public void iExpectTheEmailInputFieldToAcceptValidEmailFormats() {
        Assert.assertTrue(coursesPage.isEmailInputAcceptingValidFormats());
    }

    @Then("I expect the email input field to display appropriate placeholder text")
    public void iExpectTheEmailInputFieldToDisplayAppropriatePlaceholderText() {
        String placeholder = coursesPage.getEmailInputPlaceholder();
        Assert.assertEquals("Enter your email", placeholder); // Change as per actual placeholder
    }
}