import os
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

## Firefox profile that ignores (not CSS), images and flash since this browser is used for scraping only.
firefoxProfile = FirefoxProfile()
#firefoxProfile.set_preference('permissions.default.stylesheet', 2)
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

browser = webdriver.Firefox(firefoxProfile)
browser.get("https://my.queensu.ca/")

wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID, 'username')))

element = browser.find_element_by_id('username')
element.send_keys(os.environ['QUEENS_USERNAME'])
element = browser.find_element_by_id('password')
element.send_keys(os.environ['QUEENS_PASSWORD'])
element = browser.find_element_by_name('_eventId_proceed')
element.click()

browser.get("https://saself.ps.queensu.ca/psp/saself/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL")
