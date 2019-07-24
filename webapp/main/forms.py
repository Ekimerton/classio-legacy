from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

class SchoolForm(FlaskForm):
    schools = [('queens', "Queen's University")]
    name = SelectField('Select your school', validators=[DataRequired()], choices=schools)
    submit = SubmitField('Continue')

class ClassForm(FlaskForm):
    classes = StringField("Enter your classes, seperated with a comma:", validators=[DataRequired()])
    semester = SelectField('Semester', validators=[DataRequired()], choices=[('F', 'Fall'), ('W', 'Winter'), ('S', 'Summer')])
    submit = SubmitField('Optimize')
