from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

class SchoolForm(FlaskForm):
    schools = [('queens', "Queen's University"), ('waterloo', 'University of Waterloo')]
    name = SelectField('Select your school', validators=[DataRequired()], choices=schools)
    submit = SubmitField('Continue')

class ClassForm(FlaskForm):
    # Basic search
    classes = StringField("Enter your classes:", validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[('F', 'Fall'), ('W', 'Winter'), ('S', 'Summer')])

    # Advanced options
    lunch = IntegerRangeField('How important is not missing lunch for you?', default=60)
    dinner = IntegerRangeField('How important is not missing dinner for you?', default=60)
    offtime = IntegerRangeField('How important is minimizing time between classes for you?', default=40)
    lunch_time = StringField("Enter your desired lunch time range:")
    dinner_time = StringField("Enter your desired dinner time range:")

    submit = SubmitField('Optimize')
