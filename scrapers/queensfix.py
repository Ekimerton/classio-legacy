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

engine = create_engine('sqlite:///queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

courses = session.query(Course).filter_by(name='CISC124').all()
for course in courses:
    constant_t = course.constant_times
    variable_t = course.variable_times
    if constant_t:
        constant_t = constant_t.replace('-', '0-') + "0"
    if variable_t:
        variable_t = variable_t.replace('-', '0-') + "0"
    course.constant_times = constant_t
    course.variable_times = variable_t
    session.commit()

session.close()
