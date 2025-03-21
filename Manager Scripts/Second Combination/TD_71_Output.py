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
import logging

# Setup Chrome WebDriver
driver = webdriver.Chrome()

# Define output directory
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
    # Navigate to the webpage
    driver.get("http://localhost:4200/assignmentAssistant")
    wait = WebDriverWait(driver, 300)  # Adjust timeout as necessary

    
    # Navigate to Manager Page
    manager_page_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p-button[ng-reflect-label^='Manager Page']"))
    )
    manager_page_button.click()
    logging.info("Navigated to Manager Page.")
    logging.info("Navigated to Manager Page.", "INFO")

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

    logging.info("Clicking on suggestion 3...")
    suggestion_button.click()

    time.sleep(2)

    # Select Customer dropdown
    cust_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[1]/select"))
    )
    cust_dropdown.click()
    logging.info("Clicked on Customer dropdown...")
    time.sleep(2)
    select_cust = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[1]/select/option[64]"))
    )
    select_cust.click()
    cust_dropdown.click()
    logging.info("Selected Customer from the dropdown...")
    time.sleep(2)

    # Scrolling to find Gradedropdown
    element = driver.find_element(By.XPATH,
                                  "//html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[5]/select")
    driver.execute_script("arguments[0].scrollIntoView()", element)
    time.sleep(2)
    logging.info("Scrolling to find the Grade dropdown")
    
     # Select Grade from dropdown
    Grade_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,"//html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[5]/select"))
    )
    Grade_dropdown.click()
    logging.info("Clicked on Grade...")
    time.sleep(2)
    select_Grade = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[2]/div/div[5]/select/option[6]"))
    )
    select_Grade.click()
    Grade_dropdown.click()
    logging.info("Selected Grade from the dropdown...")
    time.sleep(2)

    #Scrolling to find the show me list of demands button
    element = driver.find_element(By.XPATH, '/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/p-button/button/span')
    driver.execute_script("arguments[0].scrollIntoView()", element)
    time.sleep(2)
    logging.info("Scrolling to the Show me list submit button...")

    start_time = time.time()
    #Click on show me list of demands button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-staffing/app-main-layout/div/div/div[2]/div/div/div[3]/div/p-button/button/span"))
    )
    submit_button.click()
    logging.info("Submit button clicked...")

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

    # Expected headers for validation
    expected_headers = ["","GTD Task Name", "Grade", "GTD Location", "Match Band", "Rationale", "Resource Name"]

    if headers == expected_headers:
        logging.info("Table headers are correct.")
        log_to_csv("Table headers are correct.", "INFO")
    else:
        logging.warning(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}")
        log_to_csv(f"Headers mismatch! Expected: {expected_headers}, Found: {headers}", "WARNING")

    # Extract data and write to CSV
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

            # Check for next page
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
