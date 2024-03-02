import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Read the Excel file
input_file_path = r"D:\\Scripts\\1\\input.xlsx"   # Change the input file path
df = pd.read_excel(input_file_path)

# Specify the full path to the ChromeDriver executable
chrome_driver_path = r"full\path\to\chromedriver.exe"  # Update with the full path to chromedriver.exe
webdriver.chrome.driver = chrome_driver_path  # Set the path as a system property

# Initialize a Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Optional: Open browser in maximized mode

# Initialize an empty list to store the working credentials
working_credentials = []

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    url = row['URL']
    username = row['Username']
    password = row['Password']

    # Initialize a new Chrome webdriver for each set of credentials
    driver = webdriver.Chrome(options=options)

    # Open the URL
    driver.get(url)

    # Find the username and password fields and enter the credentials
    username_field = driver.find_element(By.NAME, 'uname')  # Update with the actual username field name
    password_field = driver.find_element(By.NAME, 'pass')  # Update with the actual password field name
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Submit the form
    password_field.submit()

    # Check if login was successful by looking for specific strings in the response
    # If login was successful, add the working credentials to the list
    if "logout" in driver.page_source.lower() or "logged in" in driver.page_source.lower():
        print(f"Login successful for {username}")
        working_credentials.append({'URL': url, 'Username': username, 'Password': password})
        driver.close()  # Close the Chrome tab
        continue  # Move to the next set of credentials

    # If login failed, print a message and continue with the next set of credentials
    print(f"Login failed for {username}")
    driver.quit()  # Quit the browser instance

# Close the browser
driver.quit()

# Convert the working credentials list to a DataFrame
working_credentials_df = pd.DataFrame(working_credentials)

# Save the working credentials to "working_credentials.xlsx"
working_credentials_df.to_excel("working_credentials.xlsx", index=False)
