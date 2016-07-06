import time
import sys
import getpass
from selenium import webdriver
import bs4

flist=['Aditya Kanthale','Ashish Singh','Rajan Garg','Mukesh Babu'] #add your friends names here


ppath=r"C:\Users\Suhas\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe"
pw=getpass.getpass() # can be replaced with stored password 

driver = webdriver.PhantomJS(ppath)
driver.maximize_window()
driver.get('http://www.facebook.com/login.php')
username=driver.find_element_by_id('email')
username.send_keys('username') #replace with your username
passw=driver.find_element_by_id('pass')
passw.send_keys(pw)
passw.submit()

time.sleep(15) #set according to your internet speed

#driver.save_screenshot('screen.png') 

html=driver.page_source
soup=bs4.BeautifulSoup(html,'html.parser')
frds=soup.findAll("li",attrs={'class':'_42fz'})
for frd in frds:
	if frd.findAll('i'):
		#all who are online 
		for f in frd.findAll('div',attrs={'class':'_55lr'}):
			if f.string in flist:
				print(f.string+' is online')

