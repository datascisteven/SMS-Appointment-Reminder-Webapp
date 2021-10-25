from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]

# event_types = [('booked', 'Booked'),
#                ('modified', 'Modified'),
#                ('noshowed', 'No-Showed'),
#                ('cancelled', 'Cancelled'),
#                ('confirmed', 'Confirmed')]

times = ['0.25', '0.5', '1', '2', '12', '24', '48', '168']

def _intervals(): 
    return [(hr, hr + ' hours') for hr in times]

class EditAppointmentForm(FlaskForm):
    # event_type = SelectField(
    #     'Event Type', choices=event_types, validators=[DataRequired()], default='modified')
    # event_time = DateTimeField(
    #     'Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p", default=utcnow)
    # patient_id = IntegerField('Patient ID', validators=[DataRequired(), Length(min=6)])
    first = StringField(
        'Patient First Name', validators=[DataRequired()])
    last = StringField(
        'Patient Last Name', validators=[DataRequired()])
    mobile = StringField(
        'Patient Mobile Number', validators=[DataRequired(), Length(min=10)])
    # provider_id = IntegerField('Provider ID', validators=[DataRequired(), Length(min=6)])
    dr_first = StringField(
        'Provider First Name', validators=[DataRequired()])
    dr_last = StringField(
        'Provider Last Name', validators=[DataRequired()])
    location = StringField(
        'Appointment Location', validators=[DataRequired()])
    interval = SelectField(
        'Reminder Interval', choices=_intervals(), validators=[DataRequired()], default=48)
    time = DateTimeField(
        'Appointment Time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p")
    timezone = SelectField(
        'Appointment Timezone', choices=_timezones(), validators=[DataRequired()])
