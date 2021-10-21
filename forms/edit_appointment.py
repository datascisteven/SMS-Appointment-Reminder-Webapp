from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]

appointment_times = [(0.25, '15 mins'), 
                     (0.50, '30 mins'), 
                     (1.0, '1 hour'), 
                     (2.0, '2 hours'), 
                     (12.0, '12 hours'), 
                     (24.0, '24 hours'), 
                     (38.0, '48 hours'),
                     (168.0, '1 week')]

class EditAppointmentForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired(), Length(min=6)])
    patient_first_name = StringField('Patient First Name', validators=[DataRequired()])
    patient_last_name = StringField('Patient Last Name', validators=[DataRequired()])
    patient_phone = StringField('Patient Phone', validators=[DataRequired(), Length(min=10)])
    provider_id = IntegerField('Provider ID', validators=[DataRequired(), Length(min=6)])
    provider_first_name = StringField('Provider First Name', validators=[DataRequired()])
    provider_last_name = StringField('Provider Last Name', validators=[DataRequired()])
    appointment_location = StringField('Appointment Location', validators=[DataRequired()])
    appointment_delta = SelectField('Appointment Reminder', choices=appointment_times, validators=[DataRequired()])
    appointment_time = DateTimeField('Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p")
    appointment_timezone = SelectField('Appointment Timezone', choices=_timezones(), validators=[DataRequired()])