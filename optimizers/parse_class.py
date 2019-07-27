from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import sessionmaker
import scrapers.waterloo  as waterloo

Base = declarative_base()
class CourseDB(Base):
    __tablename__ = "queens_course"
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

def parseClass(course):
    constant_t = []
    variable_t = []
    if course.constant_times:
        for type in course.constant_times.split('-'):
            class_list = []
            section_name = type[:type.index(':')]
            type = type[type.index(':') + 1:]
            for choice in type.split(';'):
                date_list = []
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
                date_list = []
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
        print(school)
        engine = create_engine('sqlite:///scrapers/{}.db'.format(school))
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        class_list = []
        try:
            courses = session.query(CourseDB).filter_by(name=name, semester=semester).first()
            class_list.append(parseClass(courses))
        except:
            pass
        try:
            courses = session.query(CourseDB).filter_by(name=name+'A', semester=semester).first()
            class_list.append(parseClass(courses))
        except:
            pass
        try:
            courses = session.query(CourseDB).filter_by(name=name+'B', semester=semester).first()
            class_list.append(parseClass(courses))
        except:
            pass
        session.close()
        return class_list
    elif school == "waterloo":
        class_list = []
        try:
            result = waterloo.find_class(semester, name)
            if result:
                class_list.append(result)
        except:
            pass
        return class_list

def parse_request(request_string, semester, school):
    class_list = []
    for class_name in request_string.split(','):
        class_list += searchClass(class_name, semester, school)
    return class_list
