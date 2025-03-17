
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class SeleniumGridPage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browser handling can be implemented here
    }

    public void openURL(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isTextPresent(String text) {
        return driver.getPageSource().contains(text);
    }

    public void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }
}
	