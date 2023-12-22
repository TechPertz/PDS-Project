from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, StringField
from wtforms import DateTimeLocalField
from wtforms.validators import DataRequired, InputRequired

class AddEventForm(FlaskForm):
    timestamp = DateTimeLocalField('Timestamp', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    label_id = SelectField('Label', coerce=int, validators=[InputRequired()])
    value = IntegerField('Value', validators=[InputRequired()])
    submit = SubmitField('Add Event')

class AddEventLabelForm(FlaskForm):
    label_name = StringField('Event Label', validators=[DataRequired()])
    submit = SubmitField('Add Label')
