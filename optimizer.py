from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Course(Base):
    __tablename__ = "queens_course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    semester = Column('semester', String)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)

engine = create_engine('sqlite:///scrapers/queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

name = input("Enter the name of the class you would like to see: ")

courses = session.query(Course).filter_by(name=name)
for course in courses:
    print(course.name, course.semester)
    print(course.constant_times)
    print(course.variable_times)

courses = session.query(Course).filter_by(name=name+'A')
for course in courses:
    print(course.name, course.semester)
    print(course.constant_times)
    print(course.variable_times)

courses = session.query(Course).filter_by(name=name+'B')
for course in courses:
    print(course.name, course.semester)
    print(course.constant_times)
    print(course.variable_times)

session.close()
