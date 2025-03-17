// Step Definitions for XPath Course Coupon Page
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class XPathCourseCouponSteps {
    XPathCourseCouponPage couponPage = new XPathCourseCouponPage();

    @Given("I navigate to the XPath Course Coupon page")
    public void iNavigateToTheXPathCourseCouponPage() {
        couponPage.navigateTo();
        Assert.assertTrue(couponPage.isPageLoaded());
    }

    @Then("I expect that the page title is {string}")
    public void iExpectThatThePageTitleIs(String expectedTitle) {
        String actualTitle = couponPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("I expect that the page is loaded successfully")
    public void iExpectThatThePageIsLoadedSuccessfully() {
        Assert.assertTrue(couponPage.isPageLoaded());
    }

    @Then("I expect that no error message is displayed")
    public void iExpectThatNoErrorMessageIsDisplayed() {
        Assert.assertFalse(couponPage.isErrorMessageDisplayed());
    }