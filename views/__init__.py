from models.models import Appointment
from views.views import (
    AppointmentResourceIndex,
    AppointmentResourceCreate,
    AppointmentResourceDelete,
    AppointmentResourceUpdate,
    AppointmentNewFormResource,
    AppointmentEditFormResource
)


def init_views(app):
    app.add_url_rule('/', view_func=AppointmentResourceIndex.as_view('appointment.index'))
    app.add_url_rule('/appointment', view_func=AppointmentResourceCreate.as_view('appointment.create'))
    app.add_url_rule('/appointment/<int:id>/delete', view_func=AppointmentResourceDelete.as_view('appointment.delete'))
    app.add_url_rule('/appointment/new', view_func=AppointmentNewFormResource.as_view('appointment.new'))
    app.add_url_rule('/appointment/<int:id>/update', view_func=AppointmentResourceUpdate.as_view('appointment.update'))
    app.add_url_rule('/appointment/edit', view_func=AppointmentEditFormResource.as_view('appointment.edit'))

"""
@app.route('/')
ded index():
    pass
===
def index():
    pass
app.add_url_rule('/', 'index', index)

"""
