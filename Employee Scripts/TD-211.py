from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os
import csv

# Set up the WebDriver (e.g., Chrome)
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
    logging.info("Opening webpage...")
    driver.get("http://localhost:4200/assignmentAssistant")
    
    wait = WebDriverWait(driver, 150)  # Adjust timeout as necessary
    
    logging.info("Waiting for Employee Page button...")
    # Wait for the Employee Page button to be clickable
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Employee Page']"))
    )
    manager_page_button.click()
    logging.info("Navigated to Employee Page.")
    
    # Wait for the dropdown span to be visible
    logging.info("Waiting for resource combobox...")
    combobox = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@aria-label='Select a resource']"))
    )
    
    # Click the combobox to open the dropdown
    logging.info("Clicking combobox to open dropdown...")
    combobox.click()
    
    # Wait for the dropdown list to be visible
    logging.info("Waiting for dropdown options to be visible...")
    options_list = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "pn_id_1_list"))
    )
    
    # Select the resource "Zhuoming Huang"
    logging.info("Selecting resource 'Zhuoming Huang'...")
    resource_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//li[span[contains(text(), 'Zhuoming Huang')]]"))
    )
    
    # Click on the resource option
    resource_option.click()

    # Wait for the 'Next' button to become clickable (after selecting resource)
    logging.info("Waiting for 'Next' button to become clickable...")
    Next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.p-ripple.p-button"))
    )

    # Scroll to 'Next' button and click it
    driver.execute_script("arguments[0].scrollIntoView(true);", Next_button)
    Next_button.click()
    logging.info(f"Resource 'Zhuoming Huang' selected and 'Next' button clicked successfully.")
    time.sleep(2)

   
    # Wait for the query box to appear
    query_box = wait.until(EC.presence_of_element_located((By.ID, "customQuery")))
    time.sleep(2)

    # Type into the query box
    query_box.send_keys("show me the open demand for Java Developer role")

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
    
except Exception as e:
    # Log the detailed exception message
    logging.error(f"An error occurred: {str(e)}")
    logging.error(f"Exception type: {type(e)}")
    logging.error(f"Page source:\n{driver.page_source}")
    
finally:
    driver.quit()
