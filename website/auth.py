from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from website.forms import RegisterForm, LoginForm, ContactForms
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db  ##means from __init__.py import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    form = LoginForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
       
        if len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
            return render_template('login.html', user=current_user, form=form)
        if len(password) < 7:
            flash("Password must be at least 7 characters", category="error")
            return render_template('login.html', user=current_user, form=form)
        if not email or not password:
            flash("Please fill out all fields", category="error")
            return render_template('login.html', user=current_user, form=form)


        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash("Login successful!", category="success")
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash("username or password is incorrect", category="error")
        
    return render_template('login.html', user=current_user, form=form)    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", category="info")
    return redirect(url_for('auth.login'))
    

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        # if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        password1 = form.password.data
        password2 = form.confirm_password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exits", category="error")
      
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        
        elif len(name) < 2: 
            flash("Name must be greater than 2 characters", category="error")

        elif password1 != password2:
            flash("Passwords do not match", category="error")

        elif len(password1) < 7:
            flash("Password must be at least 7 characters", category="error")    

        else:    
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(form.password.data, method='pbkdf2:sha256')
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Account created!", "success")
            return redirect(url_for('views.home'))
    
    return render_template('sign_up.html', user=current_user, form=form)    