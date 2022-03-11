from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
from flask import Blueprint, request, render_template, redirect, url_for, flash
import uuid
import hashlib

auth= Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@auth.route("/login", methods=['POST'])
def login_post():
    user_name = request.form.get('username')
    password = request.form.get('password')
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    user = User.query.filter_by(user_name=user_name).first()

    if not user:
        user_uid = str(uuid.uuid4())
        user_hash = md5_hash

        first_user = User(user_uid=user_uid, user_name=user_name, user_hash=user_hash)
        db.session.add(first_user)
        db.session.commit()
        flash('First user created', 'info')
        return redirect(url_for('auth.unblind'))
    else:
        if md5_hash != user.user_hash:
            flash('Login error', 'danger')
            return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    flash('Login ok', 'info')
    return redirect(url_for('main.unblind'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout ok', 'info')
    return redirect(url_for('auth.login'))
