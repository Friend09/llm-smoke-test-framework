// Page Object Model for XPath Course Coupon Page
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class XPathCourseCouponPage {
    private WebDriver driver;
    private By pageTitleLocator = By.tagName("title");
    private By errorMessageLocator = By.id("error-message"); // Assuming there's an error message element with this ID

    public XPathCourseCouponPage(WebDriver driver) {
        this.driver = driver;
    }

    public void navigateTo() {
        driver.get("https://practicetestautomation.com/xpath-course-coupon");
    }

    public boolean isPageLoaded() {
        return driver.getTitle().equals("Just a moment...");
    }

    public String getPageTitle() {
        return driver.getTitle();
    }

    public boolean isErrorMessageDisplayed() {
        return driver.findElements(errorMessageLocator).size() > 0;
    }
}