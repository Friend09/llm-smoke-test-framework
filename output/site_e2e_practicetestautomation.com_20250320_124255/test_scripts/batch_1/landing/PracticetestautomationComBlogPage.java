
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class BlogPage {
    WebDriver driver;

    // Locators
    private By blogTitle = By.xpath("//h1[contains(text(), 'Unlock Your Future: Selenium WebDriver Career Launcher Part 6')]");
    private By publishedDate = By.xpath("//span[contains(text(), 'Published by Dmitry Shyshkin')]\n");
    private By navigationLinks = By.cssSelector("nav a");

    public BlogPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isBlogTitleDisplayed() {
        return driver.findElement(blogTitle).isDisplayed();
    }

    public boolean isPublishedDateDisplayed() {
        return driver.findElement(publishedDate).isDisplayed();
    }

    public void clickNavigationLink(String linkText) {
        driver.findElement(By.linkText(linkText)).click();
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }
}