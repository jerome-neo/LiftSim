from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField

from wtforms.validators import DataRequired, EqualTo, NumberRange


class addRequestForm(FlaskForm):
    arrival_time = IntegerField('arrival_time')
    src = IntegerField('src', validators=[DataRequired(), NumberRange(1, 10)])
    dest = IntegerField('dest', validators=[DataRequired(), NumberRange(1, 10)])
