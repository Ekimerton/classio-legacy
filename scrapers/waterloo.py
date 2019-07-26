import requests
import os
from bs4 import BeautifulSoup

class Course():
    def __init__(self, nme, sem, constant_t, variable_t):
        self.name = nme
        self.semester = sem
        self.constant_times = constant_t
        self.variable_times = variable_t
    def __str__(self):
        return self.name + " " + self.semester + "\n" + str(self.constant_times) + "\n" + str(self.variable_times)

def format_time(time_string):
    #do this bruh
    pass

def find_class(semester, course):
    semester_dict = {'S':'1195', 'F':'1199', 'W':'1201'}
    with requests.Session() as c:
        for idx, char in enumerate(course):
            if char.isdigit():
                break
        subject = (course[:idx])
        cournum = (course[idx:])
        query_url = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"
        sess = semester_dict[semester]
        query_data = dict(level="under", sess=sess, subject=subject, cournum=cournum)

        post = c.post(query_url, data=query_data)
        print("Connection made")
        soup = BeautifulSoup(post.content, 'xml')
        #print(returned_html)

        #print(soup.prettify())
        #print("---------")

        find_error = str(soup.find('B'))
        if find_error == '<B>Sorry, but your query had no matches.</B>':
            return None

        tables = soup.find_all('TABLE')
        table = tables[1]
        #print(table.prettify())
        rows = table.find_all('TR')
        times = []
        for row in rows:
            cols = row.find_all('TD')
            try:
                section_type = cols[1].get_text()[:3]
                if section_type == "":
                    continue
                section_time_str = cols[10].get_text()[:11]
                #print("------------------")
                #print(section_type, section_time_str)

                # Add read for days and fix time format
                #for char in cols[10].get_text():
                #    if char

                section_exists = False
                for time_section in times:
                    if section_type == time_section[0]:
                        time_section.append(section_time_str)
                        section_exists = True
                        break
                if not section_exists:
                    time_section = [section_type, section_time_str]
                    times.append(time_section)
            except:
                pass
        constant_times = []
        variable_times = []
        for time_section in times:
            if len(time_section) == 2:
                constant_times.append(time_section)
            else:
                variable_times.append(time_section)
        print(constant_times)
        print(variable_times)


find_class("F", "CS135")
