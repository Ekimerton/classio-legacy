from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Optional, ValidationError

class SchoolForm(FlaskForm):
    name = SelectField('Select your school', choices=[('Queens', "Queen's University")], validators=[InputRequired()])
    submit = SubmitField('Search')
