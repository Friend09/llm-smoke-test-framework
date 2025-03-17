
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class AdvancedCourseCouponSteps {

    private AdvancedCourseCouponPage couponPage = new AdvancedCourseCouponPage();

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        couponPage.navigateTo(url);
    }

    @Then("user verifies the title is {string}")
    public void userVerifiesTheTitleIs(String expectedTitle) {
        String actualTitle = couponPage.getPageTitle();
        Assert.assertEquals(expectedTitle, actualTitle);
    }

    @Then("user expects the page loads successfully")
    public void userExpectsThePageLoadsSuccessfully() {
        Assert.assertTrue(couponPage.isPageLoaded());
    }
}
