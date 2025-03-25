import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class PracticeTestAutomationPage {
    private WebDriver driver;
    private WebDriverWait wait;

    // Locators
    private By pageTitleLocator = By.xpath("//title");
    private By toggleNavigationButton = By.id("toggle-navigation");
    private By firstNameField = By.id("form_first_name_7");
    private By emailField = By.id("form_email_7");

    public PracticeTestAutomationPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, 10);
        PageFactory.initElements(driver, this);
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(toggleNavigationButton)).isDisplayed();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isToggleNavigationButtonDisplayed() {
        return driver.findElement(toggleNavigationButton).isDisplayed();
    }

    public boolean isToggleNavigationButtonClickable() {
        return driver.findElement(toggleNavigationButton).isEnabled();
    }

    public void enterValueIntoField(String value, String fieldId) {
        WebElement field = driver.findElement(By.id(fieldId));
        field.clear();
        field.sendKeys(value);
    }

    public boolean areAllLinksWorking() {
        // Implement link checking logic here
        return true; // Placeholder
    }

    public boolean isHeaderVisible() {
        // Implement visibility check for header
        return true; // Placeholder
    }

    public boolean isExperienceSectionVisible() {
        // Implement visibility check for experience section
        return true; // Placeholder
    }
}