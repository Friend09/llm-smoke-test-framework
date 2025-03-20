
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class PracticeTestAutomationPage {
    WebDriver driver;

    // Unique element locators
    By firstNameInput = By.id("form_first_name_7");
    By emailInput = By.id("form_email_7");
    By toggleNavigationButton = By.id("toggle-navigation");
    
    public PracticeTestAutomationPage(WebDriver driver) {
        this.driver = driver;
    }

    public void enterFirstName(String firstName) {
        driver.findElement(firstNameInput).sendKeys(firstName);
    }

    public void enterEmail(String email) {
        driver.findElement(emailInput).sendKeys(email);
    }

    public void clickToggleNavigation() {
        driver.findElement(toggleNavigationButton).click();
    }

    public boolean isFirstNameInputPresent() {
        return driver.findElement(firstNameInput).isDisplayed();
    }

    public boolean isEmailInputPresent() {
        return driver.findElement(emailInput).isDisplayed();
    }
}
	