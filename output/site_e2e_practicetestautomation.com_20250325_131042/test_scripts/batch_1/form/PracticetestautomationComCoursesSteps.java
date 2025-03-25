
import io.cucumber.java.en.*;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CoursesPageSteps {
    private WebDriver driver;
    private CoursesPage coursesPage;

    public CoursesPageSteps() {
        this.driver = DriverManager.getDriver(); // Assuming a DriverManager class for WebDriver instance
        this.coursesPage = new CoursesPage(driver);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        driver.get(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesPageTitle(String expectedTitle) {
        Assert.assertEquals(expectedTitle, driver.getTitle());
    }

    @Then("user verifies the current URL is {string}")
    public void userVerifiesCurrentURL(String expectedURL) {
        Assert.assertEquals(expectedURL, driver.getCurrentUrl());
    }

    @When("user clicks on the navigation button {string}")
    public void userClicksOnNavigationButton(String buttonId) {
        coursesPage.clickToggleNavigationButton();
    }

    @Then("user verifies the navigation menu appears")
    public void userVerifiesNavigationMenuAppears() {
        Assert.assertTrue(coursesPage.isNavigationMenuVisible());
    }

    @Then("user verifies the first name input field is present")
    public void userVerifiesFirstNameInputFieldIsPresent() {
        Assert.assertTrue(coursesPage.isFirstNameInputPresent());
    }

    @Then("user enters {string} into the first name input field")
    public void userEntersIntoFirstNameInputField(String firstName) {
        coursesPage.enterFirstName(firstName);
    }

    @Then("user verifies the email input field is present")
    public void userVerifiesEmailInputFieldIsPresent() {
        Assert.assertTrue(coursesPage.isEmailInputPresent());
    }

    @Then("user enters {string} into the email input field")
    public void userEntersIntoEmailInputField(String email) {
        coursesPage.enterEmail(email);
    }

    @When("user submits the form")
    public void userSubmitsTheForm() {
        coursesPage.submitForm();
    }

    @Then("user verifies the validation message is displayed")
    public void userVerifiesValidationMessageIsDisplayed() {
        Assert.assertTrue(coursesPage.isValidationMessageDisplayed());
    }

    @Then("user verifies the appropriate validation messages are displayed")
    public void userVerifiesAppropriateValidationMessagesAreDisplayed() {
        Assert.assertTrue(coursesPage.areValidationMessagesDisplayed());
    }
	