from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from myapp.forms.user_forms import LoginForm, RegistrationForm
from myapp.database.user import User
from myapp import db
import sqlite3

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and (user.password == form.password.data or check_password_hash(user.password, form.password.data)):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            if not user:
                error_message = "Invalid username. Please check your username and try again."
            else:
                error_message = "Invalid password. Please check your password and try again."

    return render_template('login.html', form=form, current_user=None, error_message=error_message)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error_message = None

    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            error_message = "Username already exists. Please choose a different one."
        else:
            username = form.username.data
            password = form.password.data
            name = form.name.data
            billing_address_id = form.billing_address_id.data
            zip_code = form.zip_code.data
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256')


            con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
            cur = con.cursor()

            cur.execute(
                "INSERT INTO User (username, password, name, billing_address_id, zip_code) VALUES (?, ?, ?, ?, ?)",
                (username, password, name, billing_address_id, zip_code),
            )

            cur.execute(
                "INSERT INTO Address (address, zip_code) VALUES (?, ?)",
                (billing_address_id, zip_code),
            )

            con.commit()
            new_user = User.query.filter_by(username=username).first()

            con.close()
            
            session['user_id'] = new_user.id

            return redirect(url_for('index'))

    return render_template('register.html', form=form, error_message=error_message)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
