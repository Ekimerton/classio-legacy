import requests
import os
from bs4 import BeautifulSoup
import lxml

class Course():
    def __init__(self, nme, sem, constant_t, variable_t):
        self.name = nme
        self.semester = sem
        self.constant_times = constant_t
        self.variable_times = variable_t
    def __str__(self):
        return self.name + " " + self.semester + "\n" + str(self.constant_times) + "\n" + str(self.variable_times)

def mergeCopies(times_list):
    new_list = []
    for i in range(0, len(times_list)):
        for j in range(i, len(times_list)):
            if times_list[i][0] == times_list[j][0] and i != j:
                name = times_list[i][0]
                old_times_list = times_list[j]
                del old_times_list[0]
                del times_list[i][0]
                times_list[i] = times_list[i] + old_times_list
                b_set = set(tuple(x) for x in times_list[i])
                times_list[i] = [list(x) for x in b_set]
                times_list[i].insert(0, name)
                del times_list[j]

def format_hour(hour_string):
    hour = int(hour_string[:2])
    if hour < 7:
        return str(hour+12) + hour_string[2:]
    else:
        return hour_string

def format_time(time_string):
    times = []
    hour = time_string[:11]
    day = ""
    #print(time_string[11:])
    for c in time_string[11:]:
        if c.isalpha:
            day += c
    hour = hour.replace(":", "")
    start, end = hour.split("-")
    hour = format_hour(start) + format_hour(end)
    for idx, c in enumerate(day):
        if c == 'M':
            times.append("Mo" + hour)
        if c == 'W':
            times.append("We" + hour)
        if c == "F":
            times.append("Fr" + hour)
        if c == "T":
            try:
                if day[idx + 1] == 'h':
                    times.append("Th" + hour)
                else:
                    times.append("Tu" + hour)
            except:
                times.append("Tu" + hour)

    return times


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
        soup = BeautifulSoup(post.content, 'lxml')
        #print(returned_html)

        #print(soup.prettify())
        #print("---------")

        find_error = str(soup.find('b'))
        if find_error == '<b>Sorry, but your query had no matches.</b>':
            return None

        tables = soup.find_all('table')
        table = tables[1]
        #print(table.prettify())
        rows = table.find_all('tr')
        times = []
        for row in rows:
            cols = row.find_all('td')
            try:
                section_type = cols[1].get_text()[:3]
                if section_type == "" or section_type == "&nb" or section_type == "TST":
                    continue
                class_num = cols[0].get_text().replace(" ", "")
                sec_time_str = format_time(cols[10].get_text())
                section_time_str = []
                section_time_str.append(class_num)
                section_time_str += sec_time_str
                section_exists = False
                for time_section in times:
                    if section_type == time_section[0]:
                        section_exists = True
                        if not section_time_str in time_section:
                            time_section.append(section_time_str)
                            continue
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
        return Course(course, semester, constant_times, variable_times)
