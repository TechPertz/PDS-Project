from flask import Blueprint, render_template, redirect, url_for, request, session
from myapp.forms.event_forms import AddEventForm, AddEventLabelForm
from myapp.database.event import EventData, EventLabel
from myapp import db
from datetime import datetime
import sqlite3

bp = Blueprint('event', __name__)

@bp.route('/add_event/<int:device_id>', methods=['GET', 'POST'])
def add_event(device_id):
    form = AddEventForm()

    con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur = con.cursor()

    cur.execute("SELECT id, label_name FROM Event_Label")
    event_labels = cur.fetchall()

    form.label_id.choices = [(label[0], label[1]) for label in event_labels]

    if form.validate_on_submit():
        if not isinstance(form.timestamp.data, datetime):
            form.timestamp.data = datetime.strptime(form.timestamp.data, '%Y-%m-%dT%H:%M')
        cur.execute(
            "INSERT INTO Event_Data (device_id, timestamp, label_id, value) VALUES (?, ?, ?, ?)",
            (device_id, form.timestamp.data, form.label_id.data, form.value.data)
        )
        con.commit()
        con.close()

        return redirect(url_for('add_event', device_id=device_id))

    return render_template('add_event.html', form=form, device_id=device_id)

@bp.route('/add_event_label', methods=['GET', 'POST'])
def add_event_label():
    form = AddEventLabelForm()

    con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur = con.cursor()

    if form.validate_on_submit():
        cur.execute("INSERT INTO Event_Label (label_name) VALUES (?)", (form.label_name.data,))
        con.commit()
        con.close()

        return redirect(url_for('index'))

    return render_template('add_event_label.html', form=form)
