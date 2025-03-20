
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;

public class BlogPageSteps {
    BlogPage blogPage = new BlogPage();

    @Given("user opens the URL {string}")
    public void userOpensTheURL(String url) {
        blogPage.navigateTo(url);
        Assert.assertTrue(blogPage.isPageLoaded());
    }

    @Then("user verifies the page title is {string}")
    public void userVerifiesThePageTitleIs(String title) {
        Assert.assertEquals(title, blogPage.getPageTitle());
    }

    @Then("user verifies the toggle navigation button is present")
    public void userVerifiesToggleNavigationButtonIsPresent() {
        Assert.assertTrue(blogPage.isToggleNavigationButtonPresent());
    }

    @When("user clicks on the toggle navigation button")
    public void userClicksOnToggleNavigationButton() {
        blogPage.clickToggleNavigationButton();
    }

    @Then("user expects the navigation menu to be visible")
    public void userExpectsNavigationMenuToBeVisible() {
        Assert.assertTrue(blogPage.isNavigationMenuVisible());
    }

    @Then("user expects the navigation menu to be hidden")
    public void userExpectsNavigationMenuToBeHidden() {
        Assert.assertFalse(blogPage.isNavigationMenuVisible());
    }

    @Then("user verifies the navigation links {string} are present")
    public void userVerifiesNavigationLinksArePresent(String links) {
        for (String link : links.split(", ")) {
            Assert.assertTrue(blogPage.isNavigationLinkPresent(link));
        }
    }

    @Then("user verifies the first name input field is present")
    public void userVerifiesFirstNameInputFieldIsPresent() {
        Assert.assertTrue(blogPage.isFirstNameInputPresent());
    }

    @Then("user verifies the email input field is present")
    public void userVerifiesEmailInputFieldIsPresent() {
        Assert.assertTrue(blogPage.isEmailInputPresent());
    }

    @Then("user verifies the footer links are present")
    public void userVerifiesFooterLinksArePresent() {
        Assert.assertTrue(blogPage.isFooterLinksPresent());
    }
	