from datetime import timedelta
from flask import Flask
app = Flask(__name__)
app.secret_key = "this is a secret key for sesion conf"

# la sesión durará 30minutos y luego expirará
app.permanent_session_lifetime = timedelta(minutes=30)