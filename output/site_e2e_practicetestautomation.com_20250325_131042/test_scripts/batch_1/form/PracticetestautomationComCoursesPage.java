
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CoursesPage {
    private WebDriver driver;

    // Locators
    private By toggleNavigationButton = By.id("toggle-navigation");
    private By firstNameInput = By.id("form_first_name_8");
    private By emailInput = By.id("form_email_8");
    private By validationMessage = By.cssSelector(".validation-message"); // Example selector
    private By form = By.cssSelector("form"); // Example selector for the form

    public CoursesPage(WebDriver driver) {
        this.driver = driver;
    }

    public void clickToggleNavigationButton() {
        driver.findElement(toggleNavigationButton).click();
    }

    public boolean isNavigationMenuVisible() {
        // Implement visibility check for navigation menu
        return true; // Placeholder
    }

    public boolean isFirstNameInputPresent() {
        return driver.findElement(firstNameInput).isDisplayed();
    }

    public void enterFirstName(String firstName) {
        driver.findElement(firstNameInput).sendKeys(firstName);
    }

    public boolean isEmailInputPresent() {
        return driver.findElement(emailInput).isDisplayed();
    }

    public void enterEmail(String email) {
        driver.findElement(emailInput).sendKeys(email);
    }

    public void submitForm() {
        driver.findElement(form).submit(); // Assuming the form can be submitted this way
    }

    public boolean isValidationMessageDisplayed() {
        return driver.findElement(validationMessage).isDisplayed();
    }

    public boolean areValidationMessagesDisplayed() {
        // Logic to check for multiple validation messages
        return true; // Placeholder
    }
	