from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

f = open(r"C:\Users\Suhas\Documents\hashpw.txt",mode='r') 
chrome_path = r"driver\chromedriver.exe"

nm='suhas2go' #replace with your username
pw = f.read() #replace with your password

useProxy=True #disable if not using a proxy
PROXY="202.141.80.22:3128" #hostname:port format

def leftClick(sysTrayIcon,menu_action):
    chrome_options = webdriver.ChromeOptions()
    
    if useProxy==True:
        chrome_options.add_argument('--proxy-server=%s' % PROXY)

    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('http://www.facebook.com/login.php')
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    username.send_keys(nm)  # replace with your username
    passw = driver.find_element_by_id('pass')
    passw.send_keys(pw)
    passw.submit()
    chtbx = driver.find_element_by_class_name('_58al')
    chtbx.send_keys(menu_action)
    time.sleep(5)
    chtbx.send_keys(Keys.RETURN)

def bye(sysTrayIcon): print ('Bye, then.')