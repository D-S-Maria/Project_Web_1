import os

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.add_journey import AddJourney
from data.journey import Journey
from data.login_form import LoginForm
from data.register import RegisterForm
from data.users import User
from mail_sender import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    journey = db_sess.query(Journey).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name, name.email) for name in users}
    return render_template("index.html", journey=journey, names=names, title='Jourey list')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            city=form.city.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjourney', methods=['GET', 'POST'])
def addjourney():
    add_form = AddJourney()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        journey = Journey(
            country=add_form.country.data,
            user_id=add_form.user_id.data,
            month=add_form.month.data,
            about=add_form.about.data,
            transport=add_form.transport.data
        )
        db_sess.add(journey)
        db_sess.commit()
        return redirect('/')
    return render_template('addjourney.html', title='Adding a journey', form=add_form)


@app.route('/mail', methods=['GET'])
def get_form():
    return render_template('mail_me.html')


@app.route('/mail', methods=['POST'])
def post_form():
    email = request.values.get('email')
    text_msg = request.values.get('text_msg')
    if send_email(email, 'ответ на ваше предложение', text_msg=text_msg):
        return f'Письмо отправлено успешно на адрес {email}'
    return f'Во время отправки письма на {email} произошла ошибка'


def main():
    db_session.global_init("db/travel_prop.sqlite")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
