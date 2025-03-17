
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class BlogPage {
    
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browser options can be added here
    }

    public void openURL(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isElementPresent(String elementText) {
        return driver.findElements(By.xpath("//*[contains(text(), '" + elementText + "')]" )).size() > 0;
    }

    public boolean isBlogPostDisplayed() {
        return driver.findElements(By.cssSelector(".blog-post")).size() > 0; // Adjust selector as necessary
    }

    public void clickFirstBlogPost() {
        driver.findElement(By.cssSelector(".blog-post a")).click(); // Adjust selector as necessary
    }

    public boolean isBlogPostPageDisplayed() {
        return driver.findElements(By.cssSelector(".post-title")).size() > 0; // Adjust selector as necessary
    }
    
    public void closeBrowser() {
        driver.quit();
    }
}
	