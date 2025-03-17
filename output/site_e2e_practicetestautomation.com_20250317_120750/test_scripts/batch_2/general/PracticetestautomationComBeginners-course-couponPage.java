
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.By;

public class BeginnersCourseCouponPage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browser setups can be added here
    }

    public void openUrl(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isContentPresent(String content) {
        try {
            return driver.findElement(By.xpath("//*[contains(text(), '" + content + "')]")) != null;
        } catch (NoSuchElementException e) {
            return false;
        }
    }

    public void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }
}
	