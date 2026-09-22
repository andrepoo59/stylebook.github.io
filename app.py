"""StyleBook - Sprint 1 (HU-01 a HU-07)"""
import os
from flask import Flask, render_template
from dotenv import load_dotenv

from blueprints.auth import auth_bp
from blueprints.perfil import perfil_bp
from blueprints.profesionales import profesionales_bp
from blueprints.servicios import servicios_bp
from blueprints.admin import admin_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cambia-esto-en-produccion")

app.register_blueprint(auth_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(profesionales_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host= "0.0.0.0", port=port)

