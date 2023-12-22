import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from myapp.forms.energy_forms import EnergyPriceForm
from myapp.database.energy_price import EnergyPrice
from myapp import db
import sqlite3

bp = Blueprint('energy', __name__)

@bp.route('/add_energy_price', methods=['GET', 'POST'])
def add_energy_price():
    form = EnergyPriceForm()

    con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur = con.cursor()

    if form.validate_on_submit():
        if not isinstance(form.hour.data, datetime):
            form.hour.data = datetime.strptime(form.hour.data, '%Y-%m-%dT%H:%M')

        cur.execute(
            "INSERT INTO Energy_Price (zip_code, hour, rate) VALUES (?, ?, ?)",
            (form.zip_code.data, form.hour.data, form.rate.data)
        )
        con.commit()
        con.close()

        return redirect(url_for('index'))

    return render_template('add_energy_price.html', form=form)

@bp.route('/energy_consumption/<int:service_location_id>/<string:time_resolution>')
def energy_consumption(service_location_id, time_resolution):
    if time_resolution == 'day':
        query = """
            SELECT DATE(e.Timestamp) AS date, SUM(e.Value) AS total_energy
            FROM event_data e
            JOIN enrolled_device ed ON e.Device_ID = ed.id
            WHERE ed.Service_Location_ID = :service_location_id
            GROUP BY date
        """
        con2 = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur2 = con2.cursor()
        data = cur2.execute(query, (service_location_id,)).fetchall()
    elif time_resolution == 'month':
        query = """
            SELECT strftime('%m', e.Timestamp) AS month, SUM(e.Value) AS total_energy
            FROM event_data e
            JOIN enrolled_device ed ON e.Device_ID = ed.id
            WHERE ed.Service_Location_ID = :service_location_id
            GROUP BY month
        """
        con2 = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
        cur2 = con2.cursor()
        data = cur2.execute(query, (service_location_id,)).fetchall()
        pass
    else:
        return "Invalid time resolution"

    labels = [str(row[0]) for row in data]
    values = [row[1] for row in data]
    con2.close()
    return render_template('energy_consumption.html', labels=labels, values=values, time_resolution=time_resolution)

@bp.route('/device_energy_consumption/<int:service_location_id>')
def device_energy_consumption(service_location_id):
    query = """
        SELECT * from device_energy_consumption where service_location_id=:service_location_id
    """
    con2 = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur2 = con2.cursor()
    data = cur2.execute(query, (service_location_id,)).fetchall()
    con2.close()
    model_ids = [row[0] for row in data]
    total_energies = [row[2] for row in data]


    return render_template('device_energy_consumption.html', model_ids=model_ids,  total_energies=total_energies)


@bp.route('/monthly_energy_cost/<int:service_location_id>')
def monthly_energy_cost(service_location_id):
    query = """
        SELECT * FROM monthly_energy_cost WHERE id = :service_location_id
    """
    con3 = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur3 = con3.cursor()
    data = cur3.execute(query, (service_location_id,)).fetchall()
    con3.close()

    months = [row[0] for row in data]
    total_energy_costs = [row[2] for row in data]

    return render_template('monthly_energy_cost.html', months=months, total_energy_costs=total_energy_costs)

@bp.route('/energy_price_zipcode')
def energy_price_zipcode():
    zip_code = request.args.get('zip_code')
    query = """
        Select hour,rate from energy_price where zip_code=:zip_code
    """
    con3 = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
    cur3 = con3.cursor()
    data = cur3.execute(query, (zip_code,)).fetchall()
    con3.close()

    hour = [row[0] for row in data]
    rate = [row[1] for row in data]

    return render_template('energy_price_zipcode.html', hours=hour,
                           rates=rate)
