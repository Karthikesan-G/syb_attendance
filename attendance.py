
##### Importing required modules #####

import os
import time
import warnings
import requests
import datetime
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
warnings.filterwarnings("ignore")
import base64
import json
import traceback

print("Installing Chromedriver...")
chromedriver_autoinstaller.install() 

current_year = datetime.datetime.now().year

current_date = datetime.datetime.now().strftime('%Y-%m-%d')

current_day_of_week = datetime.datetime.now().weekday()

work_place_location_id = 1

if __name__ == '__main__':
    
    pid = str(os.getpid())
    print('pid:' + pid)  

    try: 
        options1 = webdriver.ChromeOptions()  
        options1.add_argument("--headless")
        # options1.headless = True


        driver = webdriver.Chrome(options=options1)
        
        driver.delete_all_cookies()
        
        driver.get("https://sybrant-apt.greythr.com/uas/portal/auth/login")
        time.sleep(5)
        id_element = driver.find_element(By.ID, "username")
        id_element.send_keys("ST1081")
        time.sleep(2)
        encoded_password = "S2FydGhpa0A5NTQx" 
        decoded_password = base64.b64decode(encoded_password).decode('utf-8')
        pass_element = driver.find_element(By.ID, "password")
        pass_element.send_keys(decoded_password)
        time.sleep(2)
        login_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/uas-portal/div/div/main/div/section/div[1]/o-auth/section/div/app-login/section/div/div/div/form/button'))
        )
        login_element.click()
        time.sleep(15)
        print("Logged In...")

        cookies = driver.get_cookies()
        # print(cookies)

        session = requests.Session()

        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        holiday_url = f"https://sybrant-apt.greythr.com/v3/api/leave/holidays/{str(current_year)}"
        holiday_con_obj = session.get(holiday_url)
        print(f"CODE::: {holiday_con_obj.status_code}")
        holiday_con = holiday_con_obj.text

        holiday_con_json = json.loads(holiday_con)

        holidays = holiday_con_json["holidays"]
        if holidays:
            holiday_dates = []
            for holiday in holidays:
                holiday_dates.append(holiday["holidayDate"])
            print(holiday_dates)

            if current_date not in holiday_dates and current_day_of_week not in [5, 6]:

                sign_element = driver.find_element(By.XPATH, "/html/body/app/ng-component/div/div/div[2]/div/ghr-home/div[2]/div/gt-home-dashboard/div/div[2]/gt-component-loader/gt-attendance-info/div/div/div[3]/gt-button[1]")
                sign_element.click()
                time.sleep(5)
                print("Clicking Sign In or Sign Out...")
                
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "gt-popup-modal[open]"))
                )
                time.sleep(2)
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "gt-dropdown"))
                )
                time.sleep(2)
                shadow_root1 = driver.execute_script("return arguments[0].shadowRoot", dropdown)
                
                dropdown_button = WebDriverWait(shadow_root1, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown-button"))
                )
                dropdown_button.click()
                time.sleep(5)
                print("Clicking dropdown menu...")

                dropdown_items = WebDriverWait(shadow_root1, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-body .dropdown-item"))
                )
                time.sleep(2)

                dropdown_items[work_place_location_id].click()
                print("Selecting work location...")
                

                gt_button = driver.find_element(By.XPATH, '/html/body/app/ng-component/div/div/div[2]/div/ghr-home/div[2]/div/gt-home-dashboard/gt-popup-modal/div/div/div[2]/gt-button')

                shadow_root = driver.execute_script('return arguments[0].shadowRoot', gt_button)

                button = shadow_root.find_element(By.CSS_SELECTOR, 'button.btn-primary')

                print("Button text:", button.text)
                # button.click() 
                time.sleep(5)
                print("Done...")
                # log_out_button = driver.find_element(By.XPATH,"/html/body/app/ng-component/div/gt-topbar/nav/div[4]/a/div")
                # log_out_button.click()
                # print("Logged Out...")
                # time.sleep(5)
                driver.quit()
            else:
                print("Holiday...!")
                log_out_button = driver.find_element(By.XPATH,"/html/body/app/ng-component/div/gt-topbar/nav/div[4]/a/div")
                log_out_button.click()
                print("Logged Out...")
                time.sleep(5)
                driver.quit()
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Traceback: {error_traceback}\n")
        with open("Logs.txt", 'a', encoding='utf-8') as fh:
            fh.write(f"\nDate : {str(current_date)}\tException : {str(e)}\n")
            fh.write(f"Traceback: {error_traceback}\n")
            fh.write(f"#################################################################################\n")


        


    
