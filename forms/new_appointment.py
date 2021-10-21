from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField, IntegerField
from wtforms.fields.simple import TextField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]

event_types = [('booked', 'Booked'),
               ('rescheduled', 'Rescheduled'),
               ('modified', 'Modified'),
               ('noshowed', 'No-Showed'),
               ('cancelled', 'Cancelled'),
               ('confirmed', 'Confirmed')]

appointment_times = [(0.25, '15 mins'), 
                     (0.50, '30 mins'), 
                     (1.0, '1 hour'), 
                     (2.0, '2 hours'), 
                     (12.0, '12 hours'), 
                     (24.0, '24 hours'), 
                     (38.0, '48 hours'),
                     (168.0, '1 week')]

class NewAppointmentForm(FlaskForm):
    # event_type = SelectField(
    #     'Event Type', choices=event_types, validators=[DataRequired()]
    # )
    # event_time = DateTimeField(
    #     'Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p"
    # )
    patient_id = TextField('Patient ID')
    patient_first_name = StringField('Patient First Name', validators=[DataRequired()])
    patient_last_name = StringField('Patient Last Name', validators=[DataRequired()])
    patient_phone = TextField('Patient Phone', validators=[DataRequired(), Length(min=6)])
    provider_id = TextField('Provider ID')
    provider_first_name = StringField('Provider First Name', validators=[DataRequired()])
    provider_last_name = StringField('Provider Last Name', validators=[DataRequired()])
    appointment_location = StringField('Appointment Location', validators=[DataRequired()])
    appointment_delta = SelectField(
        'Appointment Reminder', choices=appointment_times, validators=[DataRequired()]
    )
    appointment_time = DateTimeField(
        'Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p"
    )
    appointment_timezone = SelectField('Appointment Timezone', choices=_timezones(), validators=[DataRequired()])


