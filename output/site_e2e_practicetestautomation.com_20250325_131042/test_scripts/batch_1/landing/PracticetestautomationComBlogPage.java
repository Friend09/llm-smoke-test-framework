
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class BlogPage {
    private WebDriver driver;

    public BlogPage(WebDriver driver) {
        this.driver = driver;
    }

    public void clickNavigationLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }

    public void clickArticleTitle(String articleTitle) {
        WebElement articleLink = driver.findElement(By.linkText(articleTitle));
        articleLink.click();
    }

    public boolean isArticleContentVisible() {
        // Check if the article content is displayed
        return driver.findElement(By.cssSelector(".entry-content")).isDisplayed();
    }

    public boolean isContentVisible() {
        // Check for visibility of title, author, and body text
        return driver.findElement(By.cssSelector("h1.entry-title")).isDisplayed() &&
               driver.findElement(By.cssSelector(".post-author")).isDisplayed() &&
               driver.findElement(By.cssSelector(".entry-content")).isDisplayed();
    }

    public boolean isToggleButtonPresent() {
        return driver.findElement(By.id("toggle-navigation")).isDisplayed();
    }
}
	