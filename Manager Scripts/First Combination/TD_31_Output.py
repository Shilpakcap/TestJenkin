from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import os

driver = webdriver.Chrome()

# Get the script name without extension and CSV path define
script_name = os.path.splitext(os.path.basename(__file__))[0]

csv_directory = os.path.join("C:\\Shilpa\\GenAI", "Scripts_Results", script_name)
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

csv_file_path = os.path.join(csv_directory, "output_data.csv")

try:
    driver.get("http://10.207.20.55:4200/assignmentAssistant")
    wait = WebDriverWait(driver, 100)
    print("Website loaded successfully.")

    # Step 1: Click the desired suggestion
    print("Waiting for the suggestion container...")
    suggestion_list_container = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-group.shadow-sm.rounded.ng-star-inserted"))
    )
    suggestions = suggestion_list_container.find_elements(By.TAG_NAME, "a")

    desired_text = "4.Show me list of relevant open demands"
    for suggestion in suggestions:
        if desired_text in suggestion.text:
            print(f"Clicking on suggestion: {suggestion.text.strip()}")
            suggestion.click()
            break
    else:
        print(f"Desired suggestion '{desired_text}' not found.")
        driver.quit()
        exit()


    submit_query = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.p-ripple.p-button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_query)

    # Record the time before submitting the query
    start_time = time.time()
    submit_query.click()

    #Wait for the grid/table to load
    grid = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ag-root-wrapper-body")))
    rows = grid.find_elements(By.CSS_SELECTOR, "div.ag-row")
    #print(f"Number of rows: {len(rows)}")

    # Record the time after the grid has loaded
    end_time = time.time()

    # Calculate response time
    response_time = end_time - start_time
    print(f"Query response time: {response_time:.2f} seconds")

    # Extract rows
    rows = grid.find_elements(By.CSS_SELECTOR, "div.ag-row")
    print(f"Number of rows: {len(rows)}")

    # Extract header (if applicable)
    header = grid.find_elements(By.CSS_SELECTOR, "div.ag-header-cell")
    actual_headers = [cell.text.strip() for cell in header]
    expected_headers = [
        "GTD Task Name", "GTD Task Skills", "Grade", "GTD Location", "Percentage Match", "Rationale", "Resource Name"
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
        writer.writerow(actual_headers)

        # Extract and validate rows
        for i, row in enumerate(rows, start=1):
            cells = row.find_elements(By.CSS_SELECTOR, "div.ag-cell")
            cell_data = [cell.text.strip() for cell in cells]
            #print(f"Row {i}: {cell_data}")
            
            # Write each row of data to the CSV
            writer.writerow(cell_data)

            # Example: Validate "Percentage Match" column (5th column, index 4)
            if len(cell_data) >= 5:  # Ensure the column exists
                if not re.match(r"^\d+(\.\d+)?$", cell_data[4]):
                    print(f"Row {i}, Column 5 (Percentage Match) is not in the correct format: {cell_data[4]}")

    print(f"Data has been saved to {csv_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()