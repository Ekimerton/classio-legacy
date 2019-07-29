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
    semester_dict = {'S':'1195', 'F':'1199', 'W':'1201'}
