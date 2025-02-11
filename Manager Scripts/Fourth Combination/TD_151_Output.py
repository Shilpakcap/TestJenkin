from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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

    # Select Demand IDs
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select Demand IDs')]")))
    dropdown.click()

    demand_ids = ["W6TX02", "QATHQ3", "98T9QK", "VCTI5Q"]
    for demand in demand_ids:
        demand_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{demand}')]")))
        demand_option.click()
    dropdown.click()  # Close dropdown

    # Select Resources
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Select Resources')]")))
    dropdown.click()

    resources = ["Adam Cabe", "Ashish Kapoor", "Chang Lee", "David Basson"]
    for resource in resources:
        resource_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{resource}')]")))
        resource_option.click()
    dropdown.click()  # Close dropdown

    time.sleep(2)

    # Click Suggestion Button
    suggestion_xpath = "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div/a[3]"
    suggestion_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
    )
    suggestion_button.click()

    # Select Grade from dropdown
    grade_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(@id, 'grade')]")))
    driver.execute_script("arguments[0].scrollIntoView();", grade_dropdown)
    time.sleep(1)
    select = Select(grade_dropdown)
    select.select_by_index(5)  # Adjust index as needed
    logging.info("Selected Grade from the dropdown.")
    time.sleep(2)

    # Select Customer
    customer_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@id, 'customer')]")))
    customer_dropdown.click()
    time.sleep(2)
    select_customer = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@id, 'customer')]/option[64]")))
    select_customer.click()
    logging.info("Selected Customer from the dropdown.")
    time.sleep(2)

    # Scroll and click 'Show me list' button
    show_list_button = driver.find_element(By.XPATH, '/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/p-button/button/span')
    driver.execute_script("arguments[0].scrollIntoView();", show_list_button)
    time.sleep(2)

    start_time = time.time()
    show_list_button.click()
    logging.info("Submit button clicked.")
    log_to_csv("Submit button clicked.", "INFO")

    # Measure response time
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p-table")))
    end_time = time.time()
    response_time = end_time - start_time
    logging.info(f"Query response time: {response_time:.2f} seconds")
    log_to_csv(f"Query response time: {response_time:.2f} seconds", "INFO")

    # Extract headers
    header_cells = table.find_elements(By.CSS_SELECTOR, "thead tr th")
    headers = [cell.text.strip() for cell in header_cells]
    logging.info(f"Extracted Headers: {headers}")
    log_to_csv(f"Extracted Headers: {headers}", "INFO")

    # Expected headers
    expected_headers = ["GTD Task Name", "Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"]
    if headers == expected_headers:
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

            # Check if next page exists
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".p-paginator-next:not(.p-disabled)")))
                next_button.click()
                time.sleep(3)
            except:
                break

    logging.info(f"Data successfully saved in {csv_file_path}")
    log_to_csv(f"Data successfully saved in {csv_file_path}", "INFO")

finally:
    driver.quit()
