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

def find_class(semester, course):
    semester_dict = {'S':'None', 'F':'Term 1', 'W':'Term 2'}
    with requests.Session() as c:
        for idx, char in enumerate(course):
            if char.isdigit():
                break
        subject = (course[:idx])
        cournum = (course[idx:])
        # THIS DOESNT WORK WTF
        query_url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={}&course={}".format(subject, cournum)
        post = c.post(query_url)
        soup = BeautifulSoup(post.content, 'lxml')
        #print(returned_html)

        print(soup.prettify())
        #print("---------")

find_class('F', "BIOL234")
