from database import db
from datetime import datetime
import arrow


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    # event_type = db.Column(db.String, nullable=False)
    # event_time = db.Column(db.DateTime, nullable=False)
    # patient_id = db.Column(db.Integer)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    # provider_id = db.Column(db.Integer)
    dr_first = db.Column(db.String(50), nullable=False)
    dr_last = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    timezone = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Appointment %r %r>' % self.first, self.last

    def get_notification_time(self):
        appointment_time = arrow.get(self.time)
        reminder_time = appointment_time.shift(hours=-self.interval)
        return reminder_time
