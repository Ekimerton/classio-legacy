from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms_components import TimeField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

# Custom validator for lunch_time and dinner_time


def check_time(form, field):
    try:
        first_time, second_time = field.data.replace(":", "").split("-")
        int(first_time)
        int(second_time)
        if len(first_time) != 4 or len(second_time) != 4:
            raise ValidationError('Please enter a valid times.')
        if int(first_time[:2]) > 24 or int(first_time[2:]) > 60 or int(second_time[:2]) > 24 or int(second_time[:2]) > 60:
            raise ValidationError('Please enter valid times.')
        if first_time > second_time:
            raise ValidationError(
                "The first time can't be after the second time.")
    except Exception as e:
        print(e)
        raise ValidationError('Please enter a valid time format.')


class SchoolForm(FlaskForm):
    schools = [('queens', "Queen's University"), ('waterloo',
                                                  'University of Waterloo'), ('ubc', 'University of British Columbia')]
    name = SelectField('Select your school:', validators=[
                       DataRequired()], choices=schools)
    submit = SubmitField('Continue')


class ClassForm(FlaskForm):
    # Basic search
    classes = StringField("Enter your classes:", validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[
                           ('F', 'Fall'), ('W', 'Winter'), ('S', 'Summer')])

    # Advanced options
    lunch = IntegerRangeField(
        'How important is not missing lunch for you?', default=60)
    dinner = IntegerRangeField(
        'How important is not missing dinner for you?', default=60)
    offtime = IntegerRangeField(
        'How important is minimizing time between classes for you?', default=40)
    lunch_start = TimeField(
        "At what time would you like to eat lunch?", validators=[DataRequired()])
    lunch_end = TimeField(
        "At what time would you like to eat lunch?", validators=[DataRequired()])
    dinner_start = TimeField(
        "At what time would you like to eat dinner?", validators=[DataRequired()])
    dinner_end = TimeField(
        "At what time would you like to eat dinner?", validators=[DataRequired()])

    submit = SubmitField('Optimize')
