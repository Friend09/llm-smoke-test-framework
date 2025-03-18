
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class PracticeTestLoginPage {
    WebDriver driver;

    // Locators
    private By usernameField = By.id("username");
    private By submitButton = By.id("submit");
    private By toggleNavigationButton = By.id("toggle-navigation");
    private By errorMessage = By.id("error-message"); // Assume id for error message

    public PracticeTestLoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isUsernameFieldPresentAndEnabled() {
        return driver.findElement(usernameField).isDisplayed() && driver.findElement(usernameField).isEnabled();
    }

    public void enterUsername(String username) {
        driver.findElement(usernameField).clear(); // Clear the field before entering
        driver.findElement(usernameField).sendKeys(username);
    }

    public String getUsernameValue() {
        return driver.findElement(usernameField).getAttribute("value");
    }

    public boolean isSubmitButtonPresentAndEnabled() {
        return driver.findElement(submitButton).isDisplayed() && driver.findElement(submitButton).isEnabled();
    }

    public void clickSubmitButton() {
        driver.findElement(submitButton).click();
    }

    public boolean isRedirectedToSuccessPage() {
        // Implement logic to verify redirection
        // This could be checking the URL or checking for a success element
        return true;
    }

    public void clickToggleNavigation() {
        driver.findElement(toggleNavigationButton).click();
    }

    public boolean isNavigationMenuVisible() {
        // Implement logic to check if the navigation menu is visible
        return true;
    }

    public boolean isErrorMessageDisplayed() {
        return driver.findElement(errorMessage).isDisplayed();
    }
	