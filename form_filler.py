#!/usr/bin/python
from sdas.core.LoadSdasData import LoadSdasData
from sdas.core.StartSdas import StartSdas
import numpy
import sys
from pyISTTOK.special_mean_val import special_mean_val
from pyISTTOK.exposure_time import exposure_time
from pyISTTOK.period_counter import period_counter
import xmlrpclib

#from pymouse import PyMouse
#from pykeyboard import PyKeyboard
import time

#####################################################################
##                  GLOBAL VARIABLES                               ##
#####################################################################
iplasma_threshold=2.5e3
dens_threshold=1.e18
marte_threshold=100
iplasma_ok=0
dens_ok=0
marte_ok=0
timeout=0
s=""
fluffytron = {
        0: "|",
        1: "/",
        2: "-",
        3: "\\",
    }

#####################################################################

#####################################################################
##                  SDAS ACCESS                                    ##
#####################################################################

client = StartSdas()

if len(sys.argv) < 2 :
    shotnr = client.searchMaxEventNumber('0x0000')
else :
    shotnr = int(sys.argv[-1])

plasma_curr_channelID='POST.PROCESSED.IPLASMA'; # Unique Identifier for plasma current
plasma_dens_channelID='POST.PROCESSED.DENSITY'; # Unique Identifier for plasma density
marte_power_channelID='MARTE_NODE_IVO3.DataCollection.Channel_105'; #Marte channel for the power supply

print '\nLoading data, CTRL-C to interrupt'
print 'I_thr ',iplasma_threshold,' n_thr ', dens_threshold
print '\nSHOT #'+str(shotnr)+'\n'
while (True):
	if iplasma_ok==0:
		try:
			[iplasma,iplasma_times] = LoadSdasData(client, plasma_curr_channelID, shotnr);
			iplasma_ok=numpy.all(numpy.isfinite(iplasma))
		except:
			iplasma_ok=0
	if dens_ok==0:
		try:
			[dens,dens_times] =       LoadSdasData(client, plasma_dens_channelID, shotnr);
			dens_ok=numpy.all(numpy.isfinite(dens))  # check if all finite
		except xmlrpclib.Fault:
			dens_ok=0
	if marte_ok==0:
		try:
			[marte,marte_times] =       LoadSdasData(client, marte_power_channelID, shotnr);
			marte_ok=numpy.all(numpy.isfinite(marte))  # check if all finite
		except xmlrpclib.Fault:
			marte_ok=0
	if dens_ok and iplasma_ok and marte_ok :
		print '\nData loaded\n'
		break
	try:
		print fluffytron.get(timeout % 4,"0")+' '+'{0:02d}'.format(timeout)+'s',
		print ' Iplasma:',
		if iplasma_ok : print ' OK',
		else : print 'NOK',
		print ' Dens:',
		if dens_ok : print ' OK',
		else : print 'NOK',
		print ' marteAQ:',
		if marte_ok : print ' OK',
		else : print 'NOK',
		print '  \r',
		sys.stdout.flush()	
		time.sleep(1)
		timeout += 1
	except KeyboardInterrupt:
		break



if iplasma_ok:
    print 'FROM IPLASMA   ( thresh',iplasma_threshold,')'
    iplasma_shot_time = exposure_time(numpy.abs(iplasma),iplasma_times,iplasma_threshold)
    iplasma_mean_val = special_mean_val(numpy.abs(iplasma),iplasma_threshold)/1.e3
    print 'Mean current {0:.3f} kA'.format(iplasma_mean_val)
    iplasma_periods, s = period_counter(numpy.abs(iplasma),iplasma_threshold)
    print 'I counted '+str(iplasma_periods)+' periods'
else:
    print 'NO IPLASMA DATA'

print ''

if dens_ok:
    print 'FROM DENSITY   ( thresh',dens_threshold,')'
    dens_shot_time = exposure_time(dens,dens_times,dens_threshold)
    dens_mean_val = special_mean_val(dens,dens_threshold)/1e18;
    print 'Mean density {0:.2e} m'.format(dens_mean_val*1e18)+u'\u207b\u00b3'
    dens_periods , s= period_counter(dens,dens_threshold)
    print 'I counted '+str(dens_periods)+' periods'
else:
    print 'NO DENSITY DATA'

print ''

if marte_ok:
    print 'FROM MARTE'
    marte_periods,cycle_mask = period_counter(abs(marte),marte_threshold,numpy.append(numpy.ones(10),numpy.zeros(1)))
    print 'I counted '+str(marte_periods)+' periods'
    print str(marte_periods*25)+' ms'
else:
    print 'NO MARTE DATA'

if marte_ok and iplasma_ok and dens_ok:
    print '\nSucess rate was '+str(iplasma_periods)+'/'+str(marte_periods)
    # print cycle_mask
    #~ if iplasma_periods==marte_periods:
        #~ print '!!!CONGRATULATIONS!!!'
    #~ elif iplasma_periods <= marte_periods/2:
        #~ print '!!!BOOOOOO!!!'

print '\n'

s=raw_input("ENTER : auto_filler / NONEMPTY STRING + ENTER : abort ...")

#####################################################################
##                  AUTO FILLER                                    ##
#####################################################################

if s !='' : sys.exit()

#m = PyMouse()
#k = PyKeyboard()

timer_max = 50;

prev_posi = (0,0);
oldr_posi = (0,0);
mouse_ready = False;

#for i in range(timer_max):
    #curr_posi = m.position()
    #print 'Mouse at '+str(curr_posi)+'(timeout in '+str(i+1)+'/'+str(timer_max)+')     \r',
    #sys.stdout.flush()
    #if curr_posi == prev_posi == oldr_posi:
        #mouse_ready = True;
        #break
    #else:
        #oldr_posi = prev_posi;
        #prev_posi = curr_posi;
    #time.sleep(0.5)

#if mouse_ready:
    #print "\nI'm going to click at"+str(curr_posi)
    #m.click(m.position()[0],m.position()[1])
    #time.sleep(0.5)

    ## Shot number
    ## k.type_string(str(shotnr)) # this should be auto-written normally
    ## k.tap_key(k.tab_key)
    ##Iplasma in kA
    #if iplasma_ok :
		#k.type_string('{0:.2f}'.format(iplasma_mean_val))
    #k.tap_key(k.tab_key)
    ##density in *1e18m-3
    #if dens_ok :
		#k.type_string('{0:.2f}'.format(dens_mean_val))
    #k.tap_key(k.tab_key)
    ##duration in ms
    #if iplasma_ok :
		#k.type_string(str(int((iplasma_shot_time//25)*25)))
    #k.tap_key(k.tab_key)

    #Shot comments
    #k.type_string('Sn-spectra, ')
    #k.type_string('Sn cold at a=XXXX cm. ')
    #k.type_string('HIB open')
    #k.type_string('spectrscpy Sn a=7.5cm P(ed) 0.18ubar ')
    #tmp_str = str(iplasma_periods)+' in '+str(marte_periods)+' cycles'
    #k.type_string(tmp_str)
    #k.tap_key(k.tab_key)
    #k.tap_key(k.enter)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

#driver = webdriver.Chrome()
capabilities = {'chrome.binary': '/home/halves/bin'}
#driver = webdriver.Remote('http://127.0.0.1:9515', capabilities)

f=open('cookie','r')
#driver = webdriver.Remote(command_executor='http://127.0.0.1:9515', desired_capabilities=capabilities)
driver=webdriver.Firefox()
#driver.close()
cookie=json.loads(f.read())

#driver.command_executor._url='http://127.0.0.1:36660/hub'
driver.get("http://baco.ipfn.ist.utl.pt/isttok/physics_summary.php")
driver.add_cookie(cookie)
driver.get("http://baco.ipfn.ist.utl.pt/isttok/physics_summary.php")
assert "Summary" in driver.title
#login_link = driver.find_element_by_link_text('Login')
#WebElement.click(login_link)

#s=raw_input(driver.session_id)
#s=raw_input(driver.command_executor._url)
driver.find_element_by_link_text('Manage session').click()
assert "Shot" in driver.title
chars=str(shotnr)
driver.find_element_by_name('shotn').clear()
driver.find_element_by_name('shotn').send_keys(chars)
if iplasma_ok :
	chars=str('{0:.2f}'.format(iplasma_mean_val))
	driver.find_element_by_name('ip').send_keys(chars)
if dens_ok :
	chars=str('{0:.2f}'.format(dens_mean_val))
	driver.find_element_by_name('dens').send_keys(chars)
if iplasma_ok :
	#chars=str(int(((iplasma_shot_time+25//2)//25)*25))
	chars=str(int(iplasma_shot_time))
	driver.find_element_by_name('duration').send_keys(chars) #res
elif dens_ok :
	chars=str(int(dens_shot_time))
	driver.find_element_by_name('duration').send_keys(chars)
driver.find_element_by_name('comment').send_keys("reference shot #39870 : Ih feedback on Eprobes ; rake@75mm, 2D@75mm , EB 120V - 300us ON 700us OFF @70mm")
# conditioning; testing EB polarization with different functions in pos and neg cycles / 
# repeat 39986; EB(ON),@r=70mm,V=+120V,1.5-3.5ms & 21.5-24ms; HIBD(ON),fmod=150kHz / 
# , rake probe&2Dprobe@ a=65mm electrode off@70mm I_h on PID20;10;5

driver.find_element_by_name("add").click()
try:
    element = WebDriverWait(driver, 600).until(
        #EC.text_to_be_present_in_element_value((By.TAG_NAME, "h2"),"Shot added OK")
        #EC.driver.find_element_by_css_selector('h2:contains("added")')
        #EC.presence_of_element_located((By.CSS_SELECTOR,'a:contains("added")'))
        #EC.presence_of_element_located((By.XPATH,"/html/body/div[@id='holder']/table[@id='bigtable']/tbody/tr/td[@id='main']/h2[1]"))
        EC.presence_of_element_located((By.XPATH,"//table/tbody/tr/td/h2[1]"))
    )
except KeyboardInterrupt:
	#driver.quit()
	pass
	print("aborted")
#except:
	#pass
finally:
	#time.sleep(1)
	driver.quit()
	print("ok")






#try:
    #while True:
        ## This will fail when the browser is closed.
        #driver.execute_script("")
        #time.sleep(1)
## Setting such a wide exception handler is generally not advisable but
## I'm not convinced there is a definite set of exceptions that
## Selenium will stick to if it cannot contact the browser. And I'm not
## convinced the set cannot change from release to release.
#except:
    #has_quit = False
    #while not has_quit:
        #try:
            ## This is to allow Selenium to run cleanup code.
            #driver.quit()
            #has_quit = True
        #except:  # See comment above regarding such wide handlers...
            #pass



#try:
    #WebDriverWait(driver, 600).until(EC.invisibility_of_element_located((By.NAME, 'Add')))
	#WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//*[@name="ip" and @text == ""]')))
#finally:
	#driver.quit() 
#send_keys_to_element(ip_text,"123")
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
