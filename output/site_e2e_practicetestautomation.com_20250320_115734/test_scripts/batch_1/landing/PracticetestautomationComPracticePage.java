
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class PracticePage {
    private WebDriver driver;

    public PracticePage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isButtonVisibleAndClickable(String buttonId) {
        try {
            WebElement button = driver.findElement(By.id(buttonId));
            new WebDriverWait(driver, Duration.ofSeconds(10))
                .until(ExpectedConditions.elementToBeClickable(button));
            return button.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public void clickLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }

    public boolean isContentDisplayed(String content) {
        // Assume we have a method to check if specific content text is displayed on the page
        return driver.getPageSource().contains(content);
    }
}