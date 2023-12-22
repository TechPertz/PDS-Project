from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

class DeviceModelForm(FlaskForm):
    type = StringField('Device Type', validators=[DataRequired()])
    model_number = StringField('Model Number', validators=[DataRequired()])
    submit = SubmitField('Add Device Model')

class EnrollDeviceForm(FlaskForm):
    device_type = SelectField('Device Type', coerce=int, validators=[DataRequired()])
    service_location = SelectField('Service Location', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Enroll Device')
