from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length
from pytz import common_timezones


def _timezones():
    return [(tz, tz) for tz in common_timezones][::-1]


appointment_times = [(t, t + " hour") for t in ['0.25', '0.50', '0.75', '1', '2', '12', '24', '48']]


class NewAppointmentForm(FlaskForm):
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
