from SeatedApp import app
from flask import render_template, url_for, redirect, flash
from SeatedApp.models import Item, User
from SeatedApp.forms import RegisterForm, LoginForm
from SeatedApp import db
from flask_login import login_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/info_Sede')
def infoSede_page():
    return render_template('infoSede.html')


@app.route('/CentroD')
def CentroD_page():
    return render_template('CentroD.html')


@app.route('/Log')
def Log_page():
    return render_template('Log.html')


@app.route('/Palazzo_Pacanowski')
def Palazzo_Pacanowski_page():
    return render_template('Palazzo_Pacanowski.html')


@app.route('/Sede')
def Sede_page():
    items = Item.query.all()
    return render_template('Sede.html', items=items)


@app.route('/SedeCentrale')
def SedeCentrale_page():
    return render_template('SedeCentrale.html')


@app.route('/ServizioC')
def ServizioC_page():
    return render_template('ServizioC.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('Sede_page'))
    if form.errors != {}:  # If there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'Errore nella creazione account: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Perfetto! Ti sei connesso come: {attempted_user.username}', category='success')
            return redirect(url_for('Sede_page'))
        else:
            flash('Username e/o password errati! Prova di nuovo', category='danger')

    return render_template('login.html', form=form)
