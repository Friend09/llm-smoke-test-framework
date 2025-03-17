
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class PrivacyPolicyPage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Add other browsers as needed
    }

    public void openUrl(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isElementPresent(String element) {
        try {
            return driver.findElement(By.xpath("//h1[contains(text(), '" + element + "')]")) != null;
        } catch (NoSuchElementException e) {
            return false;
        }
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
	