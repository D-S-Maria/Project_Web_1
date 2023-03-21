from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Логин / email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
