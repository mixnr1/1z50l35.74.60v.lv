import time
import re
import os
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Set up logging
def setup_logging():
    """Setup logging configuration"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Single log file that gets appended to
    log_filename = "logs/land_script.log"
    
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

# Region dictionary mapping region names to their XPath selectors
regionu_dic = {
    #"Visas vietas": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[1]/a/span[1]",
    # "Daugavpils": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[2]/a/span[1]",
    # "Jelgava": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[3]/a/span[1]",
    # "Jūrmala": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[4]/a/span[1]",
    # "Liepāja": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[5]/a/span[1]",
    # "Rēzekne": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[6]/a/span[1]",
    # "Rīga": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[7]/a/span[1]",
    # "Ventspils": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[8]/a/span[1]",
    # "Ādažu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[9]/a/span[1]",
    # "Aizkraukles novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[10]/a/span[1]",
    # "Alūksnes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[11]/a/span[1]",
    # "Balvu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[12]/a/span[1]",
    # "Bauskas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[13]/a/span[1]",
    # "Cēsu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[14]/a/span[1]",
    # "Daugavpils novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[15]/a/span[1]",
    # "Dobeles novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[16]/a/span[1]",
    # "Gulbenes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[17]/a/span[1]",
    # "Jēkabpils novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[18]/a/span[1]",
    # "Jelgavas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[19]/a/span[1]",
    # "Ķekavas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[20]/a/span[1]",
    # "Krāslavas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[21]/a/span[1]",
    # "Kuldīgas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[22]/a/span[1]",
    # "Limbažu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[23]/a/span[1]",
    # "Līvānu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[24]/a/span[1]",
    # "Ludzas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[25]/a/span[1]",
    # "Madonas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[26]/a/span[1]",
    # "Mārupes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[27]/a/span[1]",
    # "Ogres novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[28]/a/span[1]",
    # "Olaines novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[29]/a/span[1]",
    # "Preiļu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[30]/a/span[1]",
    # "Rēzeknes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[31]/a/span[1]",
    # "Ropažu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[32]/a/span[1]",
    #"Salaspils novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[33]/a/span[1]",
    # "Saldus novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[34]/a/span[1]",
    # "Saulkrastu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[35]/a/span[1]",
    # "Siguldas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[36]/a/span[1]",
    "Smiltenes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[37]/a/span[1]",
    "Talsu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[38]/a/span[1]",
    # "Tukuma novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[39]/a/span[1]",
    # "Valkas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[40]/a/span[1]",
    # "Varakļānu novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[41]/a/span[1]",
    # "Ventspils novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[42]/a/span[1]",
    # "Ārzemes": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[43]/a/span[1]",
    # "Liepājas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[44]/a/span[1]",
    # "Valmieras novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[45]/a/span[1]",
    # "Augšdaugavas novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[46]/a/span[1]",
    "Dienvidkurzemes novads": "/html/body/div[3]/div[2]/form[2]/div[1]/div[2]/div/div/ul/li[47]/a/span[1]"
}

# Category dictionary mapping category names to their XPath selectors
category_dic = {
    # "Visas kategorijas": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[1]/a/span[1]",
    "Zeme/mežs": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[2]/a/span[1]"
    # "Ēkas": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[3]/a/span[1]",
    # "Dzīvokļi": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[4]/a/span[1]",
    # "Dažādi": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[5]/a/span[1]",
    # "Funkcionāli saistīti īpašumi/kopīpašums": "/html/body/div[3]/div[2]/form[2]/div[1]/div[4]/div/div/ul/li[6]/a/span[1]"
}

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # Add options to prevent browser from closing automatically
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1864,769")
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
    return driver

def navigation_pages(driver):
    """Get pagination links from the results page"""
    try:
        # First check if pagination exists
        try:
            navigator = driver.find_element(By.CLASS_NAME, 'pagination')
            print("Pagination found, extracting links...")
        except NoSuchElementException:
            print("No pagination found - single page results")
            return []
        
        # Get all pagination links
        pages = navigator.find_elements(By.TAG_NAME, 'a')
        print(f"Found {len(pages)} pagination elements")
        
        not_sorted_links = []
        for i, page in enumerate(pages, 1):
            try:
                link = page.get_attribute("href")
                if link:
                    pattern = re.compile("http[s]?://izsoles.ta.gov.lv/(?:[0-9]+)")
                    if pattern.match(str(link)):
                        not_sorted_links.append(link)
                        print(f"Page {i}: {link}")
                    else:
                        print(f"Page {i}: Skipped (not a valid pagination link)")
                else:
                    print(f"Page {i}: No href attribute")
            except Exception as e:
                print(f"Page {i}: Error extracting link - {e}")
        
        sorted_links = sorted(set(not_sorted_links))
        print(f"Total valid pagination links: {len(sorted_links)}")
        return sorted_links
        
    except Exception as e:
        logger.error(f"Error in navigation_pages: {e}")
        print(f"Error extracting pagination: {e}")
        return []

def create_html_table(results):
    """Create a complete HTML table with headers"""
    try:
        html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Land Auction Results</title>
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
    <h1>Land Auction Results</h1>
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
        
        return html_content
        
    except Exception as e:
        logger.error(f"Error creating HTML table: {e}")
        return ""

def extract_table_results(driver):
    """Extract results from the auction table"""
    try:
        # First check if there's a table with results
        try:
            table = driver.find_element(By.CSS_SELECTOR, "table.table.table-bordered.auction-list.common-table")
        except NoSuchElementException:
            print("No results table found - no auction results for this search")
            return []
        
        # Check if table has any rows
        try:
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")
            
            if not rows:
                print("Table found but no rows - no auction results for this search")
                return []
                
        except NoSuchElementException:
            print("Table found but no tbody - no auction results for this search")
            return []
        
        #print(f"Found table with {len(rows)} rows")
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
                    
                    print(f"Row {i}: {title[:50]}... | Price: {start_price} | Status: {auction_status}")
                
            except Exception as e:
                logger.error(f"Error processing row {i}: {e}")
                continue
                
        #print(f"Successfully extracted {len(page_results)} results from table")
        return page_results
        
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
            
            # Compare new results with existing records
            for result in new_results:
                if result['link'] not in existing_records and result['link'] != "N/A":
                    new_unique_records.append(result)
            
            # Always overwrite the main CSV with all new data (including existing + new)
            with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
                csv_file.write("Title,Link,Valuation,Start Price,Auction Stage,Auction Status,Auction Start,Auction End,Auction Organizer\n")
                for result in new_results:
                    csv_file.write(f'"{result["title"]}","{result["link"]}","{result["valuation"]}","{result["start_price"]}","{result["auction_stage"]}","{result["auction_status"]}","{result["auction_start"]}","{result["auction_end"]}","{result["auction_organizer"]}"\n')
            
            return new_unique_records  # Return new records for TXT/HTML processing
        else:
            # Create new CSV file with all results
            with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
                csv_file.write("Title,Link,Valuation,Start Price,Auction Stage,Auction Status,Auction Start,Auction End,Auction Organizer\n")
                for result in new_results:
                    csv_file.write(f'"{result["title"]}","{result["link"]}","{result["valuation"]}","{result["start_price"]}","{result["auction_stage"]}","{result["auction_status"]}","{result["auction_start"]}","{result["auction_end"]}","{result["auction_organizer"]}"\n')
            
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
            
    except Exception as e:
        logger.error(f"Error saving new records to HTML: {e}")

def save_complete_results_to_files(all_results, txt_file_path, html_file_path):
    """Save complete results to TXT and HTML files (overwrites existing)"""
    try:
        # Save complete plain text results
        with open(txt_file_path, 'w', encoding='utf-8') as text_file:
            for result in all_results:
                text_file.write(result['plain'] + '\n')
        
        # Save complete HTML results
        complete_html = create_html_table(all_results)
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(complete_html)
        
    except Exception as e:
        logger.error(f"Error saving complete results: {e}")

def perform_single_search(driver, category_name, category_xpath, region_name, region_xpath):
    """Perform search for a single category-region combination"""
    try:
        # Step 1: Open the page
        #print(f"Opening page: https://izsoles.ta.gov.lv/ for {category_name} - {region_name}")
        driver.get("https://izsoles.ta.gov.lv/")
        time.sleep(1)  # 1 second pause
        
        # Step 2: Set window size to 1864x769
        #print("Setting window size to 1864x769")
        driver.set_window_size(1864, 769)
        time.sleep(1)  # 1 second pause
        
        # Step 3: Click on "Izvērstā meklēšana" (expanded search)
        #print("Clicking on expanded search")
        expanded_search = driver.find_element(By.CSS_SELECTOR, ".dotted-underline")
        expanded_search.click()
        time.sleep(1)  # 1 second pause
        
        # Step 4: Click on property rights dropdown (pārdošānas veids)
        #print("Clicking on property rights dropdown")
        property_rights_dropdown = driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(1) .filter-option")
        property_rights_dropdown.click()
        time.sleep(1)  # 1 second pause
        
        # Step 5: Select "Īpašumtiesības" (li[2])
        #print("Selecting Īpašumtiesības")
        property_rights_option = driver.find_element(By.XPATH, "//li[2]/a/span")
        property_rights_option.click()
        time.sleep(1)  # 1 second pause
        
        # Step 6: Click on the region dropdown
        #print("Clicking on region dropdown")
        region_dropdown = driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(2) .filter-option")
        region_dropdown.click()
        time.sleep(1)  # 1 second pause
        
        # Step 7: Select region using XPath from dictionary
        #print(f"Selecting {region_name}")
        region_option = driver.find_element(By.XPATH, region_xpath)
        region_option.click()
        time.sleep(1)  # 1 second pause
        
        # Step 8: Click on the type dropdown (tips)
        #print("Clicking on type dropdown")
        type_dropdown = driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(3) .filter-option")
        type_dropdown.click()
        time.sleep(1)  # 1 second pause
        
        # Step 9: Select "Nekustamie īpašumi" (li[2])
        #print("Selecting Nekustamie īpašumi")
        nekustamie_ipasumi_option = driver.find_element(By.XPATH, "//div[3]/div/div/ul/li[2]/a/span")
        nekustamie_ipasumi_option.click()
        time.sleep(1)  # 1 second pause
        
        # Step 10: Click on the category dropdown (kategorija)
        #print("Clicking on category dropdown")
        category_dropdown = driver.find_element(By.CSS_SELECTOR, ".row:nth-child(1) > .form-group:nth-child(4) .filter-option")
        category_dropdown.click()
        time.sleep(1)  # 1 second pause
        
        # Step 11: Select category using XPath from dictionary
        #print(f"Selecting {category_name}")
        category_option = driver.find_element(By.XPATH, category_xpath)
        category_option.click()
        time.sleep(1)  # 1 second pause
        
        # Step 12: Click and fill start price from
        #print("Filling start price from")
        start_price_from = driver.find_element(By.ID, "start-price-from")
        start_price_from.click()
        start_price_from.clear()
        start_price_from.send_keys("5000")
        time.sleep(1)  # 1 second pause
        
        # Step 13: Click and fill start price to
        #print("Filling start price to")
        start_price_to = driver.find_element(By.ID, "start-price-to")
        start_price_to.click()
        start_price_to.clear()
        start_price_to.send_keys("50000")
        time.sleep(1)  # 1 second pause
        
        # Step 14: Click and fill valuation from
        #print("Filling valuation from")
        valuation_from = driver.find_element(By.ID, "valuation-from")
        valuation_from.click()
        valuation_from.clear()
        valuation_from.send_keys("5000")
        time.sleep(1)  # 1 second pause
        
        # Step 15: Click and fill valuation to
        #print("Filling valuation to")
        valuation_to = driver.find_element(By.ID, "valuation-to")
        valuation_to.click()
        valuation_to.clear()
        valuation_to.send_keys("50000")
        time.sleep(1)  # 1 second pause
        
        # Step 16: Click search button
        #print("Clicking search button")
        search_button = driver.find_element(By.NAME, "init-search-full")
        search_button.click()
        time.sleep(3)  # Wait longer for search results to load
        
        # Step 17: Extract results from table and handle pagination
        #print("Extracting search results...")
        
        # Initialize results collection
        all_results = []
        
        # Check if there are any results first
        try:
            # Try to find the table
            table = driver.find_element(By.CSS_SELECTOR, "table.table.table-bordered.auction-list.common-table")
            print("Results table found, processing...")
        except NoSuchElementException:
            print("No results table found - no auction results for this search")
            return [] # Return empty list for this combination
        
        # Process first page
        print("Processing page 1...")
        first_page_results = extract_table_results(driver)
        all_results.extend(first_page_results)
        print(f"✓ Page 1: Found {len(first_page_results)} results")
        
        # Check for pagination
        try:
            pagination_links = navigation_pages(driver)
            print(f"Found {len(pagination_links)} pagination links")
            
            # Process additional pages if they exist
            if pagination_links:
                for i, page_link in enumerate(pagination_links, 2):
                    print(f"Processing page {i}: {page_link}")
                    try:
                        driver.get(page_link)
                        time.sleep(2)  # Wait for page to load
                        
                        page_results = extract_table_results(driver)
                        all_results.extend(page_results)
                        print(f"✓ Page {i}: Found {len(page_results)} results")
                        
                    except Exception as e:
                        logger.error(f"Error processing page {i}: {e}")
                        print(f"Error processing page {i}, continuing with next page...")
                        continue
            else:
                print("No pagination found - single page results")
                
        except Exception as e:
            logger.error(f"Error checking pagination: {e}")
            print("Error checking pagination, continuing with single page results...")
        
        print(f"Total results found: {len(all_results)}")
        print(f"Total pages processed: {len(pagination_links) + 1 if pagination_links else 1}")
        
        print(f"Search completed successfully for {category_name} - {region_name}!")
        return all_results # Return all results for this combination
        
    except Exception as e:
        print(f"An error occurred for {category_name} - {region_name}: {e}")
        return [] # Return empty list on error

def perform_regions_kategorija_operations():
    """Perform search operations for all category-region combinations"""
    total_combinations = len(category_dic) * len(regionu_dic)
    current_combination = 0
    
    # Initialize global results collection
    all_global_results = []
    
    print(f"Starting search operations for {total_combinations} category-region combinations...")
    
    for category_name, category_xpath in category_dic.items():
        for region_name, region_xpath in regionu_dic.items():
            current_combination += 1
            print(f"\n--- Combination {current_combination}/{total_combinations}: {category_name} - {region_name} ---")
            
            # Create new driver for each combination
            driver = setup_driver()
            
            try:
                # Perform the search for this combination
                combination_results = perform_single_search(driver, category_name, category_xpath, region_name, region_xpath)
                
                # Add results to global collection
                if combination_results:
                    all_global_results.extend(combination_results)
                    print(f"Added {len(combination_results)} results from {category_name} - {region_name}")
                else:
                    print(f"No results found for {category_name} - {region_name}")
                
                # Wait a bit before closing
                time.sleep(3)
                
            except Exception as e:
                print(f"Error in main loop for {category_name} - {region_name}: {e}")
            
            finally:
                # Always close the browser securely
                try:
                    print(f"Closing browser for {category_name} - {region_name}")
                    driver.quit()
                except Exception as e:
                    print(f"Error closing browser: {e}")
                
                # Small delay between combinations
                time.sleep(1)
    
    # Save all accumulated results to files at the end
    print(f"\nAll {total_combinations} combinations completed!")
    print(f"Total results collected: {len(all_global_results)}")
    
    if all_global_results:
        try:
            # Define file paths
            csv_file_path = "land_auction_results_detailed.csv"
            txt_file_path = "land_auction_results_plain.txt"
            html_file_path = "land_auction_results_complete.html"
            
            # Compare and update CSV file with all accumulated results
            new_unique_records_from_csv = compare_and_update_csv(all_global_results, csv_file_path)
            print("✓ CSV file comparison completed")
            
            # Save new unique records to TXT and HTML files
            save_new_records_to_txt(new_unique_records_from_csv, txt_file_path)
            save_new_records_to_html(new_unique_records_from_csv, html_file_path)
            
            # Save complete results to TXT and HTML files (overwrites existing)
            save_complete_results_to_files(all_global_results, txt_file_path, html_file_path)
            
            # Summary of new records found
            total_new_records = len(new_unique_records_from_csv)
            if total_new_records > 0:
                print(f"Found {total_new_records} new unique records across all combinations")
                print("New unique records have been saved to:")
                print("- land_auction_results_plain_new_records.txt")
                print("- land_auction_results_complete_new_records.html")
            else:
                print("No new records found across all combinations")
            
            print("Complete results saved to:")
            print("- land_auction_results_detailed.csv (all records from all combinations)")
            print("- land_auction_results_plain.txt (all records from all combinations)")
            print("- land_auction_results_complete.html (all records from all combinations)")
            
        except Exception as e:
            logger.error(f"Error saving final results: {e}")
            raise
    else:
        print("No results found across all combinations")
        # Save empty results to files
        try:
            csv_file_path = "land_auction_results_detailed.csv"
            txt_file_path = "land_auction_results_plain.txt"
            html_file_path = "land_auction_results_complete.html"
            
            new_unique_records_from_csv = compare_and_update_csv(all_global_results, csv_file_path)
            save_new_records_to_txt(new_unique_records_from_csv, txt_file_path)
            save_new_records_to_html(new_unique_records_from_csv, html_file_path)
            save_complete_results_to_files(all_global_results, txt_file_path, html_file_path)
            
            print("Empty results saved to files")
            
        except Exception as e:
            logger.error(f"Error saving empty results: {e}")
            raise

if __name__ == "__main__":
    perform_regions_kategorija_operations()

