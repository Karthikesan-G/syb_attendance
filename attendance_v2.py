""" 
    Attendance Automation Script Without Holiday Logic
    Need to manually update holiday dates for each months or whole year holidays in the code.
"""


##### Importing required modules #####

import os
import time
import warnings
import requests
import datetime
import pytz
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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 800))  
display.start()

ist = pytz.timezone('Asia/Kolkata')

current_year = datetime.datetime.now(ist).year

current_date = datetime.datetime.now(ist).strftime('%Y-%m-%d')
print(f"DATE:::{current_date}")

current_day_of_week = datetime.datetime.now(ist).weekday()

work_place_location_id = 1
SYB_EMAIL_PASSWORD = os.getenv('SYB_EMAIL_PASSWORD')
SYB_ATTENDANCE_PORTAL_PASSWORD = os.getenv('SYB_ATTENDANCE_PORTAL_PASSWORD')

def confirm_mail_send(mail_status):
    sender_email = "karthikesan.g@sybrantdigital.com"
    receiver_email = "karthikesan.g@sybrantdigital.com"
    password = SYB_EMAIL_PASSWORD

    current_time = datetime.datetime.now(ist).strftime("%I:%M:%S %p")
    subject = "Attendance Mail"
    body = f"{mail_status} Time : {current_time}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.zoho.com', 587)
        server.starttls() 
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

    finally:
        server.quit()

if __name__ == '__main__':
    
    pid = str(os.getpid())
    print('pid:' + pid)  

    print("Installing Chromedriver...")
    chromedriver_autoinstaller.install() 

    try: 
        options1 = webdriver.ChromeOptions()  
        # options1.add_argument("--headless")
        # options1.headless = True


        driver = webdriver.Chrome(options=options1)
        
        driver.delete_all_cookies()
        
        driver.get("https://sybrant-apt.greythr.com/uas/portal/auth/login")
        time.sleep(5)
        id_element = driver.find_element(By.ID, "username")
        id_element.send_keys("ST1081")
        time.sleep(2)
        encoded_password = "" 
        decoded_password = base64.b64decode(encoded_password).decode('utf-8')
        pass_element = driver.find_element(By.ID, "password")
        pass_element.send_keys(SYB_ATTENDANCE_PORTAL_PASSWORD)
        time.sleep(2)
        login_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/uas-portal/div/div/main/div/section/div[1]/o-auth/section/div/app-login/section/div/div/div/form/button'))
        )
        login_element.click()
        time.sleep(15)
        print("Logged In...")

        holiday_dates = ['2025-01-01', '2025-01-13', '2025-01-14', '2025-01-26', '2025-02-04', '2025-02-10']
        print(holiday_dates)

        if current_date not in holiday_dates and current_day_of_week not in [5, 6]:

            sign_element = driver.find_element(By.XPATH, "/html/body/app/ng-component/div/div/div[2]/div/ghr-home/div[2]/div/gt-home-dashboard/div/div[2]/gt-component-loader/gt-attendance-info/div/div/div[3]/gt-button[1]")
            sign_element.click()
            print(f"Clicking {sign_element.text}...")
            time.sleep(5)
            
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
            print("Clicking dropdown menu...")
            time.sleep(5)

            dropdown_items = WebDriverWait(shadow_root1, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".dropdown-body .dropdown-item"))
            )
            time.sleep(2)

            dropdown_items[work_place_location_id].click()
            print("Selecting work location...")

            gt_button = driver.find_element(By.XPATH, '/html/body/app/ng-component/div/div/div[2]/div/ghr-home/div[2]/div/gt-home-dashboard/gt-popup-modal/div/div/div[2]/gt-button')

            shadow_root = driver.execute_script('return arguments[0].shadowRoot', gt_button)

            button = shadow_root.find_element(By.CSS_SELECTOR, 'button.btn-primary')
            button_text =  button.text
            
            print("Button text:", button.text)
            button.click() 
            time.sleep(5)
            print("Done...")

            confirm_mail_send(button_text)
            
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


        


    
