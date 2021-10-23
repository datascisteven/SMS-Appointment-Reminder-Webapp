import arrow

from celery import Celery
from sqlalchemy.orm.exc import NoResultFound
from twilio.rest import Client
from ics import Calendar, Event

from reminders import db, app
from models.models import Appointment

twilio_account_sid = app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
twilio_number = app.config['TWILIO_NUMBER']
client = Client(twilio_account_sid, twilio_auth_token)

celery = Celery(app.import_name)
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task()
def send_sms_reminder(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    #
    time = arrow.get(appointment.appointment_time).to(appointment.appointment_timezone)
    body = "Hello {} {}, this is your friendly reminder of your upcoming appointment on {} at {}. Respond 1 to confirm, respond 2 to cancel. Please call directly to reschedule.".format(appointment.patient_first_name, appointment.patient_last_name, time.format('MMM-DD'), time.format('h:mma'))
    to = appointment.patient_phone

    client.messages.create(to, from_=twilio_number, body=body)


def send_sms_commit(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    time = arrow.get(appointment.appointment_time).to(appointment.appointment_timezone)
    body = "Hello {} {}, your appointment is booked for {} at {}. Respond with 3 to receive ICS file for your calendar.".format(appointment.patient_first_name, appointment.patient_last_name, time.format('MMM-DD'), time.format('h:mma'))
    to = appointment.patient_phone
    client.messages.create(to, from_=twilio_number, body=body)


def send_sms_edit(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    #
    time = arrow.get(appointment.appointment_time).to(appointment.appointment_timezone)
    body = "Hello {} {}, your upcoming appointment on {} at {} was recently changed.  Respond with 3 to receive updated ICS file for your calenda.".format(appointment.patient_first_name, appointment.patient_last_name, time.format('MMM-DD'), time.format('h:mma'))
    to = appointment.patient_phone

    client.messages.create(to, from_=twilio_number, body=body)    


def build_ics(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    
    appt_time = arrow.get(appointment.appointment_time).to(appointment.appointment_timezone)
    cal = Calendar()
    event = Event()
    event.add('summary', "Next Appointment with Dr. {}".format(appointment.provider_last_name))
    event.add('dtstart', appt_time.format('YYYY-MM-DD hh:mm:ss'))
    event.add('location', appointment.appointment_location)
    cal.add_component(event)

    with open(f'static/cal-{appointment.patient_last_name}-{appointment.appointment_time}.ics', 'wb') as ics:
        ics.write(cal.to_ical())
    
    ics_string = str(ics)
    
    return ics, ics_string
