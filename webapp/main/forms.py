from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

class SchoolForm(FlaskForm):
    schools = [('queens', "Queen's University")]
    semester = SelectField('Select your semester', validators=[DataRequired()], choices=[('F', 'Fall'), ('W', 'Winter'), ('S', 'Summer')])
    name = SelectField('Select your school', validators=[DataRequired()], choices=schools)
    submit = SubmitField('Continue')

class ClassForm(FlaskForm):
    classes = StringField("Classes", validators=[DataRequired()])
    submit = SubmitField('Optimize')
