from . import app, db, JWT_KEY, bcrypt, login_manager
from flask import render_template, flash, redirect, url_for
from .forms import SubscribersForm, Login, Register, FileUpload
from .models import Subscribers, Admin
import datetime
from flask_login import current_user, login_user, logout_user, login_required
import jwt
from .util import send_verification_mail

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route("/", methods = ['POST', 'GET'])
@app.route("/home", methods = ['POST', 'GET'])
def home():
    form = SubscribersForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        #till learn celery
        subscriber = Subscribers(name = name, email = email)
        db.session.add(subscriber)
        db.session.commit()
        #for mail verification
        '''payload = {"email": email, "name": name, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=1800)}
        encoded = jwt.encode(payload, JWT_KEY, algorithm="HS256")
        send_verification_mail(encoded, email)'''
        return render_template('success.html', email = email, name = name)
    return render_template('register.html', form = form)


@app.route("/verification/<string:token>")
def verification(token):
    try:
        details = jwt.decode(token, JWT_KEY, algorithms=["HS256"])
        name, email = details['name'], details['email'] 
        subscriber = Subscribers(name = name, email = email)
        db.session.add(subscriber)
        db.session.commit()
    except jwt.ExpiredSignatureError:
        return render_template("verifiedStatus.html", status = False, msg ="Link expired")
    return render_template("verifiedStatus.html", status = True, email = email)

@login_required
@app.route("/adminRegister", methods = ['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(email = form.email.data, password = hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash("Successfully registered", "success")
        return redirect(url_for('login'))
    return render_template("registerAdmin.html", flag = False, form = form)

@app.route("/adminLogin", methods = ['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email = form.email.data).first()
        
        if not user:
            return render_template("loginAdmin.html", msg = "User doesnt exist", form = form)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            form = FileUpload()
            return render_template("upload.html", msg = "Login Successfull", form = form)
        flash("Login Unsuccessfull")
        return redirect(url_for('login'))
    return render_template("loginAdmin.html", form = form)


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
