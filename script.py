import time
# import getpass
from selenium import webdriver
import bs4
from tkinter import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

f = open(r"C:\Users\Suhas\Documents\hashpw.txt")
pw = f.read()

flist = ['Aditya Kanthale', 'Ashish Singh','Sambhav Kothari','Mohit Bagri']  # add your friends names here
chrome_path = r"C:\Users\Suhas\Downloads\chromedriver.exe"
ppath = r"C:\Users\Suhas\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe"


def leftclick(event, obj):
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)
	driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
	driver.maximize_window()
	driver.get('http://www.facebook.com/login.php')
	username = driver.find_element_by_id('email')
	username.send_keys('suhas2go')  # replace with your username
	passw = driver.find_element_by_id('pass')
	passw.send_keys(pw)
	passw.submit()
	chtbx = driver.find_element_by_class_name('_58al')
	chtbx.send_keys(obj)
	time.sleep(10)
	chtbx.send_Keys(Keys.RETURN);


root = Tk()
root.title("Frilert")

driver = webdriver.PhantomJS(ppath,service_args=['--load-images=no'])
driver.maximize_window()
driver.get('http://www.facebook.com/login.php')
username = driver.find_element_by_id('email')
username.send_keys('suhas2go')  # replace with your username
passw = driver.find_element_by_id('pass')
passw.send_keys(pw)
passw.submit()

delay=20
#time.sleep(delay)
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'js_1g')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")


#driver.save_screenshot('screen.png')
onl = []
html = driver.page_source
soup = bs4.BeautifulSoup(html, 'html.parser')
frds = soup.findAll("li", attrs={'class': '_42fz'})
for frd in frds:
	if frd.findAll('i'):
		# all who are online
		for f in frd.findAll('div', attrs={'class': '_55lr'}):
			print(f.string.encode('utf-8'))
			onl.append(f.string)
print (len(onl))
if not onl:
	l = Label(root, text='none is online on fb')
	l.pack()
else:
	butts = []
	for onlfrd in onl:
		butts.append(Button(root, text=onlfrd))
	for b in butts:
		b.pack()
		b.bind('<Button-1>', lambda event, obj=b.config('text')[-1]: leftclick(event, obj))

root.mainloop()
