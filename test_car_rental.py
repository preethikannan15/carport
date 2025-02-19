from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Open the Car Rental Portal
driver.get("http://your-server-ip-or-domain/")  # Replace with your actual URL

# Example test: Check if page title contains "Car Rental"
assert "Car Rental" in driver.title

# Print the result
print("Test Passed: Page Title -", driver.title)

# Close the browser
driver.quit()
