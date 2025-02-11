import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv
import logging

# Initialize WebDriver
driver = webdriver.Chrome()

# Get script name and define paths
script_name = os.path.splitext(os.path.basename(__file__))[0]
csv_directory = os.path.join("C:\\Shilpa\\GenAI", "Scripts_Results", script_name)
os.makedirs(csv_directory, exist_ok=True)

# Define file paths
csv_file_path = os.path.join(csv_directory, "output_data.csv")
log_file_path = os.path.join(csv_directory, "script_logs.txt")
log_csv_path = os.path.join(csv_directory, "script_logs.csv")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, mode='a'),  
        logging.StreamHandler()  
    ]
)

# Function to log messages to CSV
def log_to_csv(message, level="INFO"):
    with open(log_csv_path, mode='a', newline='') as csv_log_file:
        csv_writer = csv.writer(csv_log_file)
        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), level, message])

# Function to validate headers
def validate_headers(actual_headers, expected_headers):
    return [header.lower().strip() for header in actual_headers] == [header.lower().strip() for header in expected_headers]

try:
    # Open the webpage
    driver.get("http://localhost:4200/assignmentAssistant")
    wait = WebDriverWait(driver, 150)  # Adjust timeout as necessary
    print("Website loaded successfully.")


    # Navigate to Manager Page
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Manager Page']"))
    )
    manager_page_button.click()
    logging.info("Navigated to Manager Page.")
    log_to_csv("Navigated to Manager Page.", "INFO")

    # Find and click the Select Demand IDs dropdown
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select Demand IDs')]"))
    )
    dropdown.click()

    # Select multiple demand IDs
    demand_ids = [
        "//span[contains(text(), 'W6TX02')]",
        "//span[contains(text(), 'QATHQ3')]",
        "//span[contains(text(), '98T9QK')]",
        "//span[contains(text(), 'VCTI5Q')]"
    ]

    # Click each demand ID
    for id_xpath in demand_ids:
        demand_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, id_xpath))
        )
        demand_option.click()

    # Close dropdown if needed
    dropdown.click()

    time.sleep(2)

    # Wait for the query box to appear
    query_box = wait.until(EC.presence_of_element_located((By.ID, "customQuery")))
    time.sleep(2)

    # Type into the query box
    query_box.send_keys("show me the open demand for Software Engineer role")
    logging.info("Query entered")

    
    # Scrolling to find the Query
    element = driver.find_element(By.XPATH,
                                  "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[4]")
    driver.execute_script("arguments[0].scrollIntoView()", element)
    time.sleep(2)

    # Wait for the submit button to become clickable
    submit_query = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.p-ripple.p-button")))

    # Click the submit button
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_query)
    logging.info("Button clicked successfully.")
    log_to_csv("Button clicked successfully.", "INFO")

    # Record the time before submitting the query
    start_time = time.time()
    
    submit_query.click()
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p-table")))
    logging.info("Table is loaded and ready.")
    log_to_csv("Table is loaded and ready.", "INFO")

    # Record the time after the grid has loaded
    end_time = time.time()

    # Calculate response time
    response_time = end_time - start_time
    logging.info(f"Query response time: {response_time:.2f} seconds")

     # Extract headers
    header_cells = table.find_elements(By.CSS_SELECTOR, "thead tr th")
    headers = [cell.text.strip() for cell in header_cells]
    logging.info(f"Extracted Headers: {headers}")
    log_to_csv(f"Extracted Headers: {headers}", "INFO")

    # Extract headers
    header_cells = table.find_elements(By.CSS_SELECTOR, "thead tr th")
    headers = [cell.text.strip() for cell in header_cells]
    logging.info(f"Extracted Headers: {headers}")
    log_to_csv(f"Extracted Headers: {headers}", "INFO")

    # Expected headers
    expected_headers = [" ,GTD Task Name","Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"]

    if validate_headers(headers, expected_headers):
        logging.info("Table headers are correct.")
        log_to_csv("Table headers are correct.", "INFO")
    else:
        logging.warning(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}")
        log_to_csv(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}", "WARNING")

    # Extract Data with Pagination
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        extended_headers = headers + ["Response Time (seconds)"]
        writer.writerow(extended_headers)

        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                cell_data = [cell.text.strip() for cell in cells]

                # Add response time only for the first row
                if len(cell_data) > 0:
                    cell_data.append(f"{response_time:.2f}")

                writer.writerow(cell_data)

            # Check if next page exists
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, ".p-paginator-next")
                if "p-disabled" in next_button.get_attribute("class"):
                    break  
                next_button.click()
                time.sleep(3)  
            except:
                break  

    logging.info(f"Data successfully saved in {csv_file_path}")
    log_to_csv(f"Data successfully saved in {csv_file_path}", "INFO")

finally:
    driver.quit()
