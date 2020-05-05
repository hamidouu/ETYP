from flask import (Flask, render_template, request, escape, flash, json, jsonify,
                    url_for, redirect, make_response, session, Blueprint)
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:09869839@localhost/Pfa2'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'\x1d\xcf\n\xe9\x0f*\xe2_Z\xdd\xdb\x19\xd8L\x1e\xaf\x058\x17\xbd\xa1_2\xf4'

db= SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from views.login import auth
app.register_blueprint(auth)



from views.predict import pred
app.register_blueprint(pred)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")