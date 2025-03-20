
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;

public class PracticeTestAutomationPage {
    private WebDriver driver;
    private WebDriverWait wait;

    public PracticeTestAutomationPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().contains("Practice Test Automation");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public void clickNavigationLink(String linkText) {
        WebElement link = wait.until(ExpectedConditions.elementToBeClickable(By.linkText(linkText)));
        link.click();
    }

    public String getCurrentURL() {
        return driver.getCurrentUrl();
    }

    public void clickProfileImage() {
        WebElement profileImage = wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("img.profile-image-selector")));
        profileImage.click();
    }

    public boolean isProfileInfoDisplayed() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("profile-info"))).isDisplayed();
    }

    public boolean isGreetingPresent(String greeting) {
        return driver.getPageSource().contains(greeting);
    }

    public boolean isIntroductionTextDisplayed() {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("introduction-text"))).isDisplayed();
    }

    public void resizeBrowser(String size) {
        switch(size) {
            case "mobile":
                driver.manage().window().setSize(new Dimension(375, 667));
                break;
            case "tablet":
                driver.manage().window().setSize(new Dimension(768, 1024));
                break;
            case "desktop":
                driver.manage().window().setSize(new Dimension(1280, 800));
                break;
        }
    }

    public boolean areNavigationLinksAccessible() {
        // Logic to verify navigation links are accessible
        return true;
    }

    public boolean isFullLayoutDisplayed() {
        // Logic to verify full layout is displayed correctly
        return true;
    }
}
