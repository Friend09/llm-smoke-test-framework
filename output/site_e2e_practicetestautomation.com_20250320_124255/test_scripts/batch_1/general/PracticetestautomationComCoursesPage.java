
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class CoursesPage {
    private WebDriver driver;

    public CoursesPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo(String url) {
        driver.get(url);
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Courses | Practice Test Automation");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public int getHTTPResponseStatus() {
        // Implementation for HTTP status check (could use a library like HttpURLConnection)
        return 200; // Placeholder for actual implementation
    }

    public void clickNavigationToggle() {
        WebElement toggleButton = driver.findElement(By.id("toggle-navigation"));
        toggleButton.click();
    }

    public boolean isNavigationMenuDisplayed() {
        // Check if the navigation menu is displayed
        // Implementation here
        return true; // Placeholder for actual implementation
    }

    public void enterFirstName(String firstName, String fieldId) {
        WebElement firstNameField = driver.findElement(By.id(fieldId));
        firstNameField.sendKeys(firstName);
    }

    public boolean isFirstNameAccepted() {
        // Check if first name is accepted
        // Implementation here
        return true; // Placeholder for actual implementation
    }

    public void enterEmail(String email, String fieldId) {
        WebElement emailField = driver.findElement(By.id(fieldId));
        emailField.sendKeys(email);
    }

    public boolean isEmailErrorDisplayed() {
        // Check if an error message is displayed for invalid email
        // Implementation here
        return false; // Placeholder for actual implementation
    }

    public boolean isEmailAccepted() {
        // Check if the email is accepted
        // Implementation here
        return true; // Placeholder for actual implementation
    }
}
