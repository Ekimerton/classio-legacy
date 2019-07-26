import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# TODO: FIX (FOR THE NEXT READ) THAT THE FINAL 0 IS CUT FROM SECTION TYPE
#Setup

    # Helper Methods
def hour12to24(timestamp):
    ep_index = timestamp.index(":")
    hour = int(timestamp[:ep_index])
    minute = timestamp[ep_index + 1:ep_index + 3]
    am_pm = timestamp[ep_index + 3:ep_index + 5]
    if hour == 12:
        hour = 0
    if am_pm == "PM":
        hour = str(hour + 12)
    if am_pm == "AM" and hour < 10:
        hour = "0" + str(hour)
    return str(hour) + minute

def standardizeTime(init_time):
    stnd_time = ""
    bits = init_time.split(", ")
    for bit in bits:
        day_string = bit[:2]
        day_list = []
        while day_string in ['Mo', 'Tu', 'We', 'Th', 'Fr']:
             day_list.append(day_string)
             bit = bit[2:]
             day_string = bit[:2]

        first_hour = bit[:bit.index('-')]
        last_hour = bit[bit.index('-') + 1:]
        for day in day_list:
            stnd_time = stnd_time + day + hour12to24(first_hour) + hour12to24(last_hour) + ","

    if not stnd_time:
        return None
    return stnd_time[:len(stnd_time)-1]

    # SQL/SQLite model classes
Base = declarative_base()
class Course(Base):
    __tablename__ = "queens_course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    semester = Column('semester', String)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)

    # SQLAlchemy creation
engine = create_engine('sqlite:///queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# start index
start = int(input("Enter the last number that was parsed: "))
semester = input("Fall or Winter? (2019/2020): ")

if not semester in ['Fall', 'Winter']:
    print("Please enter 'Fall' or 'Winter'")
    exit()

    # Firefox profile that ignores (not CSS), images and flash since this browser is used for scraping only.
firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
browser = webdriver.Firefox(firefoxProfile)

# Selenium Driver run

    # Login Stuff
browser.get("https://my.queensu.ca/")
wait = WebDriverWait(browser, 30)

element = wait.until(EC.presence_of_element_located((By.ID, 'username')))
element.send_keys(os.environ['QUEENS_USERNAME'])
element = browser.find_element_by_id('password')
element.send_keys(os.environ['QUEENS_PASSWORD'])
element = browser.find_element_by_name('_eventId_proceed')
element.click()

    # Goes to course search
for i in range(start, 143): #Replace this 136 with a dynamic range (136 for fall, 143 for winter)

    browser.get("https://saself.ps.queensu.ca/psc/saself/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U")
    wait = WebDriverWait(browser, 30)

    # semester Selection
    element = wait.until(EC.presence_of_element_located((By.ID, 'CLASS_SRCH_WRK2_STRM$35$')))
    option = element.find_elements_by_tag_name('option')
    if option != '2019 ' + semester:
        for option in element.find_elements_by_tag_name('option'):
            if option.text == '2019 ' + semester:
                option.click()
                break

        time.sleep(5)

    # Set subject type
    element = browser.find_element_by_id('SSR_CLSRCH_WRK_SUBJECT_SRCH$0')
    count = 0
    for option in element.find_elements_by_tag_name('option'):
        if count == i:
            option.click()
            print(option.text + ": " + str(i))

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

    try:
        wait = WebDriverWait(browser, 15)
        wait.until(EC.presence_of_element_located((By.ID, 'CLASS_SRCH_WRK2_SSR_PB_MODIFY$5$')))
        print("    read successfully")
    except:
        if ("The search returns no results that match the criteria specified." in browser.page_source):
            print("    returned no results")
            continue
        else:
            print("    Unknown error, query returned neither a proper page nor a 'not found'")

    for classDiv in browser.find_elements_by_xpath("//div[starts-with(@id,'win0divSSR_CLSRSLT_WRK_GROUPBOX2$')]"):
        title = classDiv.find_element_by_tag_name('a').get_attribute('title')
        title = "".join(title[17:title.index(" -")].split())
        sections = classDiv.find_elements_by_xpath(".//tr[starts-with(@id,'trSSR_CLSRCH_MTG1$')]")
        sectionID_tag = "xxx"
        times = ""
        try:
            for section in sections:
                old_sectionID_tag = sectionID_tag
                sectionID = section.find_element_by_xpath(".//a[starts-with(@id,'MTG_CLASSNAME$')]").get_attribute("innerHTML")
                sectionID = sectionID[0:sectionID.index('<')]
                sectionID_tag = sectionID[(sectionID.index('-') + 1):]
                if sectionID_tag != old_sectionID_tag:
                    times = times[:len(times) - 2]
                    times += "-" + sectionID_tag + ":"
                timeslot = section.find_element_by_xpath(".//span[starts-with(@id,'MTG_DAYTIME$')]").text
                timeslot = ", ".join(timeslot.splitlines())
                timeslot = standardizeTime(timeslot)
                times += timeslot + ";" #PROBLEM IS AROUND HERE

            times = times[1:len(times) - 1] #Removes trailing '-' and leading ';'

# ding to database
            constant_t = ""
            variable_t = ""
            for sectionType in times.split('-'):
                if ";" in sectionType:
                    variable_t += sectionType + "-"
                else:
                    constant_t += sectionType + "-"
            if constant_t:
                constant_t = constant_t[:len(constant_t) - 2]
            if variable_t:
                variable_t = variable_t[:len(variable_t) - 2]

            exists = False
            try:
                q = session.query(Course).filter(Course.name == title, Course.semester == semester[0]).first()
                if q.name == title and q.semester == semester[0]:
                    exists = True
                    print("       ", title, "already exists in the db")
            except:
                pass
            if not exists:
                course = Course()
                course.name = title
                course.constant_times = constant_t
                course.variable_times = variable_t
                course.semester = semester[0]
                session.add(course)
                try:
                    session.commit()
                except:
                    session.rollback()
                    raise
                finally:
                    session.close()
        except Exception as e:
            print("        failed reading section: ", title)
            print(e)
    continue

session.close()
