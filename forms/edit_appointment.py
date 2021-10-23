from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]

times = 0.25, 0.5, 1, 2, 12, 24, 48, 168

def _appointment_times(): 
    return [(hr, str(hr) + ' hrs') for hr in times]

class EditAppointmentForm(FlaskForm):
    # patient_id = IntegerField('Patient ID', validators=[DataRequired(), Length(min=6)])
    patient_first_name = StringField('Patient First Name', validators=[DataRequired()])
    patient_last_name = StringField('Patient Last Name', validators=[DataRequired()])
    patient_phone = StringField('Patient Phone', validators=[DataRequired(), Length(min=10)])
    # provider_id = IntegerField('Provider ID', validators=[DataRequired(), Length(min=6)])
    provider_first_name = StringField('Provider First Name', validators=[DataRequired()])
    provider_last_name = StringField('Provider Last Name', validators=[DataRequired()])
    appointment_location = StringField('Appointment Location', validators=[DataRequired()])
    appointment_delta = SelectField('Appointment Reminder', choices=_appointment_times(), validators=[DataRequired()])
    appointment_time = DateTimeField('Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p")
    appointment_timezone = SelectField('Appointment Timezone', choices=_timezones(), validators=[DataRequired()])