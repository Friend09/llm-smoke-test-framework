
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class PracticePage {

    private WebDriver driver;

    public PracticePage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().contains("Practice");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isLinkPresent(String linkText) {
        return driver.findElements(By.linkText(linkText)).size() > 0;
    }

    public void clickLink(String linkText) {
        WebElement link = driver.findElement(By.linkText(linkText));
        link.click();
    }

    public String getCurrentURL() {
        return driver.getCurrentUrl();
    }

    public void clickToggleNavigation() {
        driver.findElement(By.id("toggle-navigation")).click();
    }

    public boolean isNavigationMenuDisplayed() {
        // Assuming the navigation menu has a specific ID or class
        return driver.findElement(By.className("navigation-menu")).isDisplayed();
    }
	