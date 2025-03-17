import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class ContactPage {
    private WebDriver driver;
    private WebDriverWait wait;

    public ContactPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void launchBrowser(String browser) {
        // Implement browser launching logic here
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isInputFieldPresent(String fieldName) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(getFieldLocator(fieldName))).isDisplayed();
    }

    public boolean isTextAreaPresent(String areaName) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(getAreaLocator(areaName))).isDisplayed();
    }

    public boolean isButtonPresent(String buttonName) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(getButtonLocator(buttonName))).isDisplayed();
    }

    public void enterValueInInputField(String value, String fieldName) {
        WebElement inputField = wait.until(ExpectedConditions.visibilityOfElementLocated(getFieldLocator(fieldName)));
        inputField.clear();
        inputField.sendKeys(value);
    }

    public void clickButton(String buttonName) {
        WebElement button = wait.until(ExpectedConditions.elementToBeClickable(getButtonLocator(buttonName)));
        button.click();
    }

    public boolean isSuccessMessageDisplayed() {
        // Implement logic to check if success message is displayed
        return false;
    }

    private By getFieldLocator(String fieldName) {
        switch(fieldName) {
            case "Your Name": return By.name("name");
            case "Your Email": return By.name("email");
            default: throw new IllegalArgumentException("Field not recognized: " + fieldName);
        }
    }

    private By getAreaLocator(String areaName) {
        return By.name("message");
    }

    private By getButtonLocator(String buttonName) {
        if (buttonName.equals("Send Message")) {
            return By.cssSelector("button[type='submit']");
        }
        throw new IllegalArgumentException("Button not recognized: " + buttonName);
    }
}