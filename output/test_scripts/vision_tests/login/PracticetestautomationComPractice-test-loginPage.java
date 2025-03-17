import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class LoginPage {
    private WebDriver driver;
    private WebDriverWait wait;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Test Login | Practice Test Automation");
    }

    public void enterUsername(String username) {
        WebElement usernameField = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("username")));
        usernameField.clear();
        usernameField.sendKeys(username);
    }

    public void enterPassword(String password) {
        WebElement passwordField = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("password")));
        passwordField.clear();
        passwordField.sendKeys(password);
    }

    public void clickSubmit() {
        WebElement submitButton = wait.until(ExpectedConditions.elementToBeClickable(By.id("submit")));
        submitButton.click();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isSuccessfulLoginMessageDisplayed() {
        // Check for successful login message logic here
        return true;
    }

    public boolean isErrorMessageDisplayed() {
        // Check for error message logic here
        return true;
    }

    public boolean areValidationMessagesDisplayed() {
        // Check for validation messages logic here
        return true;
    }

    public boolean isInputLengthValidationMessageDisplayed() {
        // Check for input length validation message logic here
        return true;
    }

    public void togglePasswordVisibility() {
        // Logic to toggle password visibility here
    }

    public boolean isPasswordVisible() {
        // Logic to check if password is visible
        return true;
    }
}