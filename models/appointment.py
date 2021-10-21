from database import db
from datetime import datetime
import arrow


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    # event_type = db.Column(db.String, nullable=False)
    # event_time = db.Column(db.DateTime, nullable=False)
    patient_id = db.Column(db.Integer)
    patient_first_name = db.Column(db.String, nullable=False)
    patient_last_name = db.Column(db.String, nullable=False)
    patient_phone = db.Column(db.String(50), nullable=False)
    patient_id = db.Column(db.Integer)
    provider_name = db.Column(db.String(50), nullable=False)
    provider_name = db.Column(db.String(50), nullable=False)
    appointment_location = db.Column(db.String(255), nullable=False)
    appointment_delta = db.Column(db.Integer, nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    appointment_timezone = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Appointment %r %r>' % self.patient_first_name, self.patient_last_name

    def get_notification_time(self):
        appointment_time = arrow.get(self.appointment_time)
        reminder_time = appointment_time.shift(hours=-self.appointment_delta)
        return reminder_time
