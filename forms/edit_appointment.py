from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]


appointment_times = [(5, '5 mins'), 
                     (10, '10 mins'), 
                     (15, '15 mins'), 
                     (30, '30 mins'), 
                     (60, '1 hour'), 
                     (120, '2 hours'), 
                     (720, '12 hours'), 
                     (1440, '24 hours'), 
                     (2880, '48 hours'),
                     (10080, '1 week')]


class EditAppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[DataRequired(), Length(min=6)])
    provider_name = StringField('Provider Name', validators=[DataRequired()])
    delta = SelectField(
        'Notification time', choices=appointment_times, validators=[DataRequired()]
    )
    time = DateTimeField(
        'Appointment time', validators=[DataRequired()], format="%m-%d-%Y %I:%M%p"
    )
    timezone = SelectField('Time zone', choices=_timezones(), validators=[DataRequired()])