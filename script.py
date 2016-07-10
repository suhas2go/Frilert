import os
import sys

from win32api import *

import struct

import win32con
import win32gui_struct
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
from multiprocessing import Process

f = open(r"C:\Users\Suhas\Documents\hashpw.txt")
pw = f.read()

flist = ['Aditya Kanthale', 'Ashish Singh','Sambhav Kothari','Mohit Bagri']  # add your friends names here
chrome_path = r"C:\Users\Suhas\Downloads\chromedriver.exe"
ppath = r"C:\Users\Suhas\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe"

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

class SysTrayIcon(object):
    '''TODO'''
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    
    FIRST_ID = 1023
   
    def __init__(self,
                 icon,
                 hover_text,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):
        
        self.runevery=600 #10minutes
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit
          
        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"
        
        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER+20 : self.notify,}
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(window_class)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)

        self.ctr=0
        driver = webdriver.PhantomJS(ppath,service_args=['--load-images=no'])
        driver.maximize_window()
        driver.get('http://www.facebook.com/login.php')
        username = driver.find_element_by_id('email')
        username.send_keys('suhas2go')  # replace with your username
        passw = driver.find_element_by_id('pass')
        passw.send_keys(pw)
        passw.submit()
        self.refresh_icon()
        
        def corejob():
            if self.ctr==1:
                driver.get('http://www.facebook.com')

            delay=10
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
                        onl.append(f.string)

            #menu_options = ('Say Hello','Switch Icon')
            menu_options=tuple(onl)
            menu_options = menu_options + ('Quit',)
            self._next_action_id = self.FIRST_ID
            self.menu_actions_by_id = set()
            self.menu_options = self._add_ids_to_menu_options(list(menu_options))
            self.menu_actions_by_id = dict(self.menu_actions_by_id)
            del self._next_action_id

            title='psst..go online?'
            msg=''
            for mo in list(menu_options):
                if msg=='':
                    msg=mo
                else:
                    if mo!='Quit' and mo is not None:
                        msg=msg+','+mo

            '''icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                           self.icon,
                                           win32con.IMAGE_ICON,
                                           0,
                                           0,
                                           icon_flags)
            '''
            if(self.ctr==1):
                win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                             (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                              self.hicon, "Balloon  tooltip",msg,200,title))
            else:
                self.btip(title,msg)
            
            self.notify_id = None
            #self.refresh_icon()
            self.lastrun=time.time();
            print(self.lastrun)
        corejob() 
        self.ctr=1
        while(1):
            while(time.time()-self.lastrun<self.runevery):
                win32gui.PumpWaitingMessages()
            corejob()
              

    def btip(self,title,msg):
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, "Frilert")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                             (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                              self.hicon, "Balloon  tooltip",msg,200,title))

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text= menu_option
            self.menu_actions_by_id.add((self._next_action_id, option_text))
            result.append((menu_option,) + (self._next_action_id,))
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            self.hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            print ("Can't find icon file - using default.")
            self.hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        '''if self.notify_id: message = win32gui.NIM_MODIFY
        else: message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)'''
    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # Terminate the app.

    def notify(self, hwnd, msg, wparam, lparam):
        
        if lparam==win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam==win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam==win32con.WM_LBUTTONUP:
            pass
        return True
        
    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        #win32gui.SetMenuDefaultItem(menu, 1000, 0)
        
        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
    
    def create_menu(self, menu, menu_options):
        for option_text, option_id in menu_options[::-1]:
            if option_id in self.menu_actions_by_id:                
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_text)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)
    

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)
        
    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]    
        if menu_action == 'Quit':
            win32gui.DestroyWindow(self.hwnd)
        else:
            leftClick(self,menu_action)
            
def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        print('well')
        #return not isinstance(obj, basestring)


if __name__ == '__main__':
    import itertools, glob
    favicon = itertools.cycle(glob.glob(r"C:\Users\Suhas\Documents\Frilert\systry\favicon.ico"))
    hover_text = "Frilert"
    def leftClick(sysTrayIcon,menu_action):
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
        chtbx.send_keys(menu_action)
        time.sleep(5)
        chtbx.send_keys(Keys.Return);
    
    def bye(sysTrayIcon): print ('Bye, then.')
    
    SysTrayIcon(next(favicon), hover_text, on_quit=bye, default_menu_index=1)