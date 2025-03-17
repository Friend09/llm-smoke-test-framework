
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class PracticePage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Additional browsers can be handled here
    }

    public void openUrl(String url) {
        driver.get(url);
    }

    public String getTitle() {
        return driver.getTitle();
    }

    public boolean isElementPresent(String elementName) {
        try {
            By locator = getLocator(elementName);
            return driver.findElement(locator).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public void clickElement(String elementName) {
        By locator = getLocator(elementName);
        driver.findElement(locator).click();
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }

    public void navigateBack() {
        driver.navigate().back();
    }

    private By getLocator(String elementName) {
        switch (elementName) {
            case "Sample A": return By.linkText("Sample A");
            case "Sample B": return By.linkText("Sample B");
            case "Sample C": return By.linkText("Sample C");
            default: throw new IllegalArgumentException("No such element: " + elementName);
        }
    }

    public void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }
}
