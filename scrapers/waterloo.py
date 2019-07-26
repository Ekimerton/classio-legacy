import sqlite3

# SQL/SQLite model classes
Base = declarative_base()
class Course(Base):
    __tablename__ = "course"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    semester = Column('semester', String)
    constant_times = Column('constant_times', Text, unique=False)
    variable_times = Column('variable_times', Text, unique=False)

# SQLAlchemy creation
engine = create_engine('sqlite:///waterloo.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# start index
start = int(input("Enter the last number that was parsed: "))
semester = input("Fall, Winter or Spring? (2019/2020): ")
if not semester in ['Fall', 'Winter', 'Spring']:
    print("Please enter 'Fall' or 'Winter'")
    exit()
semester_dict = {'Spring':'1195', 'Fall':'1199', 'Winter':'1201'}
sem = semester_dict[semester]
