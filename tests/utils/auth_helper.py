"""
Authentication helpers for all user roles
"""
from selenium.webdriver.common.by import By
from tests.utils.base_test import BaseTest


class AuthHelper(BaseTest):
    """Helper class for authentication operations"""
    
    # Login page selectors
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[name='username'], input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message, .alert-danger, [role='alert']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def login(self, username: str, password: str, expected_redirect: str = None):
        """
        Generic login method
        
        Args:
            username: Username or email
            password: Password
            expected_redirect: Expected URL path after login (optional)
        
        Returns:
            bool: True if login successful
        """
        # Navigate to login page
        self.navigate_to("/login")
        self.wait_for_page_load()
        
        # Enter credentials
        self.type_text(*self.USERNAME_INPUT, username)
        self.type_text(*self.PASSWORD_INPUT, password)
        
        # Store current URL to detect redirect
        old_url = self.get_current_url()
        
        # Click login button
        self.click(*self.LOGIN_BUTTON)
        
        # Wait for redirect
        self.wait_for_url_change(old_url, timeout=10)
        
        # Check if redirected to expected page
        if expected_redirect:
            self.wait_for_url_contains(expected_redirect, timeout=5)
        
        # Return success if no error message
        return not self.element_exists(*self.ERROR_MESSAGE, timeout=2)
    
    def login_as_student(self, username: str = None, password: str = None):
        """Login as student with test credentials"""
        username = username or "test_student"
        password = password or "test_password_123"
        return self.login(username, password, expected_redirect="/student")
    
    def login_as_mentor(self, username: str = None, password: str = None):
        """Login as mentor with test credentials"""
        username = username or "test_mentor"
        password = password or "test_password_123"
        return self.login(username, password, expected_redirect="/mentor")
    
    def login_as_floor_wing(self, username: str = None, password: str = None):
        """Login as floor wing with test credentials"""
        username = username or "test_floorwing"
        password = password or "test_password_123"
        return self.login(username, password, expected_redirect="/floor-wing")
    
    def login_as_admin(self, username: str = None, password: str = None):
        """Login as admin with test credentials"""
        username = username or "test_admin"
        password = password or "test_password_123"
        return self.login(username, password, expected_redirect="/admin")
    
    def login_as_superadmin(self, username: str = None, password: str = None):
        """Login as superadmin with test credentials"""
        username = username or "superadmin"
        password = password or "admin_password_123"
        return self.login(username, password, expected_redirect="/admin")
    
    def logout(self):
        """Logout current user"""
        # Try multiple common logout methods
        logout_selectors = [
            (By.CSS_SELECTOR, "button.logout"),
            (By.CSS_SELECTOR, "[data-testid='logout']"),
            (By.XPATH, "//button[contains(text(), 'Logout')]"),
            (By.XPATH, "//a[contains(text(), 'Logout')]"),
            (By.CSS_SELECTOR, ".logout-btn"),
        ]
        
        for selector in logout_selectors:
            if self.element_exists(*selector, timeout=2):
                self.click(*selector)
                # Wait for redirect to login
                self.wait_for_url_contains("/login", timeout=10)
                return True
        
        # Fallback: Clear localStorage and navigate to login
        self.driver.execute_script("localStorage.clear(); sessionStorage.clear();")
        self.navigate_to("/login")
        return True
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        # Check for auth token in localStorage
        token = self.get_auth_token_from_browser()
        return token is not None and token != ""
    
    def get_current_role(self) -> str:
        """Detect current user role from URL or localStorage"""
        url = self.get_current_url()
        
        if "/student" in url:
            return "student"
        elif "/mentor" in url:
            return "mentor"
        elif "/floor-wing" in url:
            return "floor_wing"
        elif "/admin" in url:
            return "admin"
        else:
            # Try to get from localStorage
            try:
                role = self.driver.execute_script("return localStorage.getItem('userRole');")
                return role
            except:
                return "unknown"
    
    def verify_session_persistence(self):
        """Verify session persists after page refresh"""
        old_url = self.get_current_url()
        self.refresh_page()
        self.wait_for_page_load()
        
        # Should still be logged in
        assert self.is_logged_in(), "Session lost after page refresh"
        
        # Should be on same page
        new_url = self.get_current_url()
        assert old_url == new_url, f"URL changed after refresh: {old_url} -> {new_url}"
    
    def attempt_unauthorized_access(self, path: str) -> bool:
        """
        Attempt to access a path and check if redirected/blocked
        
        Returns:
            bool: True if access was blocked (redirected to login or error)
        """
        old_url = self.get_current_url()
        self.navigate_to(path)
        self.wait_for_page_load(timeout=5)
        
        new_url = self.get_current_url()
        
        # Check if redirected to login or stayed on same page
        if "/login" in new_url or new_url == old_url:
            return True
        
        # Check for 403/401 error messages
        forbidden_indicators = [
            (By.XPATH, "//*[contains(text(), '403')]"),
            (By.XPATH, "//*[contains(text(), '401')]"),
            (By.XPATH, "//*[contains(text(), 'Unauthorized')]"),
            (By.XPATH, "//*[contains(text(), 'Forbidden')]"),
            (By.XPATH, "//*[contains(text(), 'Access Denied')]"),
        ]
        
        for selector in forbidden_indicators:
            if self.element_exists(*selector, timeout=2):
                return True
        
        return False
    
    def get_error_message(self) -> str:
        """Get login error message if present"""
        if self.element_exists(*self.ERROR_MESSAGE, timeout=2):
            return self.get_text(*self.ERROR_MESSAGE)
        return ""
