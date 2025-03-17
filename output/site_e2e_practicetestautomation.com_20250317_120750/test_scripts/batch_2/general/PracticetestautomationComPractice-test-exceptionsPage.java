
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class TestExceptionsPage {

    private WebDriver driver;

    public void launchBrowser(String browser) {
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Add more browsers if needed
    }

    public void openURL(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isElementPresent(String element) {
        try {
            return driver.findElement(getLocator(element)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    private By getLocator(String element) {
        switch (element) {
            case "Test Exceptions":
                return By.xpath("//h1[text()='Test Exceptions']");
            case "Test Exception 1":
                return By.xpath("//h2[text()='Test Exception 1']");
            case "Test Exception 2":
                return By.xpath("//h2[text()='Test Exception 2']");
            case "Test Exception 3":
                return By.xpath("//h2[text()='Test Exception 3']");
            default:
                throw new IllegalArgumentException("No locator defined for element: " + element);
        }
    }
}
