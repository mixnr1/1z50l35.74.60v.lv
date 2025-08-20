import re
import time
import smtplib, ssl
import config
import logging
from datetime import datetime
import os
import traceback
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = time.time()

# Set up logging
def setup_logging():
    """Setup logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Single log file that gets appended to
    log_filename = "logs/auto_script.log"
    
    # Configure logging to only show ERROR and WARNING messages
    logging.basicConfig(
        level=logging.WARNING,  # Only log WARNING and ERROR messages
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8', mode='a')  # Append mode
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

start_tuple=time.localtime()
start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_tuple)

# print("="*60)
# print("STARTING AUTO SCRIPT")
# print("="*60)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "Script started")
# print(f"Script started at: {start_time}") #add timestamp here
# print("="*60)

def navigation_pages():
    """Get pagination links from the results page"""
    try:
        navigator = driver.find_element(By.CLASS_NAME, 'pagination')
        pages = navigator.find_elements(By.TAG_NAME, 'a')
        not_sorted_links = []
        for page in pages:
            link = page.get_attribute("href")
            pattern = re.compile("http[s]?://izsoles.ta.gov.lv/(?:[0-9]+)")
            if pattern.match(str(link)):
                not_sorted_links.append(link)
        #print(f"Found {len(not_sorted_links)} pagination links")
        return sorted(set(not_sorted_links))
    except NoSuchElementException:
        logger.warning("No pagination found")
        return []
    except Exception as e:
        logger.error(f"Error in navigation_pages: {e}")
        return []

def create_html_table(results):
    """Create a complete HTML table with headers"""
    try:
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Auction Results</title>
    <style>
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f5f5f5; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Auction Results</h1>
    <table>
        <thead>
            <tr>
                <th>Sludinājuma virsraksts</th>
                <th>Novērtējums</th>
                <th>Sākumcena</th>
                <th>Izsoles kārta</th>
                <th>Izsoles statuss</th>
                <th>Izsoles sākums</th>
                <th>Izsoles noslēgums</th>
                <th>Izsoles rīkotājs</th>
            </tr>
        </thead>
        <tbody>
"""
        
        for result in results:
            html_content += result['html'] + "\n"
        
        html_content += """        </tbody>
    </table>
</body>
</html>"""
        
        #print("HTML table created successfully")
        return html_content
        
    except Exception as e:
        logger.error(f"Error creating HTML table: {e}")
        return ""

def extract_table_results():
    """Extract results from the auction table"""
    try:
        # Find the table with the specified class
        table = driver.find_element(By.CSS_SELECTOR, "table.table.table-bordered.auction-list.common-table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        
        #print(f"Found {len(rows)} rows in results table")
        
        page_results = []
        for i, row in enumerate(rows, 1):
            try:
                # Get all cells in the row
                cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 9:  # Ensure we have enough columns
                    # 1. td[1] - SLUDINĀJUMA VIRSRAKSTS (Auction Title & Link)
                    title = "N/A"
                    link = "N/A"
                    
                    # Try multiple approaches to extract title and link from td[1]
                    try:
                        # Approach 1: Try td[1]/div/div[2]/a
                        title_div = cells[0].find_element(By.CSS_SELECTOR, "div > div:nth-child(2)")
                        title_link = title_div.find_element(By.TAG_NAME, "a")
                        title = title_link.text.strip()
                        link = title_link.get_attribute("href")
                    except:
                        try:
                            # Approach 2: Try td[1]/div/a
                            title_div = cells[0].find_element(By.CSS_SELECTOR, "div")
                            title_link = title_div.find_element(By.TAG_NAME, "a")
                            title = title_link.text.strip()
                            link = title_link.get_attribute("href")
                        except:
                            try:
                                # Approach 3: Try td[1]/a directly
                                title_link = cells[0].find_element(By.TAG_NAME, "a")
                                title = title_link.text.strip()
                                link = title_link.get_attribute("href")
                            except:
                                try:
                                    # Approach 4: Try any link in td[1]
                                    title_link = cells[0].find_element(By.CSS_SELECTOR, "a")
                                    title = title_link.text.strip()
                                    link = title_link.get_attribute("href")
                                except:
                                    # Approach 5: Just get the text content of td[1]
                                    title = cells[0].text.strip()
                                    link = "N/A"
                    
                    # Clean up title and link
                    if not title or title == "":
                        title = "N/A"
                    if not link or link == "":
                        link = "N/A"
                    
                    # 2. td[3] - NOVĒRTĒJUMS (Valuation)
                    valuation = cells[2].text.strip() if len(cells) > 2 else "N/A"
                    
                    # 3. td[4] - SĀKUMCENA (Start Price)
                    start_price = cells[3].text.strip() if len(cells) > 3 else "N/A"
                    
                    # 4. td[5] - IZSOLES KĀRTA (Auction Stage)
                    auction_stage = cells[4].text.strip() if len(cells) > 4 else "N/A"
                    
                    # 5. td[6] - IZSOLES STATUSS (Auction Status)
                    auction_status = cells[5].text.strip() if len(cells) > 5 else "N/A"
                    
                    # 6. td[7] - IZSOLES SĀKUMS (Auction Start)
                    auction_start = cells[6].text.strip() if len(cells) > 6 else "N/A"
                    
                    # 7. td[8] - IZSOLES NOSLĒGUMS (Auction End)
                    auction_end = cells[7].text.strip() if len(cells) > 7 else "N/A"
                    
                    # 8. td[9] - IZSOLES RĪKOTĀJS (Auction Organizer)
                    auction_organizer = cells[8].text.strip() if len(cells) > 8 else "N/A"
                    
                    # Create HTML and plain text entries with all information
                    html_entry = f'''<tr>
                        <td><a href="{link}">{title}</a></td>
                        <td>{valuation}</td>
                        <td>{start_price}</td>
                        <td>{auction_stage}</td>
                        <td>{auction_status}</td>
                        <td>{auction_start}</td>
                        <td>{auction_end}</td>
                        <td>{auction_organizer}</td>
                    </tr>'''
                    
                    plain_entry = f"{link} - {title} | Valuation: {valuation} | Start Price: {start_price} | Stage: {auction_stage} | Status: {auction_status} | Start: {auction_start} | End: {auction_end} | Organizer: {auction_organizer}"
                    
                    page_results.append({
                        'html': html_entry,
                        'plain': plain_entry,
                        'title': title,
                        'link': link,
                        'valuation': valuation,
                        'start_price': start_price,
                        'auction_stage': auction_stage,
                        'auction_status': auction_status,
                        'auction_start': auction_start,
                        'auction_end': auction_end,
                        'auction_organizer': auction_organizer
                    })
                    
                    #print(f"Row {i}: {title[:30]}... | Price: {start_price} | Valuation: {valuation} | Status: {auction_status}")
                
            except Exception as e:
                logger.error(f"Error processing row {i}: {e}")
                continue
                
        #print(f"Successfully extracted {len(page_results)} results from table")
        return page_results
        
    except NoSuchElementException as e:
        logger.error(f"No results table found: {e}")
        return []
    except Exception as e:
        logger.error(f"Error processing results table: {e}")
        return []

def compare_and_update_csv(new_results, csv_file_path):
    """Compare new results with existing CSV and handle updates"""
    try:
        existing_records = []
        new_unique_records = []
        
        # Check if CSV file exists
        if os.path.exists(csv_file_path):
            #print(f"Existing CSV file found: {csv_file_path}")
            
            # Read existing records
            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                lines = csv_file.readlines()
                
                # Skip header line
                if len(lines) > 1:
                    for line in lines[1:]:  # Skip header
                        line = line.strip()
                        if line:
                            # Extract link from CSV line (link is in second column)
                            parts = line.split('","')
                            if len(parts) >= 2:
                                existing_link = parts[1].replace('"', '')
                                existing_records.append(existing_link)
            
            #print(f"Found {len(existing_records)} existing records in CSV")
            
            # Compare new results with existing records
            for result in new_results:
                if result['link'] not in existing_records and result['link'] != "N/A":
                    new_unique_records.append(result)
                    #print(f"New unique record found: {result['title'][:50]}...")
            
            #print(f"Found {len(new_unique_records)} new unique records")
            
            # Always overwrite the main CSV with all new data (including existing + new)
            with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
                csv_file.write("Title,Link,Valuation,Start Price,Auction Stage,Auction Status,Auction Start,Auction End,Auction Organizer\n")
                for result in new_results:
                    csv_file.write(f'"{result["title"]}","{result["link"]}","{result["valuation"]}","{result["start_price"]}","{result["auction_stage"]}","{result["auction_status"]}","{result["auction_start"]}","{result["auction_end"]}","{result["auction_organizer"]}"\n')
            
            #print(f"✓ Main CSV file updated with all {len(new_results)} records")
            return new_unique_records  # Return new records for TXT/HTML processing
        else:
            #print(f"CSV file does not exist, creating new file: {csv_file_path}")
            
            # Create new CSV file with all results
            with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
                csv_file.write("Title,Link,Valuation,Start Price,Auction Stage,Auction Status,Auction Start,Auction End,Auction Organizer\n")
                for result in new_results:
                    csv_file.write(f'"{result["title"]}","{result["link"]}","{result["valuation"]}","{result["start_price"]}","{result["auction_stage"]}","{result["auction_status"]}","{result["auction_start"]}","{result["auction_end"]}","{result["auction_organizer"]}"\n')
            
            #print(f"✓ New CSV file created with {len(new_results)} records")
            return new_results  # Return all records as "new" for first run
            
    except Exception as e:
        logger.error(f"Error in compare_and_update_csv: {e}")
        return []

def save_new_records_to_txt(new_unique_records, txt_file_path):
    """Save only new unique records to TXT file"""
    try:
        if new_unique_records:
            # Create temporary file with only new records
            temp_file_path = txt_file_path.replace('.txt', '_new_records.txt')
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                for result in new_unique_records:
                    temp_file.write(result['plain'] + '\n')
            
            #print(f"✓ New unique records saved to: {temp_file_path}")
        #     print(f"✓ Saved {len(new_unique_records)} new records to TXT")
        # else:
        #     print("No new records to save to TXT file")
            
    except Exception as e:
        logger.error(f"Error saving new records to TXT: {e}")

def save_new_records_to_html(new_unique_records, html_file_path):
    """Save only new unique records to HTML file"""
    try:
        if new_unique_records:
            # Create temporary file with only new records
            temp_file_path = html_file_path.replace('.html', '_new_records.html')
            temp_html = create_html_table(new_unique_records)
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                temp_file.write(temp_html)
            
            # print(f"✓ New unique records saved to: {temp_file_path}")
        #     print(f"✓ Saved {len(new_unique_records)} new records to HTML")
        # else:
        #     print("No new records to save to HTML file")
            
    except Exception as e:
        logger.error(f"Error saving new records to HTML: {e}")

def save_complete_results_to_files(all_results, txt_file_path, html_file_path):
    """Save complete results to TXT and HTML files (overwrites existing)"""
    try:
        # Save complete plain text results
        with open(txt_file_path, 'w', encoding='utf-8') as text_file:
            for result in all_results:
                text_file.write(result['plain'] + '\n')
        #print(f"✓ Complete results saved to: {txt_file_path}")
        
        # Save complete HTML results
        complete_html = create_html_table(all_results)
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(complete_html)
        #print(f"✓ Complete results saved to: {html_file_path}")
        
    except Exception as e:
        logger.error(f"Error saving complete results: {e}")

#print("Starting auto script based on auto.side file...")

# Initialize variables for storing results
HTML_text = []
plain_text = []
all_results = []  # Store complete result dictionaries

# Set up Chrome options - VISIBLE MODE
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Keep visible for debugging
# chrome_options.add_argument("--window-size=1414x810")  # Same as auto.side
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

try:
    #print("Initializing Chrome driver...")
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented out for visible mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1414,810")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    #print("Chrome driver initialized successfully")
    
    # Step 1: Open the website
    #print("Step 1: Opening website...")
    driver.get('https://izsoles.ta.gov.lv/')
    time.sleep(2)
    #print("✓ Website opened successfully")
    
    # Step 2: Click "Izvērstā meklēšana" (Expand search)
    #print("Step 2: Clicking 'Izvērstā meklēšana'...")
    expand_search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dotted-underline")))
    expand_search.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Expanded search clicked")
    
    # Step 3: Click "Pārdošanas veids"
    #print("Step 3: Clicking 'Pārdošanas veids'...")
    sales_type_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(1) .filter-option")))
    sales_type_dropdown.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Sales Type dropdown clicked")
    
    # Step 4: Select "Īpašumtiesības"
    #print("Step 4: Selecting 'Īpašumtiesības'...")
    ipasumtiesibas_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(1) li:nth-child(2) .text")))
    ipasumtiesibas_option.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Selected 'Īpašumtiesības'")
    
    # Step 5: Click "Tips"
    #print("Step 5: Clicking 'Tips'...")
    type_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(3) .filter-option")))
    type_dropdown.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Type dropdown clicked")
    
    # Step 6: Select "Kustamā manta"
    #print("Step 6: Selecting 'Kustamā manta'...")
    kustama_manta_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(3) li:nth-child(3) .text")))
    kustama_manta_option.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Selected 'Kustamā manta'")
    
    # Step 7: Click "Kategorija"
    #print("Step 7: Clicking 'Kategorija'...")
    category_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(4) .filter-option")))
    category_dropdown.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Category dropdown clicked")
    
    # Step 8: Select "Transportlīdzekļi" 
    #print("Step 8: Selecting 'Transportlīdzekļi'...")
    transportlizekli_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li:nth-child(2) > .category_option > .text")))
    transportlizekli_option.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Selected 'Transportlīdzekļi'")
    
    # Step 9: Click Start Price From field
    #print("Step 9: Clicking Start Price From field...")
    start_price_from = wait.until(EC.element_to_be_clickable((By.ID, "start-price-from")))
    start_price_from.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Start Price From field clicked")
    
    # Step 10: Type in Start Price From
    #print("Step 10: Typing in Start Price From...")
    start_price_from.clear()
    start_price_from.send_keys("10000")
    time.sleep(1)  # 1 second sleep after typing
    #print("✓ Typed '1000' in Start Price From")
    
    # Step 11: Click Start Price To field
    #print("Step 11: Clicking Start Price To field...")
    start_price_to = wait.until(EC.element_to_be_clickable((By.ID, "start-price-to")))
    start_price_to.click()
    time.sleep(1)  # 1 second sleep after click
    #print("✓ Start Price To field clicked")
    
    # Step 12: Type in Start Price To
    #print("Step 12: Typing in Start Price To...")
    start_price_to.clear()
    start_price_to.send_keys("25000")
    time.sleep(1)  # 1 second sleep after typing
    #print("✓ Typed '11000' in Start Price To")
    
    # # Step 13: Click Valuation From field
    # valuation_from = wait.until(EC.element_to_be_clickable((By.ID, "valuation-from")))
    # valuation_from.click()
    # time.sleep(1)  # 1 second sleep after click
    # # Step 14: Type in Valuation From
    # valuation_from.clear()
    # valuation_from.send_keys("1000")
    # time.sleep(1)  # 1 second sleep after typing
    
    # # Step 15: Click Valuation To field
    # valuation_to = wait.until(EC.element_to_be_clickable((By.ID, "valuation-to")))
    # valuation_to.click()
    # time.sleep(1)  # 1 second sleep after click
    # # Step 16: Type in Valuation To
    # valuation_to.clear()
    # valuation_to.send_keys("11000")
    # time.sleep(1)  # 1 second sleep after typing

    
    # Step 17: Click Search button
    #print("Step 17: Clicking Search button...")
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-button .search")))
    search_button.click()
    time.sleep(3)  # Wait longer for search results to load
    #print("✓ Search button clicked")
    
    # Step 18: Extract results from table and handle pagination
    #print("Step 18: Extracting search results...")
    
    # Get pagination links
    pagination_links = navigation_pages()
    #print(f"Found {len(pagination_links)} pagination links")
    
    # Process first page
    #print("Processing page 1...")
    first_page_results = extract_table_results()
    HTML_text.extend(first_page_results)
    plain_text.extend([result['plain'] for result in first_page_results])
    all_results.extend(first_page_results) # Add to all_results
    #print(f"✓ Page 1: Found {len(first_page_results)} results")
    
    # Process additional pages
    for i, page_link in enumerate(pagination_links, 2):
        #print(f"Processing page {i}: {page_link}")
        driver.get(page_link)
        time.sleep(2)  # Wait for page to load
        
        page_results = extract_table_results()
        HTML_text.extend(page_results)
        plain_text.extend([result['plain'] for result in page_results])
        plain_text.extend([result['plain'] for result in page_results])
        all_results.extend(page_results) # Add to all_results
        #print(f"✓ Page {i}: Found {len(page_results)} results")
    
    # Print summary
    # print("="*60)
    # print("SEARCH RESULTS SUMMARY")
    # print("="*60)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Total results found: {len(HTML_text)}")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Total pages processed: {len(pagination_links) + 1}")
    
    # Save results to files
    try:
        path = config.path
        #print(f"Saving results to: {path}")
        
        # Compare and update CSV file (single source of truth)
        new_unique_records_from_csv = compare_and_update_csv(all_results, path+"/auction_results_detailed.csv")
        #print("✓ CSV file comparison completed")
        
        # Save new unique records to TXT and HTML files
        save_new_records_to_txt(new_unique_records_from_csv, path+"/unique_links_plain_auto.txt")
        save_new_records_to_html(new_unique_records_from_csv, path+"/auction_results_complete.html")
        
        # Save complete results to TXT and HTML files (overwrites existing)
        save_complete_results_to_files(all_results, path+"/unique_links_plain_auto.txt", path+"/auction_results_complete.html")
        
        # Summary of new records found
        total_new_records = len(new_unique_records_from_csv)
        if total_new_records > 0:
            # print("="*60)
            # print("NEW RECORDS DETECTED!")
            # print("="*60)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Found {total_new_records} new unique records")
            # print("New unique records have been saved to:")
            # print("- unique_links_plain_auto_new_records.txt")
            # print("- auction_results_complete_new_records.html")
            # print("Complete results saved to:")
            # print("- auction_results_detailed.csv (all records)")
            # print("- unique_links_plain_auto.txt (all records)")
            # print("- auction_results_complete.html (all records)")
        else:
            # print("="*60)
            # print("NO NEW RECORDS FOUND")
            # print("="*60)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "No new records found")
            # print("All existing records are up to date")
            # print("Complete results saved to:")
            # print("- auction_results_detailed.csv (all records)")
            # print("- unique_links_plain_auto.txt (all records)")
            # print("- auction_results_complete.html (all records)")
        
        # print("="*60)
        # print("✓ All files updated successfully!")
        # print("="*60)
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise
    
    # Close the browser after successful completion
    # print("Closing browser...")
    try:
        driver.quit()
        # print("✓ Browser closed successfully")
    except Exception as e:
        # print(f"Warning: Could not close browser gracefully: {e}")
        try:
            driver.close()
            # print("✓ Browser closed with close() method")
        except:
            print("Warning: Could not close browser - may need manual cleanup")
    
except Exception as e:
    logger.error(f"Error during execution: {e}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Close browser even if there's an error
    try:
        # print("Closing browser due to error...")
        driver.quit()
        # print("✓ Browser closed successfully")
    except Exception as close_error:
        # print(f"Warning: Could not close browser gracefully: {close_error}")
        try:
            driver.close()
            # print("✓ Browser closed with close() method")
        except:
            # print("Warning: Could not close browser - may need manual cleanup")
            logger.error("Failed to close browser - manual cleanup required")

# Script completion
end = time.time()
end_tuple = time.localtime()
end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_tuple)
# print("="*60)
# print("SCRIPT COMPLETION SUMMARY")
# print("="*60)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Script ended: {end_time}")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"Script running time: {time.strftime('%H:%M:%S', time.gmtime(end - start))}")
# print("="*60)