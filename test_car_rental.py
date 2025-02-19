from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Correct WebDriver initialization
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Wait for server to start
max_retries = 5
for i in range(max_retries):
    try:
        driver.get("http://127.0.0.1:8000")
        break
    except Exception as e:
        print(f"Server not ready, retrying ({i+1}/{max_retries})...")
        time.sleep(5)
else:
    print("Server did not start in time. Exiting...")
    driver.quit()
    exit(1)

# Validate title
assert "Car Rental" in driver.title

print("Test Passed: Car Rental Portal is accessible.")

# Close browser
driver.quit()
