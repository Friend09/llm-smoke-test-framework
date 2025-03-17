
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class CourseCouponSteps {

    private CourseCouponPage courseCouponPage;

    public CourseCouponSteps() {
        courseCouponPage = new CourseCouponPage();
    }

    @Given("user launches browser in {string}")
    public void userLaunchesBrowserIn(String browser) {
        // Implementation for launching the specified browser
        courseCouponPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        courseCouponPage.openURL(url);
    }

    @Then("user verifies the title is {string}")
    public void userVerifiesTheTitleIs(String expectedTitle) {
        Assert.assertEquals(expectedTitle, courseCouponPage.getPageTitle());
    }

    @Then("user verifies that the content is present on the screen")
    public void userVerifiesThatTheContentIsPresent() {
        Assert.assertTrue(courseCouponPage.isContentPresent());
    }

    @When("user verifies that the 'Get Your Coupon' link is present")
    public void userVerifiesGetYourCouponLinkIsPresent() {
        Assert.assertTrue(courseCouponPage.isGetYourCouponLinkPresent());
    }

    @When("user clicks on the link 'Get Your Coupon'")
    public void userClicksOnGetYourCouponLink() {
        courseCouponPage.clickGetYourCouponLink();
    }

    @Then("user expects that a new page loads with appropriate content")
    public void userExpectsNewPageLoads() {
        Assert.assertTrue(courseCouponPage.isNewPageLoaded());
    }
	