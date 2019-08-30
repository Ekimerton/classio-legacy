import requests
import os
import json


class Course():
    def __init__(self, nme, sem, constant_t, variable_t):
        self.name = nme
        self.semester = sem
        self.constant_times = constant_t
        self.variable_times = variable_t

    def __str__(self):
        return self.name + " " + self.semester + "\n" + str(self.constant_times) + "\n" + str(self.variable_times)


def format_hour(hour_string):
    while len(hour_string) < 4:
        hour_string = "0" + hour_string
    return hour_string


def find_class(semester, course):
    semester_dict = {'S': 'None', 'F': '1', 'W': '2'}
    with requests.Session() as c:
        for idx, char in enumerate(course):
            if char.isdigit():
                break
        subject = (course[:idx])
        cournum = (course[idx:])
        query_url = "https://ubc-courses-api.herokuapp.com/tree/2019W/{}/{}/".format(
            subject, cournum)
        post = c.get(query_url)
        response = post.json()
        last_section = ""
        times = []
        activity_times = []
        for section_num in response['sections']:
            term = response['sections'][section_num]['term']
            if term != semester_dict[semester]:
                continue
            activity = response['sections'][section_num]['activity'][:3].upper(
            )
            if activity == "WAI":
                continue

            start_time = format_hour(response['sections'][section_num]['start'].replace(
                ':', ''))
            end_time = format_hour(response['sections'][section_num]['end'].replace(
                ':', ''))
            days = response['sections'][section_num]['days'][1:]
            section_times = []
            section_times.append(section_num)
            for day in days.split(" "):
                section_times.append(day[:2] + start_time + end_time)
            if last_section == activity:
                activity_times.append(section_times)
            else:
                times.append(activity_times)
                activity_times = []
                activity_times.append(activity)
                activity_times.append(section_times)
            last_section = activity
        times.append(activity_times)

        constant_t = []
        variable_t = []
        for time in times:
            if len(time) < 2:
                continue
            elif len(time) == 2:
                constant_t.append(time)
            elif len(time) > 2:
                variable_t.append(time)
    return Course(course, semester, constant_t, variable_t)


find_class('F', "BIOL234")
