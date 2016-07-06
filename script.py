import time
import sys
import getpass
from selenium import webdriver
import bs4
from tkinter import *

f=open(r"C:\Users\Suhas\Documents\hashpw.txt")
pw=f.read()

flist=['Aditya Kanthale','Ashish Singh','Sambhav Kothari','Mohit Bagri'] #add your friends names here
chrome_path=r"C:\Users\Suhas\Downloads\chromedriver.exe"
ppath=r"C:\Users\Suhas\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe"

def leftclick(event,obj):
		driver = webdriver.Chrome(chrome_path)
		driver.maximize_window()
		driver.get('http://www.facebook.com/login.php')
		username=driver.find_element_by_id('email')
		username.send_keys('suhas2go') #replace with your username
		passw=driver.find_element_by_id('pass')
		passw.send_keys(pw)
		passw.submit()
		chtbx=driver.find_element_by_class_name('_58al')
		chtbx.send_keys(obj)
		chtbx.submit()

root=Tk()

driver = webdriver.PhantomJS(ppath)
driver.maximize_window()
driver.get('http://www.facebook.com/login.php')
username=driver.find_element_by_id('email')
username.send_keys('suhas2go') #replace with your username
passw=driver.find_element_by_id('pass')
passw.send_keys(pw)
passw.submit()

time.sleep(15)

driver.save_screenshot('screen.png') 
onl=[]
html=driver.page_source
soup=bs4.BeautifulSoup(html,'html.parser')
frds=soup.findAll("li",attrs={'class':'_42fz'})
for frd in frds:
	if not frd.findAll('i'):
		#all who are online NOT  
		for f in frd.findAll('div',attrs={'class':'_55lr'}):
			if f.string in flist:
				print (f.string)
				onl.append(f.string)

if not onl:
	l=Label(root,text='none is online on fb')
	l.pack()
else:
	ctr=0
	butts=[]
	for onlfrd in onl:
		butts.append(Button(root,text=onlfrd))
	for b in butts:
		b.pack()
		b.bind('<Button-1>',lambda event, obj=b.config('text')[-1]: leftclick(event, obj))
	

root.mainloop()