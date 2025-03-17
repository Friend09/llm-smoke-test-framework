import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import org.junit.Assert;

public class CoursesPageSteps {
    private CoursesPage coursesPage = new CoursesPage();

    @Given("user launches browser in {string}")
    public void userLaunchesBrowser(String browser) {
        coursesPage.launchBrowser(browser);
    }

    @Given("user opens URL {string}")
    public void userOpensURL(String url) {
        coursesPage.openURL(url);
    }

    @Then("user verifies page title is {string}")
    public void userVerifiesPageTitle(String expectedTitle) {
        Assert.assertEquals(expectedTitle, coursesPage.getPageTitle());
    }

    @Then("user verifies course section is present on screen")
    public void userVerifiesCourseSection() {
        Assert.assertTrue(coursesPage.isCourseSectionPresent());
    }

    @Then("user verifies course list is displayed")
    public void userVerifiesCourseList() {
        Assert.assertTrue(coursesPage.isCourseListDisplayed());
    }
}