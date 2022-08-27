from flask import render_template, redirect, session, request, flash
from flask_app import app

# importacion del modelo
from flask_app.models.users import User

# importacion Bcrypt

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registrate', methods=['POST'])
def registrate():
    # validar info ingresada
    if not User.valida_usuario(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)  # recive id de la nueva persona

    session['user_id'] = id

    return redirect('/appointments')


@app.route('/login', methods=['POST'])
def login():
    # verificar que el email exista
    user = User.get_by_email(request.form)
    if not user:
        flash('E-mail no encontrado', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/appointments')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
