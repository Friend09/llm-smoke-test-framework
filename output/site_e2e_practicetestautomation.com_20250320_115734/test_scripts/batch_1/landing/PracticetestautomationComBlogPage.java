
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class BlogPage {
    private WebDriver driver;

    // Locators
    private By toggleNavigationButton = By.id("toggle-navigation");
    private By firstNameInput = By.id("form_first_name_8");
    private By emailInput = By.id("form_email_8");
    private By navigationMenu = By.className("navigation-menu");
    private By footerLinks = By.className("footer-links");
    
    public BlogPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Blog | Practice Test Automation");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isToggleNavigationButtonPresent() {
        return driver.findElement(toggleNavigationButton).isDisplayed();
    }

    public void clickToggleNavigationButton() {
        driver.findElement(toggleNavigationButton).click();
    }

    public boolean isNavigationMenuVisible() {
        return driver.findElement(navigationMenu).isDisplayed();
    }

    public boolean isNavigationLinkPresent(String linkText) {
        return driver.findElement(By.linkText(linkText)).isDisplayed();
    }

    public boolean isFirstNameInputPresent() {
        return driver.findElement(firstNameInput).isDisplayed();
    }

    public boolean isEmailInputPresent() {
        return driver.findElement(emailInput).isDisplayed();
    }

    public boolean isFooterLinksPresent() {
        return driver.findElement(footerLinks).isDisplayed();
    }
}
