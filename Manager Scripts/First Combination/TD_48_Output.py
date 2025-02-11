from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import csv
import re
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
    logging.info("Opening website...")
    log_to_csv("Opening website...", "INFO")
    
    driver.get("http://localhost:4200/assignmentAssistant")
    wait = WebDriverWait(driver, 300)
    logging.info("Website loaded successfully.")
    log_to_csv("Website loaded successfully.", "INFO")

    # Navigate to Manager Page
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Manager Page']"))
    )
    manager_page_button.click()
    logging.info("Navigated to Manager Page.")
    log_to_csv("Navigated to Manager Page.", "INFO")

    time.sleep(10)

    # Click desired suggestion
    suggestion_list_container = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-group.shadow-sm.rounded.ng-star-inserted"))
    )
    suggestions = suggestion_list_container.find_elements(By.TAG_NAME, "a")

    desired_text = "3.show me list of open demands, for specified customer or account, pu, industry, type of assignment (remote/ hybrid/ onsite), role, grade"
    normalized_desired_text = re.sub(r"\s+", " ", desired_text.strip().lower())

    for suggestion in suggestions:
        normalized_suggestion_text = re.sub(r"\s+", " ", suggestion.text.strip().lower())
        if normalized_suggestion_text == normalized_desired_text:
            logging.info(f"Clicking on suggestion: {suggestion.text.strip()}")
            log_to_csv(f"Clicking on suggestion: {suggestion.text.strip()}", "INFO")
            suggestion.click()
            break
    else:
        logging.error(f"Desired suggestion '{desired_text}' not found.")
        log_to_csv(f"Desired suggestion '{desired_text}' not found.", "ERROR")
        exit()

    # Select Role
    role_input = wait.until(EC.presence_of_element_located((By.ID, "role")))

    preferred_role = "Software Engineer"  
    role_input.clear()  
    role_input.send_keys(preferred_role)  
    logging.info(f"Entered Role: {preferred_role}")
    log_to_csv(f"Entered Role: {preferred_role}", "INFO")

    time.sleep(2)  

     # Select Grade
    grade_dropdown = wait.until(EC.presence_of_element_located((By.ID, "grade")))
    dropdown = Select(grade_dropdown)
    dropdown.select_by_visible_text("C1")
    logging.info("Grade 'C1' selected.")
    log_to_csv("Grade 'C1' selected.", "INFO")

     # Select Customer
    grade_dropdown = wait.until(EC.presence_of_element_located((By.ID, "customer")))
    dropdown = Select(grade_dropdown)
    dropdown.select_by_visible_text("Dell")
    logging.info("Customer 'Dell' selected.")
    log_to_csv("Customer 'Dell' selected.", "INFO")

    time.sleep(10)

    # Select Pu
    grade_dropdown = wait.until(EC.presence_of_element_located((By.ID, "pu")))
    dropdown = Select(grade_dropdown)
    dropdown.select_by_visible_text("ED-DE-CNE")
    logging.info("Pu 'ED-DE-CNE' selected.")
    log_to_csv("Pu 'ED-DE-CNE' selected.", "INFO")

    time.sleep(10)

    # Select Industry
    grade_dropdown = wait.until(EC.presence_of_element_located((By.ID, "industry")))
    dropdown = Select(grade_dropdown)
    dropdown.select_by_visible_text("Telecoms")
    logging.info("Industry 'Telecoms' selected.")
    log_to_csv("Industry 'Telecoms' selected.", "INFO")

    time.sleep(10)
    
    # Click the button
    button_selector = "p-button[ng-reflect-label^='Show me list of open demands,']"
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))

    start_time = time.time()

    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    button.click()
    logging.info("Button clicked successfully.")
    log_to_csv("Button clicked successfully.", "INFO")

    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p-table")))
    logging.info("Table is loaded and ready.")
    log_to_csv("Table is loaded and ready.", "INFO")

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
    expected_headers = ["GTD Task Name","Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"]

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
