# core/auth_handler.py - Add your implementation here
"""2.Authentication Handler"""

# core/auth_handler.py
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config

logger = logging.getLogger(__name__)


class AuthHandler:
    """Handles different authentication methods for web applications."""

    def __init__(self, driver):
        self.driver = driver
        self.config = Config()

    def authenticate(self, auth_type=None):
        """
        Authenticate to the application using the specified method.

        Args:
            auth_type (str): Authentication type (basic, ntlm, okta)

        Returns:
            bool: True if authentication successful, False otherwise
        """
        auth_type = auth_type or self.config.AUTH_TYPE

        try:
            if auth_type.lower() == "basic":
                return self._handle_basic_auth()
            elif auth_type.lower() == "ntlm":
                return self._handle_ntlm_auth()
            elif auth_type.lower() == "okta":
                return self._handle_okta_auth()
            else:
                logger.warning(f"Unsupported authentication type: {auth_type}")
                return False
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    def _handle_basic_auth(self):
        """Handle basic username/password login."""
        try:
            logger.info("Attempting basic authentication")

            if "practice-test-login" in self.driver.current_url:
                # Wait for username field
                username_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
                username_input.clear()
                username_input.send_keys(self.config.USERNAME or "student")

                # Enter password
                password_input = self.driver.find_element(By.ID, "password")
                password_input.clear()
                password_input.send_keys(self.config.PASSWORD or "Password123")

                # Try multiple strategies to locate the login button
                login_button = None
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                except NoSuchElementException:
                    try:
                        login_button = self.driver.find_element(By.ID, "submit")
                    except NoSuchElementException:
                        try:
                            login_button = self.driver.find_element(By.CSS_SELECTOR, "button#submit")
                        except NoSuchElementException:
                            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit') or contains(text(), 'Login')]")

                if login_button:
                    login_button.click()
                else:
                    logger.error("Login button not found. Page source:\n" + self.driver.page_source)
                    return False

                WebDriverWait(self.driver, 15).until(
                    lambda d: "login" not in d.current_url.lower() or "logged-in" in d.current_url.lower()
                )
            else:
                logger.info("No authentication needed or already authenticated")
                return True

            logger.info("Basic authentication successful")
            return True

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Basic authentication failed: {str(e)}")
            return False

    def _handle_ntlm_auth(self):
        """Handle NTLM authentication."""
        # For NTLM auth, we typically need to set up the driver with credentials
        # If driver already has credentials, we just need to verify we're logged in
        try:
            logger.info("Using NTLM authentication")

            # Check if we're already authenticated
            # Look for elements that would only be visible when logged in
            # This is application-specific and needs to be adjusted
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'user-profile')]")
                )
            )

            logger.info("NTLM authentication confirmed")
            return True

        except TimeoutException:
            logger.warning("Unable to confirm NTLM authentication")
            return False

    def _handle_okta_auth(self):
        """Handle Okta authentication."""
        try:
            logger.info("Attempting Okta authentication")

            # Navigate to Okta login page if needed
            if (
                self.config.OKTA_URL
                and self.config.OKTA_URL not in self.driver.current_url
            ):
                self.driver.get(self.config.OKTA_URL)

            # Enter username
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "okta-signin-username"))
            )
            username_input.clear()
            username_input.send_keys(self.config.USERNAME)

            # Enter password
            password_input = self.driver.find_element(By.ID, "okta-signin-password")
            password_input.clear()
            password_input.send_keys(self.config.PASSWORD)

            # Click sign in
            sign_in_button = self.driver.find_element(By.ID, "okta-signin-submit")
            sign_in_button.click()

            # Wait for MFA if required (application specific)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//form[contains(@data-se, 'mfa-verify')]")
                    )
                )
                logger.info("MFA required for Okta login - waiting for user input")

                # Wait for MFA completion (this may require manual intervention)
                WebDriverWait(self.driver, 60).until(
                    lambda d: "okta" not in d.current_url.lower()
                    or "dashboard" in d.current_url.lower()
                )
            except TimeoutException:
                # No MFA prompt appeared, continue
                pass

            # Verify successful login
            time.sleep(2)  # Brief pause to allow redirect

            # Check if we've been redirected away from Okta login
            if "okta-signin" not in self.driver.page_source.lower():
                logger.info("Okta authentication successful")
                return True
            else:
                logger.warning(
                    "Still on Okta login page - authentication may have failed"
                )
                return False

        except Exception as e:
            logger.error(f"Okta authentication failed: {str(e)}")
            return False
