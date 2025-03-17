
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

public class LoginTestSteps {

    private LoginPage loginPage;

    @Given("I open the login page")
    public void i_open_the_login_page() {
        loginPage = new LoginPage();
        loginPage.open();
    }

    @Then("the page title should be {string}")
    public void the_page_title_should_be(String title) {
        assertEquals(title, loginPage.getPageTitle());
    }

    @Then("the username input field should be present and enabled")
    public void the_username_input_field_should_be_present_and_enabled() {
        assertTrue(loginPage.isUsernameFieldPresentAndEnabled());
    }

    @When("I click the {string} button")
    public void i_click_the_button(String button) {
        loginPage.clickButton(button);
    }

    @Then("I should see an error message for empty username and password fields")
    public void i_should_see_an_error_message_for_empty_fields() {
        assertTrue(loginPage.isErrorMessageDisplayedForEmptyFields());
    }

    @When("I enter a valid username and an incorrect password")
    public void i_enter_valid_username_and_incorrect_password() {
        loginPage.enterUsername("validUser");
        loginPage.enterPassword("wrongPassword");
    }

    @Then("I should see an error message for incorrect credentials")
    public void i_should_see_an_error_message_for_incorrect_credentials() {
        assertTrue(loginPage.isErrorMessageDisplayedForIncorrectCredentials());
    }

    @When("I enter a valid username and a valid password")
    public void i_enter_valid_username_and_valid_password() {
        loginPage.enterUsername("validUser");
        loginPage.enterPassword("validPassword");
    }

    @Then("I should see a success message")
    public void i_should_see_a_success_message() {
        assertTrue(loginPage.isSuccessMessageDisplayed());
    }

    @When("I click the Toggle Navigation button")
    public void i_click_the_toggle_navigation_button() {
        loginPage.clickToggleNavigation();
    }

    @Then("the navigation menu should expand or collapse")
    public void the_navigation_menu_should_expand_or_collapse() {
        assertTrue(loginPage.isNavigationMenuExpandedOrCollapsed());
    }
}
