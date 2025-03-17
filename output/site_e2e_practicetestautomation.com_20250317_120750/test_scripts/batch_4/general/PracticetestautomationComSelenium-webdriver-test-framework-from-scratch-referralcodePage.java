
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class Page {
    private WebDriver driver;
    private WebDriverWait wait;

    public Page(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isLoadingMessageDisplayed() {
        try {
            WebElement loadingMessage = wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//*[contains(text(), 'Just a moment')]")));
            return loadingMessage.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public void waitForLoading() {
        wait.until(ExpectedConditions.invisibilityOfElementLocated(By.xpath("//*[contains(text(), 'Just a moment')]")));
    }

    public boolean isExpectedContentDisplayed() {
        // Modify this method based on actual expected content after loading
        return true; // Placeholder
    }
}