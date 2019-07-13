import os
import time
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

# Login Stuff
browser.get("https://my.queensu.ca/")
wait = WebDriverWait(browser, 10)

element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
element.send_keys(os.environ['QUEENS_USERNAME'])
element = browser.find_element_by_id('password')
element.send_keys(os.environ['QUEENS_PASSWORD'])
element = browser.find_element_by_name('_eventId_proceed')
element.click()

# Goes to course catalog
browser.get("https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U")
wait = WebDriverWait(browser, 10)

# Fall
element = wait.until(EC.presence_of_element_located((By.ID, 'CLASS_SRCH_WRK2_STRM$35$')))
for option in element.find_elements_by_tag_name('option'):
    if option.text == '2019 Fall':
        option.click()
        break

time.sleep(5)

for i in range(1, 136):
    # Set subject type
    element = browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0')
    count = 0
    for option in element.find_elements_by_tag_name('option'):
        if count == i:
            option.click()

        count+=1

    # Set search options
    element = browser.find_element_by_id('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1')
    element.send_keys("c")
    element = browser.find_element_by_id('SSR_CLSRCH_WRK_ACAD_CAREER$2')
    for option in element.find_elements_by_tag_name('option'):
        if option.text == 'Undergraduate':
            option.click()
            break

    element = browser.find_element_by_id('SSR_CLSRCH_WRK_CAMPUS$3')
    element.send_keys("m")
    element = browser.find_element_by_id('SSR_CLSRCH_WRK_INSTRUCTION_MODE$4')
    element.send_keys("i")
    element = browser.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')
    element.click()

    time.sleep(5)

    # TODO: See if the submit click returns a "not found", continue for loop in that case
    if ("The search returns no results that match the criteria specified." in browser.page_source):
        print(i)
        continue
    else:
        element = browser.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH')
        element.click()
        time.sleep(5)


    #print(browser.page_source)
