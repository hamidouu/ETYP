from flask import render_template, Blueprint, request, url_for, flash, redirect, request, session
from models import Users
from models import db, bcrypt
from views.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='templates')

"""@login.route('/new', methods=['POST', 'GET'])
def createAccount():
    if request.method == "POST":
        firstName = request.form.get('FirstName')
        lastName = request.form.get('LastName')
        email = request.form.get('Email')
        password = request.form.get('Password')
        username = request.form.get('Username')
        user = Users(firstName, lastName, email, username, password)
        db.session.add(user)
        db.session.commit()
    return render_template("registration.html")
"""

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user = Users(firstName, lastName, email, username, password)
        user = Users(firstName=form.firstname.data, lastName=form.lastname.data, email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        #session['logged_in'] = True

        return redirect(url_for('auth.login',messages=''))
    return render_template('registration.html', title='Register', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args['messages'] 
            #next_page = request.args.get("next")
            print("*************")
            print(next_page)
            session['logged_in'] = True
            return redirect(next_page) if next_page=="/predict" else redirect(url_for('home'))

            #flash('Login successful.', 'success')
            #if next_page=="/predict":
            #    return redirect(next_page) 
            #else:               
            #    redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            return redirect(url_for('auth.redirected'))
    return render_template('login.html', title='Login', form=form)

@auth.route("/redirected", methods=['GET', 'POST'])
def redirected():
    return redirect(url_for('auth.login' , messages=''))


@auth.route("/logout")
def logout():
    logout_user()
    session['logged_in'] = False

    return redirect(url_for('home'))

