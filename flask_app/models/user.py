from flask import flash
from flask_app.models.models import Model
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# largo entre 8 y 16
# al menos una minúscula y una mayúscula
# al menos un dígito
PASS_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')



class User(Model):
    tabla = "users"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.genre = data['genre']
        self.birthday = data['birthday']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.bands = []

    @classmethod
    def save(cls, data):
        query = f"INSERT INTO {cls.tabla} ( first_name , last_name , email, genre, birthday, password ) VALUES ( %(fname)s , %(lname)s , %(email)s, %(genre)s, %(birthday)s, %(password)s );" 
        return connectToMySQL(cls.esquema).query_db( query, data )

    @classmethod
    def getByEmail(cls, email):
        query = f"SELECT * FROM {cls.tabla} WHERE email= %(email)s"
        results = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla,
            "email": email
        })

        if len(results) == 0:
            return False

        return cls(results[0])

    @staticmethod
    def validUser(dataUser):
        is_valid = True

        if len(dataUser['first_name']) < 2:
            flash("El nombre debe poseer al menos 2 caracteres", "danger")
            is_valid = False
        if len(dataUser['last_name']) < 2:
            flash("El Apellido debe poseer al menos 2 caracteres", "danger")
            is_valid = False
        if not EMAIL_REGEX.match(dataUser['email']): 
            flash("Debe ingresar una dirección de correo válida", "danger")
            is_valid = False
        if not dataUser['password'] == dataUser['password_confirm']:
            flash("Las contraseñan no coinciden", "danger")
            is_valid = False
        if not PASS_REGEX.match(dataUser['password']): 
            flash("Debe ingresar una contraseña válida", "danger")
            is_valid = False
        if 'accept_terms' not in dataUser:
            flash("Debes aceptar nuestros terminos para poder registrarte", "danger")
            is_valid = False
        if 'birthday' not in dataUser:
            flash("Debes ingresar una fecha de nacimiento", "danger")
            is_valid = False
        if 'genre' not in dataUser:
            flash("Debes indicar un genero", "danger")
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('esquema_bandas').query_db(query, {
            "email": dataUser['email'],
        })

        if len(results) > 0:
            flash("La dirección de correo ya se encuentra registrada", "danger")
            is_valid = False

        return is_valid