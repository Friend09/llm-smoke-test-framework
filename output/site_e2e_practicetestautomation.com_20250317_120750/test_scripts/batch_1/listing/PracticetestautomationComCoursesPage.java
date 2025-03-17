import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class CoursesPage {
    private WebDriver driver;

    public void launchBrowser(String browser) {
        // Implement logic to launch the specified browser
        if (browser.equalsIgnoreCase("Chrome")) {
            System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
            driver = new ChromeDriver();
        }
        // Add other browsers as needed
    }

    public void openURL(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isCourseSectionPresent() {
        return driver.findElements(By.cssSelector(".course-section-selector")).size() > 0; // Replace with actual selector
    }

    public boolean isCourseListDisplayed() {
        return driver.findElements(By.cssSelector(".course-list-selector")).size() > 0; // Replace with actual selector
    }

    public void closeBrowser() {
        if (driver != null) {
            driver.quit();
        }
    }
}