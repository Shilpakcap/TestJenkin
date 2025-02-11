from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
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
    wait = WebDriverWait(driver, 150)
    logging.info("Website loaded successfully.")

    # Navigate to Manager Page
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Manager Page']"))
    )
    manager_page_button.click()
    logging.info("Navigated to Manager Page.")
    log_to_csv("Navigated to Manager Page.", "INFO")

    time.sleep(2)

    # Select Resources
    dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select Resources')]"))
    )
    dropdown.click()

    resources = ["Adam Cabe", "Ashish Kapoor", "Chang Lee", "David Basson"]

    for resource in resources:  # Use different variable name
        resource_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{resource}')]"))
        )
        resource_option.click()

    dropdown.click()  # Close dropdown

    time.sleep(2)

    # Click Suggestion Button
    suggestion_xpath = "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div/a[2]"
    suggestion_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
    )
    suggestion_button.click()

     # Select Location dropdown
    Loc_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable ((By.XPATH," /html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div/select"))
    )
    Loc_dropdown.click()
    logging.info("Clicked on Location dropdown...")
    time.sleep(2)
    select_cust = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH," /html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div/select/option[6]"))
    )
    select_cust.click()
    Loc_dropdown.click()
    logging.info("Selected Location from the dropdown...")
    
    time.sleep(10)

    start_time = time.time()  # Start time for performance tracking

    try:
        updated_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//p-button[contains(@ng-reflect-label, 'Show me list of open demands')]//button"))
        )

        driver.execute_script("arguments[0].click();", updated_button)  # JavaScript click
        logging.info("Updated button clicked successfully.")
        log_to_csv("Updated button clicked successfully.", "INFO")

    except Exception as e:
        logging.error(f"Error clicking updated button: {str(e)}")
        log_to_csv(f"Error clicking updated button: {str(e)}", "ERROR")


    # Scroll before clicking
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", updated_button)
    time.sleep(2)  # Short pause for stability

    driver.execute_script("arguments[0].click();", updated_button)
    logging.info("Updated button clicked successfully.")

    # Wait for table to load instead of using sleep
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p-table")))
    logging.info("Table is loaded and ready.")
    log_to_csv("Table is loaded and ready.", "INFO")

    end_time = time.time()  # End time for response calculation
    response_time = end_time - start_time
    logging.info(f"Query response time: {response_time:.2f} seconds")

    # Extract Headers
    header_cells = driver.find_elements(By.CSS_SELECTOR, "thead tr th")
    headers = [cell.text.strip() for cell in header_cells]
    logging.info(f"Extracted Headers: {headers}")
    log_to_csv(f"Extracted Headers: {headers}", "INFO")

    expected_headers = [" ", "GTD Task Name", "Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"]

    if validate_headers(headers, expected_headers):
        logging.info("Table headers are correct.")
        log_to_csv("Table headers are correct.", "INFO")
    else:
        logging.warning(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}")
        log_to_csv(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}", "WARNING")

    # Extract Data with Pagination
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers + ["Response Time (seconds)"])

        while True:
            rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                cell_data = [cell.text.strip() for cell in cells]

                if cell_data:
                    cell_data.append(f"{response_time:.2f}")
                writer.writerow(cell_data)

            # Handle Pagination
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
