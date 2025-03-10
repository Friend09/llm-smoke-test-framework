
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class ContactPage {
    private WebDriver driver;

    // Locators
    private By nameField = By.name("wpforms[fields][0]");
    private By emailField = By.name("wpforms[fields][1]");
    private By messageField = By.name("wpforms[fields][2]");
    private By submitButton = By.cssSelector("button[type='submit']");
    private By nameValidationMessage = By.cssSelector(".wpforms-error[data-name='name']");
    private By emailValidationMessage = By.cssSelector(".wpforms-error[data-name='email']");
    private By confirmationMessage = By.cssSelector(".wpforms-confirmation");
    private By navigationLinks = By.cssSelector(".navigation a");

    public ContactPage(WebDriver driver) {
        this.driver = driver;
    }

    public void fillName(String name) {
        driver.findElement(nameField).sendKeys(name);
    }

    public void fillEmail(String email) {
        driver.findElement(emailField).sendKeys(email);
    }

    public void fillMessage(String message) {
        driver.findElement(messageField).sendKeys(message);
    }

    public void clickSubmitButton() {
        driver.findElement(submitButton).click();
    }

    public boolean isNameValidationMessageDisplayed() {
        return driver.findElements(nameValidationMessage).size() > 0;
    }

    public boolean isEmailValidationMessageDisplayed() {
        return driver.findElements(emailValidationMessage).size() > 0;
    }

    public boolean isConfirmationMessageDisplayed() {
        return driver.findElements(confirmationMessage).size() > 0;
    }

    public void clickNavigationLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }
}
	