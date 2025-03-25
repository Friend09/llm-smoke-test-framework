
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class ContactPage {
    private WebDriver driver;

    public ContactPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Contact | Practice Test Automation | Selenium WebDriver");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public void enterFirstName(String firstName) {
        driver.findElement(By.id("wpforms-161-field_0")).sendKeys(firstName);
    }

    public void enterLastName(String lastName) {
        driver.findElement(By.id("wpforms-161-field_1")).sendKeys(lastName);
    }

    public void enterEmail(String email) {
        driver.findElement(By.id("wpforms-161-field_2")).sendKeys(email);
    }

    public void enterMessage(String message) {
        driver.findElement(By.id("wpforms-161-field_3")).sendKeys(message);
    }

    public void clickSubmitButton() {
        driver.findElement(By.id("wpforms-submit-161")).click();
    }

    public boolean isValidationMessagesDisplayed() {
        // Implement logic to check for validation messages
        return true; // Placeholder
    }

    public boolean isSubmissionAcknowledgmentDisplayed() {
        // Implement logic to check for submission acknowledgment
        return true; // Placeholder
    }

    public boolean isInvalidEmailErrorDisplayed() {
        // Implement logic to check for invalid email error
        return true; // Placeholder
    }

    public boolean isMessageLengthErrorDisplayed() {
        // Implement logic to check for message length error
        return true; // Placeholder
    }

    public boolean isCorrectPageURL(String page) {
        // Implement logic to verify the correct URL based on the page
        return true; // Placeholder
    }
}
