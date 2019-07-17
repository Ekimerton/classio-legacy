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

engine = create_engine('sqlite:///scrapers/queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

name = input("Enter the name of the class you would like to see: ")
courses = session.query(CourseDB).filter_by(name=name)
for course in courses:
    print(course.name)
    print(course.)
