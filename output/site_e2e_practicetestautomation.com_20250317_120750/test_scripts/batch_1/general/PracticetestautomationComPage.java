
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class PracticeTestPage {
    private WebDriver driver;

    public PracticeTestPage(WebDriver driver) {
        this.driver = driver;
    }

    public void launchBrowser(String browser) {
        // Implementation to launch the browser
    }

    public void openUrl(String url) {
        driver.get(url);
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isHeadingPresent(String heading) {
        return driver.findElement(By.xpath("//h1[contains(text(), '" + heading + "')]")) != null;
    }

    public void clickLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }

    public boolean isBlogPostDisplayed() {
        // Implementation to check if a blog post is displayed
        return true; // Placeholder
    }

    public boolean isCourseDisplayed() {
        // Implementation to check if a course is displayed
        return true; // Placeholder
    }

    public void scrollToFooter() {
        // Implementation to scroll to the footer of the page
    }

    public boolean isLinkPresent(String linkText) {
        return driver.findElements(By.linkText(linkText)).size() > 0;
    }
}
