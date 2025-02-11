import os
import re
import csv
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Setup Chrome WebDriver
driver = webdriver.Chrome()

# Get the script name without extension
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Generate the directory to save the CSV file
csv_directory = os.path.join("C:\\Shilpa\\GenAI", "Scripts_Results", script_name)

# Create the directory if it doesn't exist
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Generate the full file path for the CSV
csv_file_path = os.path.join(csv_directory, "output_data.csv")

try:
    # Navigate to the webpage
    driver.get("http://localhost:4200/assignmentAssistant")
    wait = WebDriverWait(driver, 300)  # Adjust timeout as necessary

    
    # Navigate to Manager Page
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Manager Page']"))
    )
    manager_page_button.click()
    print("Navigated to Manager Page.")
    print("Navigated to Manager Page.", "INFO")

    time.sleep(30)
    # Find and click the Select Demand IDs dropdown
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select Demand IDs')]"))
    )
    dropdown.click()

    # Select multiple demand IDs (modify XPath as needed)
    demand_ids = [
        "//span[contains(text(), 'W6TX02')]",
        "//span[contains(text(), 'QATHQ3')]"
    ]

    # Click each selected demand ID
    for id_xpath in demand_ids:
        demand_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, id_xpath))
        )
        demand_option.click()

    # Optional: Close dropdown if needed
    dropdown.click()

    time.sleep(2)

    # Find and click suggestion 3
    suggestion_xpath = "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div/a[3]"
    suggestion_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
    )

    print("Clicking on suggestion 3...")
    suggestion_button.click()

    time.sleep(2)

    # Select Customer dropdown
    cust_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[1]/select"))
    )
    cust_dropdown.click()
    print("Clicked on Customer dropdown...")
    time.sleep(2)

    # Select Customer from the dropdown
    select_cust = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[1]/select/option[64]"))
    )
    select_cust.click()
    # Optional: Close dropdown if needed
    cust_dropdown.click()
    print("Selected Customer from the dropdown...")
    time.sleep(2)

    # Scrolling to find the Industry dropdown
    element = driver.find_element(By.XPATH,
                                  '/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[3]/select')
    driver.execute_script("arguments[0].scrollIntoView()", element)
    time.sleep(2)
    print("Scrolling to find the industry dropdown")

    time.sleep(2)

    # Select Industry dropdown
    ind_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[3]/select"))
    )
    ind_dropdown.click()
    print("Clicked on Industry...")
    time.sleep(2)

    # Select Automotive from the dropdown
    auto_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[3]/select/option[4]"))
    )
    auto_dropdown.click()
    # Optional: Close dropdown if needed
    ind_dropdown.click()
    print("Selected Automotive on Industry from dropdown...")
    time.sleep(2)

    #Scrolling to find the show me list of demands button
    element = driver.find_element(By.XPATH, '/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/p-button/button/span')
    driver.execute_script("arguments[0].scrollIntoView()", element)
    time.sleep(2)
    print("Scrolling to the Show me list submit button...")

    #Click on show me list of demands button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/p-button/button/span"))
    )
    submit_button.click()
    print("Submit button clicked...")

    # Wait for the grid to load
    grid = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/div/div/div")))
    print("Grid Found.")

    # Extract rows
    rows = grid.find_elements(By.CSS_SELECTOR, "div.ag-row")
    print(f"Number of rows: {len(rows)}")

    # Extract header (if applicable)
    header = grid.find_elements(By.CSS_SELECTOR, "div.ag-header-cell")
    actual_headers = [cell.text.strip() for cell in header]
    expected_headers = [
        "GTD Task Name", "Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"
    ]
    print(f"Actual Headers: {actual_headers}")

    if actual_headers == expected_headers:
        print("Headers are correct.")
    else:
        print(f"Headers are incorrect. Expected: {expected_headers}")

    # Open the CSV file to write the data
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row into the CSV
        writer.writerow(expected_headers)

        # Extract and validate rows
        for i, row in enumerate(rows, start=1):
            cells = row.find_elements(By.CSS_SELECTOR, "div.ag-cell")
            cell_data = [cell.text.strip() for cell in cells]
            print(f"Row {i}: {cell_data}")

            # Write each row of data to the CSV
            writer.writerow(cell_data)

            # Example: Validate "Percentage Match" column (5th column, index 4)
            if len(cell_data) >= 5:  # Ensure the column exists
                if not re.match(r"^\d+(\.\d+)?%$", cell_data[4]):
                    print(f"Row {i}, Column 5 (Percentage Match) is not in the correct format: {cell_data[4]}")

    print(f"Data has been saved to {csv_file_path}")

    # Optional: Wait before closing the browser for observation
    time.sleep(10)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the browser
    driver.quit()