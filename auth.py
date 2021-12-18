import re
from threading import current_thread
import flask as fl
from flask import request
from flask.helpers import flash, get_flashed_messages, url_for
from flask.templating import render_template
from flask_login.utils import login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from app import db
from dataModels import User
from werkzeug.security import check_password_hash, generate_password_hash
from is_safe_url import is_safe_url

auth = fl.Blueprint("auth",__name__)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        message = ""
        try:
            message = get_flashed_messages()[0]
        except:
            pass

        url_to_str = "?next="

        url_to = request.args.get('next')

        print(url_to == None)

        if url_to == None:
            url_to_str = ""
        else:
            url_to_str += str(url_to)

        return render_template('login.jinja2',message = message,url_to=url_to_str)
    if request.method == "POST":
        name = request.form.get('uName')
        password = request.form.get('psw')
        
        remember = request.form.get('remember')

        user = User.query.filter_by(name=name).first()

        if user and check_password_hash(user.password,password):
            login_user(user,remember=bool(remember))

            url_to = request.args.get('next')

            if(url_to == None):
                return redirect(url_for('main.index'))
            else:
                if not is_safe_url(url_to, {"localhost,127.0.0.1,your-domain.de"}):
                    return redirect(url_for('main.index'))
                else:
                    return redirect(url_to)

        else:
            flash("Invalid login details")
            return redirect(url_for('auth.login'))
        


@auth.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        
        users = User.query.all()

        if users:
            return fl.redirect(url_for('auth.login'))
        else:
            return render_template('signup.jinja2')

    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')

        addUser(name,password)

        return fl.redirect(url_for('auth.login'))


def addUser(name:str,password:str):
    
    password = generate_password_hash(password,method="sha256",salt_length=32)
    
    new_User = User(name = name,password=password)
    db.session.add(new_User)
    db.session.commit()