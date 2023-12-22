from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from myapp.forms.service_location_forms import AddServiceLocationForm, EditServiceLocationForm
from myapp.database.service_location import ServiceLocation
from myapp.database.user import User
from myapp import db
import sqlite3

bp = Blueprint('service_location', __name__)

@bp.route('/add_service_location', methods=['GET', 'POST'])
def add_service_location():
    form = AddServiceLocationForm()

    if form.validate_on_submit():
        user_id = session['user_id']
        address = form.address.data
        unit_number = form.unit_number.data
        square_footage = form.square_footage.data
        bedrooms = form.bedrooms.data
        occupants = form.occupants.data

        con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO Service_Location (user_id, address, unit_number, square_footage, bedrooms, occupants) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, address, unit_number, square_footage, bedrooms, occupants),
        )

        con.commit()
        con.close()

        return redirect(url_for('profile'))

    return render_template('add_service_location.html', form=form)

@bp.route('/edit_service_location/<int:location_id>', methods=['GET', 'POST'])
def edit_service_location(location_id):
    form = EditServiceLocationForm()
    location = ServiceLocation.query.get(location_id)

    if form.validate_on_submit():
        address = form.address.data
        unit_number = form.unit_number.data
        square_footage = form.square_footage.data
        bedrooms = form.bedrooms.data
        occupants = form.occupants.data

        con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur = con.cursor()

        cur.execute(
            "UPDATE Service_Location SET address = ?, unit_number = ?, square_footage = ?, bedrooms = ?, occupants = ? "
            "WHERE id = ?",
            (address, unit_number, square_footage, bedrooms, occupants, location_id),
        )

        con.commit()
        con.close()

        return redirect(url_for('profile'))

    form.address.data = location.address
    form.unit_number.data = location.unit_number
    form.square_footage.data = location.square_footage
    form.bedrooms.data = location.bedrooms
    form.occupants.data = location.occupants

    return render_template('edit_service_location.html', form=form, location=location)

@bp.route('/delete_service_location/<int:location_id>', methods=['POST'])
def remove_service_location(location_id):
    location = ServiceLocation.query.get(location_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for('profile'))
