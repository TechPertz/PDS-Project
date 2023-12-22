from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from myapp.forms.device_forms import DeviceModelForm, EnrollDeviceForm
from myapp.database.device import DeviceModel, EnrolledDevice
from myapp import db
import sqlite3

bp = Blueprint('device', __name__)

@bp.route('/add_device_model', methods=['GET', 'POST'])
def add_device_model():
    form = DeviceModelForm()

    if form.validate_on_submit():
        device_type = form.type.data
        model_number = form.model_number.data

        con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO DeviceModel (type, model_number) VALUES (?, ?)",
            (device_type, model_number),
        )

        con.commit()
        con.close()

        return redirect(url_for('add_device_model'))

    return render_template('add_device_model.html', form=form)

@bp.route('/add_device', methods=['GET', 'POST'])
def add_device():
    form = AddDeviceForm()

    if form.validate_on_submit():
        device_model = DeviceModel.query.filter_by(type=form.type.data, model_number=form.model_number.data).first()
        if not device_model:
            device_model = DeviceModel(type=form.type.data, model_number=form.model_number.data)
            db.session.add(device_model)
            db.session.commit()

        enrolled_device = EnrolledDevice(service_location_id=session['service_location_id'], device_model_id=device_model.id)
        db.session.add(enrolled_device)
        db.session.commit()
        return redirect(url_for('enroll_device'))

    return render_template('add_device.html', form=form)

@bp.route('/enroll_device', methods=['GET', 'POST'])
def enroll_device():
    form = EnrollDeviceForm()

    con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur = con.cursor()
    cur.execute("SELECT id, type, model_number FROM Device_Model")
    device_models = cur.fetchall()
    con.close()
    form.device_type.choices = [(model[0], f"{model[1]} - {model[2]}") for model in device_models]

    user_id = session['user_id']
    con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur = con.cursor()
    cur.execute("SELECT id, address FROM Service_Location WHERE user_id = ?", (user_id,))
    service_locations = cur.fetchall()
    con.close()
    form.service_location.choices = [(location[0], location[1]) for location in service_locations]

    if form.validate_on_submit():
        device_type_id = form.device_type.data
        service_location_id = form.service_location.data

        con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO Enrolled_Device (service_location_id, model_id) VALUES (?, ?)",
            (service_location_id, device_type_id),
        )

        con.commit()
        con.close()

        return redirect(url_for('profile'))

    return render_template('enroll_device.html', form=form)

@bp.route('/enrolled_devices')
def enrolled_devices():
    if 'user_id' in session:
        user_id = session['user_id']

        con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur = con.cursor()

        cur.execute("SELECT id FROM ServiceLocation WHERE user_id = ? LIMIT 1", (user_id,))
        service_location_id = cur.fetchone()

        if service_location_id:
            service_location_id = service_location_id[0]
            cur.execute("SELECT * FROM EnrolledDevice WHERE service_location_id = ?", (service_location_id,))
            enrolled_devices = cur.fetchall()

            devices_info = []
            for device in enrolled_devices:
                device_id = device[0]
                model_info = cur.execute("SELECT type, model_number FROM DeviceModel WHERE id = ?", (device[3],)).fetchone()
                devices_info.append({'id': device_id, 'type': model_info[0], 'model_number': model_info[1]})

            con.close()

            return render_template('enrolled_devices.html', user=user, devices_info=devices_info)
        else:
            flash("Please add a service location before viewing enrolled devices.", 'warning')
            return redirect(url_for('add_service_location'))
    else:
        return redirect(url_for('login'))

@bp.route('/remove_enrolled_device/<int:device_id>')
def remove_enrolled_device(device_id):
    enrolled_device = EnrolledDevice.query.get(device_id)
    
    if enrolled_device:
        db.session.delete(enrolled_device)
        db.session.commit()

    return redirect(url_for('profile'))
