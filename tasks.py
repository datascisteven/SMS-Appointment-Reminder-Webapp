import arrow

from celery import Celery
from sqlalchemy.orm.exc import NoResultFound
from twilio.rest import Client

from ics import Calendar, Event
from reminders import db, app
from models.models import Appointment
from twilio.twiml.messaging_response import MessagingResponse

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
    time = arrow.get(appointment.time).to(appointment.timezone)
    body = "Hello {0} {1}, your friendly reminder of an upcoming appointment on {2} at {3}. Reply 1 to confirm, 2 to cancel. Please call directly to reschedule.".format(
        appointment.first, appointment.last, time.format('MMM-DD'), time.format('h:mma')
    )
    to = appointment.mobile
    client.messages.create(to, from_=twilio_number, body=body)

@celery.task()
def send_sms_commit(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    
    time = arrow.get(appointment.time).to(appointment.timezone)
    body = "Hello {0} {1}, your appointment is booked for {2} at {3}. Reply 3 for ICS calender file.".format(
        appointment.first, appointment.last, time.format('MMM-DD'), time.format('h:mma')
    )
    to = appointment.mobile
    client.messages.create(to, from_=twilio_number, body=body)

@celery.task()
def send_sms_edit(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    #
    time = arrow.get(appointment.time).to(appointment.timezone)
    body = "Hello {0} {1}, your appointment on {2} at {3} was recently changed.  Reply 3 for updated ICS file.".format(
        appointment.first, appointment.last, time.format('MMM-DD'), time.format('h:mma')
    )
    to = appointment.mobile
    client.messages.create(to, from_=twilio_number, body=body)    

@celery.task()
def send_ics(appointment_id):
    try:
        appointment = db.session.query(Appointment).filter_by(id=appointment_id).one()
    except NoResultFound:
        return
    
    time = arrow.get(appointment.time).to(appointment.timezone)
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    event = Event()
    event.add('summary', 'VA Medical Appointment')
    event.add('dtstart', time.format('YYYYMMDDThhmmss'))
    event.add('dtend', time.shift(hours=+1).format('YYYYMMDDThhmmss'))
    event.add('location', 'appointment.location')
    cal.add_component(event)
    f = open('static/appointment.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

    body = "Hello {} {}, here is the ICS file for your appointment.".format(
        appointment.first, appointment.last
    )
    to = appointment.mobile
    client.messages.create(
        to, 
        from_=twilio_number, 
        body=body,
        media_url=['static/appointment.ics'])
    
