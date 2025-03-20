
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class PracticeTestLoginPage {
    private WebDriver driver;

    // Locators
    private By usernameField = By.id("username");
    private By submitButton = By.id("submit");
    private By toggleNavigationButton = By.id("toggle-navigation");
    
    public PracticeTestLoginPage(WebDriver driver) {
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
        return driver.findElement(usernameField).isDisplayed();
    }

    public boolean isSubmitButtonVisible() {
        return driver.findElement(submitButton).isDisplayed();
    }

    public boolean isToggleNavigationButtonVisible() {
        return driver.findElement(toggleNavigationButton).isDisplayed();
    }

    public void enterUsername(String username) {
        WebElement usernameInput = driver.findElement(usernameField);
        usernameInput.clear();
        usernameInput.sendKeys(username);
    }

    public boolean isUsernameInputAccepted() {
        String enteredText = driver.findElement(usernameField).getAttribute("value");
        return !enteredText.isEmpty();
    }
}
