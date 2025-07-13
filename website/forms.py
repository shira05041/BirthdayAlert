from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from website.models import User

class RegisterForm(FlaskForm):
    name = StringField('שם', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('אימייל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired(), Length(min=6, max=100)])
    confirm_password = PasswordField('אישור סיסמה', validators=[DataRequired(), EqualTo('password', message='הסיסמאות אינן תואמות')])
    submit = SubmitField('הרשם')

    def validate_email(self, field):
        if '@' not in field.data:
            raise ValueError("Invalid email address")
        existing_user = User.query.filter_by(email=field.data).first()
        if existing_user:
            raise ValueError("Email already exists") 
        

class LoginForm(FlaskForm):
    email = EmailField('אימייל', validators=[DataRequired(), Email()])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    submit = SubmitField('התחבר')

class ContactForms(FlaskForm):
    name = StringField('שם', validators=[DataRequired(), Length(min=2, max=100)])
    date = DateField('תאריך לידה', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('הוסף')

class UpdateContactForm(FlaskForm):
    name = StringField('שם', validators=[DataRequired(), Length(min=2, max=100)])
    date = DateField('תאריך לידה', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('עדכן')

class DeleteContactForm(FlaskForm):
    submit = SubmitField('מחק')
    cancel = SubmitField('ביטול')


