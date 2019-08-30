import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# Firefox profile that ignores (not CSS), images and flash since this browser is used for scraping only.
firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference(
    'dom.ipc.plugins.enabled.libflashplayer.so', 'false')
browser = webdriver.Firefox(firefoxProfile)

# Start
browser.get(
    "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=sectsearch")
