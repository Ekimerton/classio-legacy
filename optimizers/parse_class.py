from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker
import scrapers.waterloo as waterloo
import scrapers.ubc as ubc

Base = declarative_base()


class CourseDB(Base):
    __tablename__ = "course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    semester = Column('semester', String)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)


class Course():
    def __init__(self, nme, sem, constant_t, variable_t):
        self.name = nme
        self.semester = sem
        self.constant_times = constant_t
        self.variable_times = variable_t

    def __str__(self):
        return self.name + " " + self.semester + "\n" + str(self.constant_times) + "\n" + str(self.variable_times)

# Merges two same-id sections, two TUTs for example


def mergeCopies(times_list):
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

# Change this to work with class number!


def parseClass(course):
    constant_t = []
    variable_t = []
    if course.constant_times:
        for type in course.constant_times.split('-'):
            class_list = []
            section_name = type[:type.index(':')]
            type = type[type.index(':') + 1:]
            for choice in type.split(';'):
                class_num = choice[:choice.index('?')]
                choice = choice[choice.index('?') + 1:]
                date_list = []
                date_list.append(class_num)
                for date in choice.split(','):
                    date_list.append(date)
                date_list = list(dict.fromkeys(date_list))
                class_list.append(date_list)
            b_set = set(tuple(x) for x in class_list)
            class_list = [list(x) for x in b_set]
            class_list.insert(0, section_name)
            constant_t.append(class_list)
    mergeCopies(constant_t)
    if course.variable_times:
        for type in course.variable_times.split('-'):
            class_list = []
            section_name = type[:type.index(':')]
            type = type[type.index(':') + 1:]
            for choice in type.split(';'):
                class_num = choice[:choice.index('?')]
                choice = choice[choice.index('?') + 1:]
                date_list = []
                date_list.append(class_num)
                for date in choice.split(','):
                    date_list.append(date)
                date_list = list(dict.fromkeys(date_list))
                class_list.append(date_list)
            b_set = set(tuple(x) for x in class_list)
            class_list = [list(x) for x in b_set]
            class_list.insert(0, section_name)
            variable_t.append(class_list)
    mergeCopies(variable_t)
    return Course(course.name, course.semester, constant_t, variable_t)


def searchClass(name, semester, school):
    if school in ['queens']:
        engine = create_engine('sqlite:///scrapers/{}.db'.format(school))
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        class_list = []
        try:
            courses = session.query(CourseDB).filter_by(
                name=name, semester=semester).first()
            class_list.append(parseClass(courses))
        except Exception as e:
            pass
        try:
            courses = session.query(CourseDB).filter_by(
                name=name+'A', semester=semester).first()
            class_list.append(parseClass(courses))
        except Exception as e:  # except Exception as eion as e:
            pass
        try:
            courses = session.query(CourseDB).filter_by(
                name=name+'B', semester=semester).first()
            class_list.append(parseClass(courses))
        except Exception as e:
            pass
        session.close()
        for cls in class_list:
            cls.variable_times = mergeClasses(cls.variable_times)
        return class_list
    elif school == "waterloo":
        class_list = []
        try:
            result = waterloo.find_class(semester, name)
            if result:
                class_list.append(result)
        except Exception as e:
            pass
        for cls in class_list:
            cls.variable_times = mergeClasses(cls.variable_times)
        return class_list
    elif school == "ubc":
        class_list = []
        try:
            result = ubc.find_class(semester, name)
            if result:
                class_list.append(result)
        except Exception as e:
            pass
        for cls in class_list:
            cls.variable_times = mergeClasses(cls.variable_times)
        return class_list

# Function that gets rid of duplicate class times, merges the class numbers


def mergeClasses(classes):
    new_list = []
    for section in classes:
        new_section = []
        new_section.append(section[0])
        for class1 in section[1:]:
            found_in_new = False
            for class2 in new_section[1:]:
                if class1[1:] == class2[1:]:
                    class2[0] += ", " + class1[0]
                    found_in_new = True
                    break
            if not found_in_new:
                new_section.append(class1)
        new_list.append(new_section)
    return new_list
# This is a patchy get-it-done deal. Not eff at all, will work on it tomorrow.


def narrow_result(cls, params):
    if not params:
        return cls
    narrow_constant_times = []
    narrow_variable_times = []
    for param in params:
        for section in cls.constant_times:
            if section[0] == param['section']:
                new_section = []
                new_section.append(section[0])
                for time in section[1:]:
                    if param['class'] in time[0]:
                        new_section.append(time)
                narrow_constant_times.append(new_section)
            else:
                # Check is section name already is in the list
                name_exits = False
                for sec in params:
                    if sec['section'] == section[0]:
                        name_exits = True
                        break
                for sec in narrow_constant_times:
                    if sec[0] == section[0]:
                        name_exits = True
                        break
                if not name_exits:
                    narrow_constant_times.append(section)
        for section in cls.variable_times:
            if section[0] == param['section']:
                new_section = []
                new_section.append(section[0])
                for time in section[1:]:
                    if param['class'] in time[0]:
                        new_section.append(time)
                narrow_variable_times.append(new_section)
            else:
                name_exits = False
                for sec in params:
                    if sec['section'] == section[0]:
                        name_exits = True
                        break
                for sec in narrow_variable_times:
                    if sec[0] == section[0]:
                        name_exits = True
                        break
                if not name_exits:
                    narrow_variable_times.append(section)
    return Course(cls.name, cls.semester, narrow_constant_times, narrow_variable_times)


def parse_request(request_string, semester, school):
    class_list = []
    for class_string in request_string.split(','):
        class_params = []
        try:
            class_params_str = class_string[class_string.index(
                '(') + 1: class_string.index(')')]
            for class_param_str in class_params_str.split("-"):
                try:
                    section_type = class_param_str[:class_param_str.index(":")]
                    class_num = class_param_str[class_param_str.index(
                        ":") + 1:]
                    class_param = {'section': section_type, 'class': class_num}
                    class_params.append(class_param)
                except Exception as e:
                    pass
            class_string = class_string[:class_string.index('(')]
        except Exception as e:
            pass
        results = searchClass(class_string, semester, school)
        for result in results:
            result = narrow_result(result, class_params)
            class_list.append(result)
    return class_list
