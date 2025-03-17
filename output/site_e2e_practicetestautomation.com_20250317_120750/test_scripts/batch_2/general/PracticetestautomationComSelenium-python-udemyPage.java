import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.By;

public class JustAMomentPage {
    private WebDriver driver;
    private WebDriverWait wait;

    public JustAMomentPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, 10);
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isLoadingIndicatorDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("loading-indicator-id"))).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isContentLoaded() {
        // Assume content is identified by a specific element
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("content-id"))).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }
}