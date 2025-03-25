
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class LoginPage {
    private WebDriver driver;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Test Login | Practice Test Automation");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isUsernameFieldPresent() {
        return isElementPresent(By.id("username"));
    }

    public boolean isPasswordFieldPresent() {
        return isElementPresent(By.id("password"));
    }

    public boolean isSubmitButtonPresent() {
        return isElementPresent(By.id("submit"));
    }

    public void enterUsername(String username) {
        WebElement usernameField = driver.findElement(By.id("username"));
        usernameField.clear();
        usernameField.sendKeys(username);
    }

    public void enterPassword(String password) {
        WebElement passwordField = driver.findElement(By.id("password"));
        passwordField.clear();
        passwordField.sendKeys(password);
    }

    public void clickSubmitButton() {
        driver.findElement(By.id("submit")).click();
    }

    public boolean isLoginSuccessful() {
        // Implement logic to verify successful login
        return true; // Placeholder
    }

    public boolean isValidationMessageDisplayed() {
        // Implement logic to verify validation messages
        return true; // Placeholder
    }

    private boolean isElementPresent(By locator) {
        return driver.findElements(locator).size() > 0;
    }
}