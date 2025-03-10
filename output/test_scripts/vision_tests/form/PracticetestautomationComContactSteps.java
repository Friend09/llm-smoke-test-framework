
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.By;
import static org.junit.Assert.assertTrue;

public class ContactFormSteps {
    WebDriver driver = new ChromeDriver();
    ContactPage contactPage = new ContactPage(driver);

    @Given("I navigate to the contact page")
    public void i_navigate_to_the_contact_page() {
        driver.get("https://practicetestautomation.com/contact/");
    }

    @When("I click the submit button")
    public void i_click_the_submit_button() {
        contactPage.clickSubmitButton();
    }

    @Then("I should see validation messages for Name and Email fields")
    public void i_should_see_validation_messages_for_Name_and_Email_fields() {
        assertTrue(contactPage.isNameValidationMessageDisplayed());
        assertTrue(contactPage.isEmailValidationMessageDisplayed());
    }

    @Given("I fill in the contact form with valid data")
    public void i_fill_in_the_contact_form_with_valid_data(io.cucumber.datatable.DataTable dataTable) {
        var data = dataTable.asLists(String.class);
        contactPage.fillName(data.get(1).get(0));
        contactPage.fillEmail(data.get(1).get(1));
        contactPage.fillMessage(data.get(1).get(2));
    }

    @Then("I should see a confirmation message")
    public void i_should_see_a_confirmation_message() {
        assertTrue(contactPage.isConfirmationMessageDisplayed());
    }

    @Given("I fill in the contact form with invalid email")
    public void i_fill_in_the_contact_form_with_invalid_email(io.cucumber.datatable.DataTable dataTable) {
        var data = dataTable.asLists(String.class);
        contactPage.fillName(data.get(1).get(0));
        contactPage.fillEmail(data.get(1).get(1));
        contactPage.fillMessage(data.get(1).get(2));
    }

    @Then("I should see a validation message for the email format")
    public void i_should_see_a_validation_message_for_the_email_format() {
        assertTrue(contactPage.isEmailValidationMessageDisplayed());
    }

    @When("I click on the {string} link")
    public void i_click_on_the_link(String linkText) {
        contactPage.clickNavigationLink(linkText);
    }

    @Then("I should be redirected to the {string} page")
    public void i_should_be_redirected_to_the_page(String expectedPageTitle) {
        assertTrue(driver.getTitle().contains(expectedPageTitle));
    }

    // Cleanup after tests
    @After
    public void tearDown() {
        driver.quit();
    }
}
	