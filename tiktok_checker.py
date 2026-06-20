import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def check_credentials(email: str, password: str) -> dict:
    """Check TikTok credentials using Selenium with Chrome"""

    # Chrome options for Render
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    try:
        # Use webdriver-manager to handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(3)
        
        # Wait for email field
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email or username']"))
        )
        
        # Enter email
        email_field = driver.find_element(By.XPATH, "//input[@placeholder='Email or username']")
        email_field.send_keys(email)
        time.sleep(1)
        
        # Enter password
        password_field = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password_field.send_keys(password)
        time.sleep(1)
        
        # Click login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait for response
        time.sleep(5)
        
        # Check if login was successful
        current_url = driver.current_url
        
        driver.quit()
        
        if "feed" in current_url or "following" in current_url:
            return {
                "success": True,
                "status": "valid",
                "message": "Credentials are valid",
                "account": {"username": email}
            }
        else:
            return {
                "success": False,
                "status": "error",
                "message": "Login failed. Please check your credentials."
            }
            
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)[:200]}"
        }
        
