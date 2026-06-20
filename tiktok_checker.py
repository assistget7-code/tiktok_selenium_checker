import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium_stealth import stealth

def check_credentials(email: str, password: str) -> dict:
    """Check TikTok credentials using undetected_chromedriver"""
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Use headless mode on Render
    headless_mode = os.environ.get("RENDER", False)
    
    try:
        driver = uc.Chrome(
            use_subprocess=True,
            headless=headless_mode,
            options=options
        )
        
        # Apply stealth settings
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        
        # Wait for email field
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email or username']"))
        )
        
        # Type email with human-like delay
        email_field = driver.find_element(By.XPATH, "//input[@placeholder='Email or username']")
        for char in email:
            email_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        # Type password with human-like delay
        password_field = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for redirect or error
        time.sleep(8)
        
        # Check if login was successful
        current_url = driver.current_url
        
        if "feed" in current_url or "following" in current_url:
            result = {
                "success": True,
                "status": "valid",
                "message": "Credentials are valid",
                "account": {"username": email}
            }
        else:
            # Check for error messages
            try:
                error_element = driver.find_element(By.XPATH, "//div[contains(@class, 'error')]")
                error_text = error_element.text
            except:
                error_text = "Login failed. Please check your credentials."
            
            result = {
                "success": False,
                "status": "error",
                "message": error_text
            }
        
        driver.quit()
        return result
            
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)}"
        }
