
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class PracticePage {
    private WebDriver driver;

    // Constructor
    public PracticePage(WebDriver driver) {
        this.driver = driver;
    }

    // Locators
    private By testLoginPageLink = By.linkText("Test Login Page");
    private By testExceptionsLink = By.linkText("Test Exceptions");
    private By headerLinks = By.cssSelector("#main-header a");
    private By pageTitle = By.tagName("title");

    // Actions
    public void clickTestLoginPage() {
        driver.findElement(testLoginPageLink).click();
    }

    public void clickTestExceptions() {
        driver.findElement(testExceptionsLink).click();
    }

    public void clickHeaderLink(String linkText) {
        driver.findElement(By.linkText(linkText)).click();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isDescriptionDisplayed(String page) {
        String expectedDescription = page.equals("Test Login Page") ? "A test page for logging in" : "A test page for exceptions";
        return driver.findElement(By.xpath("//h3[contains(text(), '" + page + "')]//following-sibling::p")).getText().equals(expectedDescription);
    }
}
