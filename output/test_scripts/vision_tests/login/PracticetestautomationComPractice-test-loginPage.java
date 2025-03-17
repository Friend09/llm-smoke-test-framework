
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {
    private WebDriver driver;

    public LoginPage(WebDriver driver) {
        this.driver = driver;
    }

    public void open() {
        driver.get("https://practicetestautomation.com/practice-test-login/");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isUsernameFieldPresentAndEnabled() {
        return driver.findElement(By.id("username")).isDisplayed() && driver.findElement(By.id("username")).isEnabled();
    }

    public void enterUsername(String username) {
        driver.findElement(By.id("username")).sendKeys(username);
    }

    public void enterPassword(String password) {
        driver.findElement(By.id("password")).sendKeys(password);
    }

    public void clickButton(String buttonId) {
        driver.findElement(By.id(buttonId)).click();
    }

    public boolean isErrorMessageDisplayedForEmptyFields() {
        // Implement logic to check for empty field error messages
        return true; // Placeholder
    }

    public boolean isErrorMessageDisplayedForIncorrectCredentials() {
        // Implement logic to check for incorrect credentials error messages
        return true; // Placeholder
    }

    public boolean isSuccessMessageDisplayed() {
        // Implement logic to check for success messages
        return true; // Placeholder
    }

    public void clickToggleNavigation() {
        driver.findElement(By.id("toggle-navigation")).click();
    }

    public boolean isNavigationMenuExpandedOrCollapsed() {
        // Implement logic to check the state of the navigation menu
        return true; // Placeholder
    }
}
