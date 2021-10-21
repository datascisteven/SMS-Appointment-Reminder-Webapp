import arrow

from flask.views import MethodView
from flask import render_template, request, redirect, url_for

from database import db
from models.appointment import Appointment
from forms.new_appointment import NewAppointmentForm
from forms.edit_appointment import EditAppointmentForm


class AppointmentResourceDelete(MethodView):
    def post(self, id):
        appt = db.session.query(Appointment).filter_by(id=id).one()
        db.session.delete(appt)
        db.session.commit()

        return redirect(url_for('appointment.index'), code=303)


class AppointmentResourceCreate(MethodView):
    def post(self):
        form = NewAppointmentForm(request.form)

        if form.validate():
            from tasks import send_sms_reminder

            appt = Appointment(
                name=form.data['name'],
                phone_number=form.data['phone_number'],
                provider_name=form.data['provider_name'],
                delta=form.data['delta'],
                time=form.data['time'],
                timezone=form.data['timezone'],
            )

            appt.time = arrow.get(appt.time, appt.timezone).to('utc').naive

            db.session.add(appt)
            db.session.commit()
            send_sms_reminder.apply_async(
                args=[appt.id], eta=appt.get_notification_time()
            )

            return redirect(url_for('appointment.index'), code=303)
        else:
            return render_template('appointments/new.html', form=form), 400


class AppointmentResourceEdit(MethodView):
    def post(self, id):
        appt = db.session.query(Appointment).filter_by(id=id).one()
        form = EditAppointmentForm(request.form)
        if form.validate():
            from tasks import send_sms_reminder

            appt = Appointment(
                name=form.data['name'],
                phone_number=form.data['phone_number'],
                provider_name=form.data['provider_name'],
                delta=form.data['delta'],
                time=form.data['time'],
                timezone=form.data['timezone'],
            )
            appt.time = arrow.get(appt.time, appt.timezone).to('utc').naive

            db.session.add(appt)
            db.session.commit()
            send_sms_reminder.apply_async(
                args=[appt.id], eta=appt.get_notification_time()
            )

            return redirect(url_for('appointment.index'), code=303)
        else:
            return render_template('appointments/edit.html', form=form), 400

     

class AppointmentResourceIndex(MethodView):
    def get(self):
        all_appointments = db.session.query(Appointment).all()
        return render_template('appointments/index.html', appointments=all_appointments)


class AppointmentFormResource(MethodView):
    def get(self):
        form = NewAppointmentForm()
        return render_template('appointments/new.html', form=form)


class AppointmentEditFormResource(MethodView):
    def get(self):
        form = EditAppointmentForm()
        return render_template('appointmmets/edit.html', form=form)
