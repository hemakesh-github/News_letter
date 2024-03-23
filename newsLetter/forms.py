from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import email_validator
from .models import Subscribers, Admin
from flask_wtf.file import FileAllowed


class SubscribersForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe to monthly newsletter')

    def validate_email(self, email):
        user = Subscribers.query.filter_by(email = email.data).first()
        if user != None:
            raise ValidationError('The username is already taken')

    def __repr__(self):
        return f"name: {self.name}\temail: {self.email}"

class Login(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Log In")

    def validate_email(self, email):
        user = Admin.query.filter_by(email = email.data).first()
        if user == None:
            raise ValidationError('User does not exist')
        


class Register(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("confirm password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_email(self, email):

        user = Subscribers.query.filter_by(email = email.data).first()
        if user != None:
            raise ValidationError('Email already exists')


class FileUpload(FlaskForm):
    file = FileField("Add file to send(pdf or word format)", validators=[FileAllowed(['.pdf', '.docx'])] )
    submit = SubmitField("Send")
