from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

LOGIN_URL = "https://admin.sbmurban.org/u/login"  
TARGET_URL = "https://admin.sbmurban.org/user/OFFICIAL/proposals/STATE/CSAP/consolidated-plans/478;sectors=CST"
USERNAME = "nodal.officer@mp"
PASSWORD = "SBMMP@state1"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
all_data = []

try:
    print("Navigating to the Login Page...")
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,30)

    try:
        user_field = wait.until(EC.presence_of_element_located((By.ID,"mat-input-0")))
        user_field.send_keys(USERNAME)

        pass_field = driver.find_element(By.ID, "mat-input-1")
        pass_field.send_keys(PASSWORD)
    except:
        print("Pls Type the CAPTCHA")

    print("\n" + "="*60)
    print("ACTION REQUIRED: The script is paused.")
    print("1. Go to the browser window.")
    print("2. Type the CAPTCHA and click 'Sign In'.")
    print("3. Wait until you are successfully logged in.")
    print("4. Come back here and PRESS ENTER to continue...")
    print("="*60 + "\n")
    input() 
    
    print("Jumping to the Target Page..")
    driver.get(TARGET_URL)
    
    while True:
        print("Waiting for the data...")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"mat-row")))
        time.sleep(3)

        rows = driver.find_elements(By.CLASS_NAME,"mat-row")
        for row in rows:
            cells = row.find_elements(By.CLASS_NAME,"mat-cell")
            row_text = [cell.text.strip() for cell in cells]
        

            if len(row_text) >=8:
                all_data.append({
                    'Action Plan Id': row_text[0],
                    'Action Plan Cost': row_text[3],
                    'Central Share':row_text[4],
                    'State Share':row_text[5],
                    'ULB Share':row_text[6] if len(row_text) > 6 else""
                    })
        
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next page']")
            
            if next_btn.get_attribute("disabled") == "true" or "disabled" in next_btn.get_attribute("class"):
                print("reached the last page")
                break
            next_btn.click()
            time.sleep(3)

        except Exception:
            print("no next Button found")
            break

    df = pd.DataFrame(all_data)
    df.to_csv('results.csv', index=False)

except Exception as e:
    print(f"an error occured:{e}")

#finally:
#    driver.quit()
