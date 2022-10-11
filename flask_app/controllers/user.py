from flask_app import app
from flask import flash, render_template, session, redirect, request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if not isLogged():
        return render_template("index.html")
    return redirect('/home')

@app.route("/home")
def home():
    if not isLogged():
        return render_template("index.html")

    return render_template('home.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# validamos que se encuentre una sesión activa
def isLogged():
    if 'user' in session:
        return True

    return False

@app.route("/register", methods = ["POST"])
def createUser():
    if not User.validUser(request.form):
        return redirect('/')

    pwHash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'fname': request.form['first_name'],
        'lname': request.form['last_name'],
        'email': request.form['email'],
        'password': pwHash,
        'genre': request.form['genre'],
        'birthday': request.form['birthday'],
    }
    userId = User.save(data)

    if userId is False:
        flash("Lo sentimos, ha ocurrido un erro al registrar un nuevo usuario", "danger")

    session['user'] = {
        'id': userId,
        'name': data["fname"] +" "+ data["lname"],
    }

    flash("Te has registrado correctamente", "success")
    return redirect('/home')

@app.route("/login", methods = ["POST"])
def loginUser():
    user = User.getByEmail(request.form['email'])

    if user is False:
        flash('email / password incorrectos!', 'warning')
        return redirect('/')

    print("PSW", bcrypt.check_password_hash(user.password, request.form['password']))
    if bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash('email / password incorrectos!', 'warning')
        return redirect('/')

    session['user'] = {
        'id': user.id,
        'name': user.first_name +" "+ user.last_name
    }

    flash("Te has logeado correctamente", "success")
    return redirect('/home')