from flask import Blueprint, render_template, redirect, url_for, session
from myapp.database.user import User
from myapp.database.user import EnergyPrice, EditProfileForm
from myapp import db
import sqlite3

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        all_zip_codes = db.session.query(EnergyPrice.zip_code).distinct().all()
        all_zip_codes = [zip_code[0] for zip_code in all_zip_codes]
        return render_template('profile.html', user=user, all_zip_codes=all_zip_codes)
    else:
        return redirect(url_for('auth.login'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()

    if 'user_id' in session:
        user = User.query.get(session['user_id'])

        if form.validate_on_submit():
            user_id = session['user_id']
            name = form.name.data
            billing_address_id = form.billing_address_id.data

            con = sqlite3.connect("C:\\Users\\TechPertz\\Desktop\\PDS\\PDS\\instance\\site.db")
            cur = con.cursor()

            cur.execute(
                "UPDATE User SET name = ?, billing_address_id = ? WHERE id = ?",
                (name, billing_address_id, user_id),
            )

            con.commit()
            con.close()

            return redirect(url_for('profile'))

        form.name.data = user.name
        form.billing_address_id.data = user.billing_address_id

        return render_template('edit_profile.html', form=form)
    else:
        return redirect(url_for('login'))


