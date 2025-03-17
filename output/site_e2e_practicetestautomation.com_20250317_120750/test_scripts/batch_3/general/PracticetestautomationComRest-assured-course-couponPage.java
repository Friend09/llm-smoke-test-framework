
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class CourseCouponPage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browser launch configurations can be added here
    }

    public void openURL(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isContentPresent() {
        // Implement logic to verify if content is present
        return driver.findElement(By.tagName("body")).isDisplayed();
    }

    public boolean isGetYourCouponLinkPresent() {
        // Implement logic to verify if the link is present
        return driver.findElement(By.linkText("Get Your Coupon")).isDisplayed();
    }

    public void clickGetYourCouponLink() {
        driver.findElement(By.linkText("Get Your Coupon")).click();
    }

    public boolean isNewPageLoaded() {
        // Implement logic to check if the new page has loaded correctly
        return driver.getTitle().contains("Expected Title of New Page");
    }
    
    public void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }
	