from database import db
from datetime import datetime
import arrow


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

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
