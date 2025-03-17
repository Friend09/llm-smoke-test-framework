
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class BeginnersCourseCouponSteps {
    
    private final BeginnersCourseCouponPage couponPage = new BeginnersCourseCouponPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        couponPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        couponPage.openUrl(url);
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String expectedTitle) {
        String actualTitle = couponPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user verifies the content {string} is present on screen")
    public void userVerifiesTheContentIsPresentOnScreen(String content) {
        Assert.assertTrue(couponPage.isContentPresent(content));
    }
}
	