import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Load contacts from CSV file
contacts = pd.read_csv('contacts.csv')

# Customize your message
message_template = "Hello {}, this is a test message."

# Function to send WhatsApp messages
def send_whatsapp_message(driver, phone, message):
    try:
        url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
        driver.get(url)
        print(f"Navigating to {url}")

        # Wait for the message input box to be loaded
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')) # adjust the selector XPATH
        )
        print("Message box located")

        # Click the message box to ensure focus
        message_box.click()

        # Wait for the send button to be clickable and click it
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))  # adjust the selector XPATH
        )
        print("Send button located")
        send_button.click()

        print(f"Message sent to {phone}")

    except Exception as e:
        print(f"Failed to send message to {phone}. Error: {str(e)}")

# Set up Selenium WebDriver to use existing Chrome session
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir={your-path}")  # Update with your profile path, check using your browser ex: Chrome, use "chrome://version" from your browser
options.add_argument("profile-directory=Default")  # This should match the profile name

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Ensure WhatsApp Web is already logged in
driver.get("https://web.whatsapp.com")
input("Press Enter after ensuring WhatsApp Web is fully loaded")

# Send message to each contact
for index, contact in contacts.iterrows():
    personalized_message = message_template.format(contact['name'])
    send_whatsapp_message(driver, contact['phone'], personalized_message)
    time.sleep(10)  # wait before sending the next message

print("All messages have been sent.")
driver.quit()
