import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class ContactPage {
    private WebDriver driver;

    // Locators
    private By nameField = By.id("wpforms-161-field_0");
    private By emailField = By.id("wpforms-161-field_1");
    private By commentField = By.id("wpforms-161-field_2");
    private By submitButton = By.id("wpforms-submit-161");
    private By successMessage = By.className("wpforms-confirmation");

    public ContactPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateToContactPage() {
        driver.get("https://practicetestautomation.com/contact/");
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Contact | Practice Test Automation | Selenium WebDriver");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isInputFieldPresent(String fieldName) {
        switch (fieldName) {
            case "Name": return driver.findElement(nameField).isDisplayed();
            case "Email": return driver.findElement(emailField).isDisplayed();
            case "Comment/Message": return driver.findElement(commentField).isDisplayed();
            default: return false;
        }
    }

    public void enterValueIntoField(String fieldName, String value) {
        WebElement field;
        switch (fieldName) {
            case "Name": field = driver.findElement(nameField); break;
            case "Email": field = driver.findElement(emailField); break;
            case "Comment/Message": field = driver.findElement(commentField); break;
            default: throw new IllegalArgumentException("Invalid field name");
        }
        field.clear();
        field.sendKeys(value);
    }

    public void clickButton(String buttonName) {
        if (buttonName.equals("Submit")) {
            driver.findElement(submitButton).click();
        } else {
            throw new IllegalArgumentException("Invalid button name");
        }
    }

    public boolean isSuccessMessageDisplayed() {
        return driver.findElement(successMessage).isDisplayed();
    }

    public boolean isValidationMessageDisplayed(String fieldName) {
        // Implement validation message checking logic here based on your application's response
        return false;
    }

    public void clickNavigationLink(String linkName) {
        // Implement navigation link click logic here
    }

    public boolean isNavigatedTo(String expectedPage) {
        // Implement navigation verification logic here
        return false;
    }
}