import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class PracticePage {
    private WebDriver driver;

    // Locators
    private By toggleNavigationButton = By.id("toggle-navigation");
    private By navigationMenu = By.id("navigation"); // Adjust as needed

    public PracticePage(WebDriver driver) {
        this.driver = driver;
    }

    public boolean isToggleButtonVisible() {
        return driver.findElement(toggleNavigationButton).isDisplayed();
    }

    public void clickToggleButton() {
        driver.findElement(toggleNavigationButton).click();
    }

    public boolean isNavigationMenuDisplayed() {
        return driver.findElement(navigationMenu).isDisplayed();
    }
}
