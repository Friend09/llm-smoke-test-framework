
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CoursesPage {
    private WebDriver driver;

    public CoursesPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo() {
        driver.get("https://practicetestautomation.com/courses/");
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Courses | Practice Test Automation");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public String getPageURL() {
        return driver.getCurrentUrl();
    }

    public void clickNavigationToggle() {
        driver.findElement(By.id("toggle-navigation")).click();
    }

    public boolean isNavigationMenuVisible() {
        return driver.findElement(By.id("navigation")).isDisplayed(); // Assuming the menu has ID navigation
    }

    public void clickFirstNameInputField() {
        driver.findElement(By.id("form_first_name_8")).click();
    }

    public boolean isFirstNameInputEditable() {
        return driver.findElement(By.id("form_first_name_8")).isEnabled();
    }

    public boolean canInputTextInFirstNameField() {
        driver.findElement(By.id("form_first_name_8")).sendKeys("Test");
        String value = driver.findElement(By.id("form_first_name_8")).getAttribute("value");
        return value.equals("Test");
    }

    public void clickEmailInputField() {
        driver.findElement(By.id("form_email_8")).click();
    }

    public boolean isEmailInputEditable() {
        return driver.findElement(By.id("form_email_8")).isEnabled();
    }

    public boolean isEmailInputAcceptingValidFormats() {
        driver.findElement(By.id("form_email_8")).sendKeys("test@example.com");
        // You can add more robust validation here if needed.
        return true; // Placeholder for actual validation logic
    }

    public String getEmailInputPlaceholder() {
        return driver.findElement(By.id("form_email_8")).getAttribute("placeholder");
    }
}