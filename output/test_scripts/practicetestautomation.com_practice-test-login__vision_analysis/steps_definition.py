from behave import given, when, then
from selenium import webdriver

@given('I navigate to the login page')
def step_navigate_to_login(context):
    context.browser = webdriver.Chrome()
    context.browser.get('https://practicetestautomation.com/practice-test-login/')

@then('the page title should be "{expected_title}"')
def step_check_page_title(context, expected_title):
    assert context.browser.title == expected_title

@when('I leave the username input field empty')
def step_empty_username_field(context):
    username_field = context.browser.find_element_by_id('username')
    username_field.clear()

@when('I click the Submit button')
def step_click_submit_button(context):
    submit_button = context.browser.find_element_by_id('submit')
    submit_button.click()

@then('I should see an error message')
def step_check_error_message(context):
    error_message = context.browser.find_element_by_css_selector('.error-message')
    assert error_message.is_displayed()

@when('I enter a valid username in the input field')
def step_enter_valid_username(context):
    username_field = context.browser.find_element_by_id('username')
    username_field.send_keys('valid_username')

@then('I should be redirected to the success page or see a success message')
def step_check_success_message(context):
    assert 'success' in context.browser.page_source

@when('I click the Log Out button')
def step_click_logout_button(context):
    logout_button = context.browser.find_element_by_id('logout-button')
    logout_button.click()

@then('I should be redirected to the login page or see a logout confirmation message')
def step_check_logout_confirmation(context):
    assert 'login' in context.browser.current_url

@when('I click on each navigation link')
def step_click_navigation_links(context):
    navigation_links = context.browser.find_elements_by_css_selector('.nav-link')
    for link in navigation_links:
        link.click()
        assert context.browser.current_url == link.get_attribute('href')

@when('I click the Toggle Navigation button')
def step_click_toggle_navigation(context):
    toggle_button = context.browser.find_element_by_id('toggle-navigation')
    toggle_button.click()

@then('the navigation menu should toggle visibility')
def step_check_navigation_menu(context):
    nav_menu = context.browser.find_element_by_id('nav-menu')
    assert nav_menu.is_displayed()