import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class ExampleDomainPage {
    private WebDriver driver;

    // Locators
    private By heading = By.xpath("//h1[text()='Example Domain']");
    private By link = By.xpath("//a[text()='More information...']");

    public ExampleDomainPage(WebDriver driver) {
        this.driver = driver;
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isHeadingDisplayed() {
        return driver.findElement(heading).isDisplayed();
    }

    public boolean isLinkVisibleAndEnabled() {
        WebElement linkElement = driver.findElement(link);
        return linkElement.isDisplayed() && linkElement.isEnabled();
    }

    public void clickLink() {
        driver.findElement(link).click();
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }
}