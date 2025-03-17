
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class AdvancedCourseCouponPage {
    private WebDriver driver;

    public AdvancedCourseCouponPage() {
        // Initialize WebDriver, e.g., ChromeDriver for testing
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        this.driver = new ChromeDriver();
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isPageLoaded() {
        // Implement logic to check if the page is loaded
        // This could be checking for specific elements or just waiting for the page to finish loading
        return driver.getTitle().equals("Just a moment...");
    }

    public void close() {
        driver.quit();
    }
}
