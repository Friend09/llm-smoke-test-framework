
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage {
    private WebDriver driver;

    // Locators
    private By usernameField = By.id("username");
    private By passwordField = By.id("password");
    private By loginButton = By.id("submit");
    private By message = By.id("message");
    
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

    public void clickLoginButton() {
        driver.findElement(loginButton).click();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isMessageDisplayed(String expectedMessage) {
        return driver.findElement(message).getText().contains(expectedMessage);
    }
}
	