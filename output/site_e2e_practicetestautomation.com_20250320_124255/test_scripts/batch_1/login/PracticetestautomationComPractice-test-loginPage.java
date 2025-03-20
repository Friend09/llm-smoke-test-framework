
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {
    private WebDriver driver;

    // Locators
    private By usernameField = By.id("username");
    private By passwordField = By.id("password");
    private By submitButton = By.id("submit");
    private By successMessage = By.id("welcome");
    private By errorMessage = By.id("error");
    
    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Test Login | Practice Test Automation");
    }

    public void enterUsername(String username) {
        driver.findElement(usernameField).sendKeys(username);
    }

    public void enterPassword(String password) {
        driver.findElement(passwordField).sendKeys(password);
    }

    public void clickSubmit() {
        driver.findElement(submitButton).click();
    }

    public boolean isLoginSuccessful() {
        return driver.findElement(successMessage).isDisplayed();
    }

    public boolean isErrorDisplayed() {
        return driver.findElement(errorMessage).isDisplayed();
    }

    public boolean isEmptyFieldErrorDisplayed() {
        // Implement logic to check for empty field error messages
        return true; // Placeholder
    }

    public boolean isUsernameFieldActive() {
        // Implement logic to check if the username field is active
        return true; // Placeholder
    }

    public boolean isPasswordFieldActive() {
        // Implement logic to check if the password field is active
        return true; // Placeholder
    }
}