def hour12to24(timestamp):
    ep_index = timestamp.index(":")
    hour = int(timestamp[:ep_index])
    minute = timestamp[ep_index + 1:ep_index + 3]
    am_pm = timestamp[ep_index + 3:ep_index + 5]
    if am_pm == "PM":
        hour = str(hour + 12)
    if am_pm == "AM" and hour < 10:
        hour = "0" + str(hour)
    return str(hour) + minute

def standardizeTime(init_time):
    stnd_time = ""
    bits = init_time.split(", ")
    for bit in bits:
        stnd_time = stnd_time + bit[:2] + hour12to24(bit[3: bit.index('-')]) + hour12to24(bit[bit.index('-') + 2:]) + ","

    return stnd_time[:len(stnd_time)-1]

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
class Course(Base):
    __tablename__ = "queens_course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)

engine = create_engine('sqlite:///scrapers/queens.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

'''
course = Course()
course.name = "Helloninja"
course.constant_times = "constant"
course.variable_times = "variable"
session.add(course)
session.commit()
'''
courses = session.query(Course).all()
for course in courses:
    print(course.name)
    print(course.constant_times)
    print(course.variable_times)

session.close()
