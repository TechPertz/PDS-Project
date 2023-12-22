from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class AddServiceLocationForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    unit_number = StringField('Unit Number')
    square_footage = IntegerField('Square Footage')
    bedrooms = IntegerField('Bedrooms')
    occupants = IntegerField('Occupants')
    submit = SubmitField('Add Service Location')

class EditServiceLocationForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    unit_number = StringField('Unit Number')
    square_footage = IntegerField('Square Footage')
    bedrooms = IntegerField('Bedrooms')
    occupants = IntegerField('Occupants')
    submit = SubmitField('Update Service Location')
