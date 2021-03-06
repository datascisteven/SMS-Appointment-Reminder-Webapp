import arrow

from flask.views import MethodView
from flask import render_template, request, redirect, url_for

from database import db
from models.models import Appointment
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
            from tasks import send_sms_reminder, send_sms_commit
            appt = Appointment(
                # event_type=form.data['event_type'],
                # event_time=form.data['event_time'],
                first=form.data['first'],
                last=form.data['last'],
                mobile=form.data['mobile'],
                dr_first=form.data['dr_first'],
                dr_last=form.data['dr_last'],
                location=form.data['location'],
                interval=form.data['interval'],
                time=form.data['time'],
                timezone=form.data['timezone'],
            )
            appt.time = arrow.get(appt.time, appt.timezone).to('utc').naive
            db.session.add(appt)
            db.session.commit()
            send_sms_reminder.apply_async(
                args=[appt.id], eta=appt.get_notification_time()
            )
            send_sms_commit.apply_async(
                args=[appt.id], eta=arrow.utcnow()
            )
            return redirect(url_for('appointment.index'), code=303)
        else:
            return render_template('appointments/new.html', title='New', form=form), 400

class AppointmentResourceUpdate(MethodView):
    def post(self, id):
        appt = db.session.query(Appointment).filter_by(id=id).one()
        form = EditAppointmentForm(request.form)
        if form.validate():
            from tasks import send_sms_edit
            appt = Appointment(
                # event_type=form.data['event_type'],
                # event_time=form.data['event_time'],
                first=form.data['first'],
                last=form.data['last'],
                mobile=form.data['mobile'],
                dr_first=form.data['dr_first'],
                dr_last=form.data['dr_last'],
                location=form.data['location'],
                interval=form.data['interval'],
                time=form.data['time'],
                timezone=form.data['timezone'],
            )
            appt.time = arrow.get(appt.time, appt.timezone).to('utc').naive
            # db.session.add(appt)
            db.session.commit()
            send_sms_edit.apply_async(
                args=[appt.id], eta=arrow.utcnow()
            )
            return redirect(url_for('appointment.index'), code=303)
        else:
            return render_template('appointments/edit.html', title='Edit', form=form), 400

class AppointmentResourceIndex(MethodView):
    def get(self):
        all_appointments = db.session.query(Appointment).all()
        return render_template('appointments/index.html', appointments=all_appointments)


class AppointmentNewFormResource(MethodView):
    def get(self):
        form = NewAppointmentForm()
        return render_template('appointments/new.html', form=form)


class AppointmentEditFormResource(MethodView):
    def get(self):
        form = EditAppointmentForm()
        return render_template('appointments/edit.html', form=form)

# class AppointmentEditFormResource(MethodView):
#     def get(self):
#         form = EditAppointmentForm(request.form)
#         if form.validate_on_submit():
#             appt = Appointment(
#                 # event_type=form.data['event_type'],
#                 # event_time=form.data['event_time'],
#                 first=form.data['first'],
#                 last=form.data['last'],
#                 mobile=form.data['mobile'],
#                 dr_first=form.data['dr_first'],
#                 dr_last=form.data['dr_last'],
#                 location=form.data['location'],
#                 interval=form.data['interval'],
#                 time=form.data['time'],
#                 timezone=form.data['timezone'],
#             )
#             db.session.commit(appt)
#         return render_template('appointments/edit.html', form=form)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @app.route("/account")
# @login_required
# def account():
#     return render_template('account.html', title='Account')