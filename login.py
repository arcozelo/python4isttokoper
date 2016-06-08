#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

#PROXY = ""
#acapabilities = {'chrome.binary': '/home/opertok/python/', 'proxy' : {
    #"httpProxy":None,
    #"ftpProxy":None,
    #"sslProxy":None,
    #"noProxy":"127.0.0.1",
    #"proxyType":"DIRECT",
    #"class":"org.openqa.selenium.Proxy",
    #"autodetect":False}
    #}

#driver = webdriver.Remote('http://127.0.0.1:9515', acapabilities, proxy=setproxy)
driver=webdriver.Firefox()
driver.get("http://baco.ipfn.ist.utl.pt/isttok/physics_summary.php")
assert "Summary" in driver.title
driver.find_element_by_link_text('Login').click()
#driver.click(login_link)

try:
    element = WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.TAG_NAME, "h3"))
    )
finally:
	cookie=driver.get_cookie('cookie_isttok_info')
	#print(cookie)
	f=open('cookie','w')
	f.write(json.dumps(cookie))
	driver.quit()

#print(driver.session_id)
#print(driver.command_executor._url)


