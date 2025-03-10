class PracticeTestLoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = self.driver.find_element_by_id('username')
        self.submit_button = self.driver.find_element_by_id('submit')
        self.logout_button = self.driver.find_element_by_id('logout-button')
        self.toggle_navigation_button = self.driver.find_element_by_id('toggle-navigation')

    def enter_username(self, username):
        self.username_field.clear()
        self.username_field.send_keys(username)

    def click_submit(self):
        self.submit_button.click()

    def click_logout(self):
        self.logout_button.click()

    def click_toggle_navigation(self):
        self.toggle_navigation_button.click()

    def is_error_message_displayed(self):
        return self.driver.find_element_by_css_selector('.error-message').is_displayed()

    def is_success_message_displayed(self):
        return 'success' in self.driver.page_source

    def get_current_url(self):
        return self.driver.current_url