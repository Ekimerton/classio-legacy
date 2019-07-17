from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class CourseDB(Base):
    __tablename__ = "queens_course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    semester = Column('semester', String)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)

class Course():
    def __init__(id, name, semester, constant_times, variable_times):
        name = name
        semester = semester
        constant_times = constant_times
        variable_times = variable_times

def mergeCopies(times_list):
    new_list = []
    for i in range(0, len(times_list) - 1):
        for j in range(0, len(times_list) - 1):
            if times_list[i][0] = times_list[j][0]:


def parseClass(courses):
    for course in courses:
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
            print(constant_t)

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
            print(variable_t)

engine = create_engine('sqlite:///scrapers/queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

name = input("Enter the name of the class you would like to see: ")
class_list = []

courses = session.query(CourseDB).filter_by(name=name)
parseClass(courses)

#courses = session.query(CourseDB).filter_by(name=name+'A')
#parseClass(courses)

#courses = session.query(CourseDB).filter_by(name=name+'B')
#parseClass(courses)

session.close()
